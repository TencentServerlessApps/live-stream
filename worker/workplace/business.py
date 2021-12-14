# -*- coding: utf-8 -*-

import re
import os
import time
import json
import logging
import requests
import datetime
import traceback
import threading
import subprocess
from queue import Queue

from etc.config import *
from module.redis_helper import RedisClient
from module.task_struct import TaskStruct
from workplace.base_worker import BaseWorker
from workplace.common.tools import task_identifier, \
    event_queue_identifier, time_to_num
from error.errors import BaseError, ResourceNotFoundTask

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MainHandler(BaseWorker):

    def __init__(self, inputs):
        self.task_id = inputs['TaskId']
        self.event_deliver_mq = Queue()
        self.redis_client = RedisClient()
        self.task_struct = None
        self.ffmpeg_cmd_list = None
        # 控制主进程是否退出
        self.watch_dog_wake = False
        # 控制转码输出监听是否因信号退出
        self.ffmpeg_exit_by_sig = False

        self.event_handler_map = {
            PausedSig: self.paused_handler,
            ResumeSig: self.resume_handler,
            TerminateSig: self.finish_handler,
            RefreshSig: self.refresh_handler,
            FFmpegNormalTerminateSig: self.ffmpeg_exit_handler,
            FFmpegAbnormalTerminateSig: self.ffmpeg_exit_handler,
            WorkerTerminateSig: self.work_exit_handler
        }

        # 初始化等待睡眠时长
        if 'StreamBrokenSleepInterval' in inputs and \
                isinstance(inputs['StreamBrokenSleepInterval'], int):
            self.stream_broken_sleep_interval = inputs['StreamBrokenSleepInterval']
        else:
            self.stream_broken_sleep_interval = StreamBrokenSleepInterval
        # 工作中断流等待拉起前睡眠时间
        if 'StreamIdleTimeOut' in inputs and \
                isinstance(inputs['StreamIdleTimeOut'], int):
            self.stream_idle_timeout = inputs['StreamIdleTimeOut'] * 1000 * 1000
        else:
            self.stream_idle_timeout = StreamIdleTimeOut
        # FFmpeg异常退出后重试次数
        if 'FailureRetryTimes' in inputs and \
                isinstance(inputs['FailureRetryTimes'], int):
            self.failure_retry_times = inputs['FailureRetryTimes']
        else:
            self.failure_retry_times = FFmpegJobRetry

    def main_handler(self):

        # 先开启信号监听和事件处理线程
        base_task_list = []
        event_handler = threading.Thread(target=self.event_handler_loop,
                                         args=(), daemon=True)
        base_task_list.append(event_handler)
        signal_listener = threading.Thread(target=self.signal_listener,
                                           args=(), daemon=True)
        base_task_list.append(signal_listener)
        for item in base_task_list:
            item.start()

        try:
            self.task_struct = self.redis_client.get(task_identifier(self.task_id))['data']
            if not self.task_struct:
                logger.info(msg='[{time} {task_id} ResourceNotFoundTask] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=''
                ))
                raise ResourceNotFoundTask()
            else:
                logger.info(msg='[{time} {task_id} TaskStructInit] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=self.task_struct
                ))
                self.task_struct = TaskStruct(metadata=json.loads(self.task_struct),
                                              data_sync_client=self.redis_client)
                self.task_struct.update('TaskStartTime', int(time.time()))
                self.task_struct.save()

            listener_list = []
            stream_listener = threading.Thread(target=self.stream_listener,
                                               args=(), daemon=True)
            listener_list.append(stream_listener)

            for item in listener_list:
                item.start()

            self.watch_dog()
        except BaseError as e:
            print(traceback.print_exc())
            logger.info(msg='[{time} {task_id} InternalError] {message}'.format(
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                task_id=self.task_id,
                message=print(traceback.print_exc())
            ))

        finally:
            return

    def stream_listener(self):
        try:
            monitor_control = {
                # 控制转码输出监听是否因超过重试次数而退出
                'ffmpeg_exit_by_monitor': None,
            }

            while True:
                while self.ffmpeg_exit_by_sig or \
                        monitor_control['ffmpeg_exit_by_monitor']:
                    time.sleep(StreamHandlerIdleSleep)

                self.ffmpeg_monitor(monitor_control)

        except Exception as e:
            logger.info(msg='[{time} {task_id} InternalError] {message}'.format(
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                task_id=self.task_id,
                message=print(traceback.print_exc())
            ))
        finally:
            return

    def signal_listener(self):
        event_queue = event_queue_identifier(self.task_id)
        while True:
            try:
                event = self.redis_client.blpop([event_queue], timeout=2)
                event_data = event['data']
                if event_data:
                    logger.info(msg='[{time} {task_id} receiveEventSuccess] {msg}'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                        msg=''
                    ))

                    msg = {
                        'from': 'signal_listener',
                        'event': event_data[1]
                    }
                    try:
                        self.event_deliver_mq.put(msg)
                    except Exception as e:
                        logger.info(msg='[{time} {task_id} EventHandlerError] {msg}'.format(
                            time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            task_id=self.task_id,
                            msg=''
                        ))
            except Exception as e:
                logger.info(msg='[{time} {task_id} SignalListenerError] {msg}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    msg=print(traceback.print_exc())
                ))

    def watch_dog(self):
        while not self.watch_dog_wake:
            time.sleep(WatchDogSleepTime)

        time.sleep(WatchDogSleepTime * 5)

    def ffmpeg_monitor(self, monitor_control):
        current_retry = 0
        current_stream_error = False
        is_stream_init = True
        sig = FFmpegNormalTerminateSig
        monitor_control['ffmpeg_exit_by_monitor'] = False
        if self.task_struct.get("SourceUrls"):
            if len(list(self.task_struct.get('SourceUrls'))) > 0:
                self.ffmpeg_cmds()
            else:
                return
        else:
            self.ffmpeg_cmd()

        while True:
            # 开启转码进程
            proc = subprocess.Popen(
                self.ffmpeg_cmd_list, stderr=subprocess.PIPE, universal_newlines=True)

            # 监听转码输出日志
            while True:

                if self.ffmpeg_exit_by_sig:
                    logger.info(msg='[{time} {task_id} FFmpeg Kill] {msg}'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                        msg=''
                    ))
                    break
                o_pipe = proc.stderr.readline().strip()
                if o_pipe:
                    logger.info(msg='[{time} {task_id} FFmpeg Output] {msg}'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                        msg=str(o_pipe)
                    ))
                    cur_time = re.search(VideoRealtime, o_pipe)
                    # 记录视频现阶段处理的时间
                    if cur_time:
                        video_realtime = cur_time.groupdict()['t']
                        self.task_struct.stream_handler_offset = time_to_num(video_realtime)
                    for error_item in StreamError:
                        if error_item in o_pipe:
                            current_stream_error = True
                            break
                # 读取到EOF
                else:
                    break

            # 确保转码进程退出
            while proc.poll() is None:
                if self.ffmpeg_exit_by_sig:
                    proc.kill()
                    return
                time.sleep(2)

            ffmpeg_exit_code = proc.poll()
            # 检查转码进程退出后的相关信息，决定是否重启
            if current_stream_error:
                if is_stream_init:
                    is_stream_init = False
                    current_stream_error = False
                    time.sleep(self.stream_broken_sleep_interval)
                    logger.info(msg='[{time} {task_id} StreamInitError]'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                    ))

                time.sleep(self.stream_broken_sleep_interval)
                current_stream_error = False
                current_retry += 1
                sig = FFmpegAbnormalTerminateSig
                logger.info(msg='[{time} {task_id} StreamHandlerError]'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                ))

            else:
                if ffmpeg_exit_code == FFmpegErrorExitCode:
                    current_retry += 1
                    sig = FFmpegAbnormalTerminateSig
                    logger.info(msg='[{time} {task_id} FFmpegExitWithError]'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                    ))
                elif ffmpeg_exit_code == FFmpegNormalExitCode:
                    pass

            # 发送退出信号
            if current_retry >= self.failure_retry_times \
                    or ffmpeg_exit_code == FFmpegNormalExitCode:
                monitor_control['ffmpeg_exit_by_monitor'] = True
                event_msg = {
                    'from': 'stream_listener',
                    'event': sig,
                }
                self.event_deliver_mq.put(event_msg)
                break

    def ffmpeg_cmd(self):
        pass

    def ffmpeg_cmds(self):
        pass

    def event_handler_loop(self):
        # 收到信号，置位watch_dog_wake和ffmpeg_exit_by_self
        while True:
            event_package = {}
            try:
                event_package = self.event_deliver_mq.get(block=True)
                logger.info(msg='[{time} {task_id} GetEventSuccess] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=json.dumps(event_package)
                ))
            except Exception as e:
                logger.info(msg='[{time} {task_id} GetEventError] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=print(traceback.print_exc())
                ))

            # 根据信号不同，做后续处理
            # 信号分三类: 转码进程退出(有可能是异常退出)信号
            #            任务处理进程退出信号
            #            任务状态变更信号
            event = event_package['event']
            handler = self.event_handler_map.get(event, None)

            try:
                if callable(handler):
                    handler(event)
                else:
                    logger.info(msg='[{time} {task_id} EventHandlerNotCallable] {message}'.format(
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        task_id=self.task_id,
                        message=''
                    ))
                logger.info(msg='[{time} {task_id} ProcessEventSuccess] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=''
                ))
            except Exception as e:
                logger.info(msg='[{time} {task_id} ProcessEventError] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=print(traceback.print_exc())
                ))
            finally:
                task_info = self.redis_client.get(task_identifier(self.task_id))['data']
                logger.info(msg='[{time} {task_id} RealTimeTaskInfo] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=task_info
                ))
                logger.info(msg='[{time} {task_id} RealTimeTaskInfo] {message}'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message='start={start}, duration={duration}'.format(
                        start=self.task_struct.get('StreamHandlerStart'),
                        duration=self.task_struct.get('StreamHandlerDuration')
                    )
                ))
                if event in [TerminateSig, FFmpegNormalTerminateSig,
                             FFmpegAbnormalTerminateSig, WorkerTerminateSig]:
                    self.watch_dog_wake = True
                    break

    def paused_handler(self, event):
        pass
                
    def resume_handler(self, event):
        self.ffmpeg_exit_by_sig = False
        self.task_struct.update('Status', TaskRunning)
        self.task_struct.save()

    def refresh_handler(self, event_package):
        return

    def finish_handler(self, event_package):
        data = {
            'TaskId': self.task_struct.get('TaskId'),
            'TargetUrl': self.task_struct.get('TargetUrl'),
            'SourceUrl': self.task_struct.get('SourceUrl'),
            'Message': 'Task exit by user'
        }
        self.task_struct.update('Status', TaskFinish)
        self.task_struct.update('TaskFinishTime', int(time.time()))
        self.task_struct.save()

        self.ffmpeg_exit_by_sig = True
        self.callback(data)

    def ffmpeg_exit_handler(self, event):
        data = {
            'TaskId': self.task_struct.get('TaskId'),
            'TargetUrl': self.task_struct.get('TargetUrl'),
            'SourceUrl': self.task_struct.get('SourceUrl'),
        }
        if event == FFmpegNormalTerminateSig:
            data['Message'] = 'Task finish when ffmpeg exit[0]'
            self.task_struct.update('Status', TaskFinish)
        elif event == FFmpegAbnormalTerminateSig:
            data['Message'] = 'Task finish when ffmpeg exit[1]'
            self.task_struct.update('Status', TaskFailed)
        self.task_struct.update('TaskFinishTime', int(time.time()))
        self.task_struct.update('ErrorMessage', data['Message'])
        self.task_struct.save()
        self.callback(data)

    def work_exit_handler(self, event):
        data = {
            'TaskId': self.task_struct.get('TaskId'),
            'Message': 'Task finish when internal error happened',
            'TargetUrl': self.task_struct.get('TargetUrl'),
            'SourceUrl': self.task_struct.get('SourceUrl'),
        }
        self.task_struct.save()
        self.ffmpeg_exit_by_sig = True
        self.callback(data)

    def callback(self, data):
        callback_url = self.task_struct.get('CallbackUrl')
        if callback_url is None:
            logger.info(msg='[{time} {task_id} CallbackUrlNotSet]'.format(
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                task_id=self.task_id,
            ))
        else:
            try:
                requests.request('POST', callback_url,
                                 data=json.dumps(data), timeout=5)
                logger.info(msg='[{time} {task_id} CallbackSuccess {message}]'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=json.dumps(data)
                ))
            except Exception as e:
                logger.info(msg='[{time} {task_id} CallbackFailed {message}]'.format(
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    task_id=self.task_id,
                    message=print(traceback.print_exc())
                ))


class VodToRtmpHandler(MainHandler):

    def __init__(self, inputs):
        super(VodToRtmpHandler, self).__init__(inputs)

    def ffmpeg_cmd(self):

        stream_handler_duration = int(self.task_struct.get('StreamHandlerDuration'))
        stream_handler_start = int(self.task_struct.get('StreamHandlerStart'))
        transcode_params = self.task_struct.get('TranscodeParams')

        if stream_handler_duration == 0:
            offset_config = '-ss {handler_start}'.format(
                handler_start=stream_handler_start
            )
        else:
            offset_config = '-ss {handler_start} -t {handler_duration}'.format(
                handler_start=stream_handler_start,
                handler_duration=stream_handler_duration
            )
        if transcode_params is None:
            transcode_params = "-c copy"
        cmd_origin = FFmpegVodToRtmp
        cmd = cmd_origin.format(offset_config=offset_config,
                                source_url=self.task_struct.get('SourceUrl'),
                                transcode_params=transcode_params,
                                target_url=self.task_struct.get('TargetUrl'))
        logger.info(msg='[{time} {task_id} FFmpeg Cmd] {message}'.format(
            time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            task_id=self.task_id,
            message=cmd
        ))
        self.ffmpeg_cmd_list = cmd.split(' ')

    def ffmpeg_cmds(self):
        source_urls=self.task_struct.get('SourceUrls')[0],
        stream_handler_duration = int(self.task_struct.get('StreamHandlerDuration'))
        stream_handler_start = int(self.task_struct.get('StreamHandlerStart'))
        loop = int(self.task_struct.get('Loop'))
        transcode_params = self.task_struct.get('TranscodeParams')
        if stream_handler_duration == 0:
            offset_config = '-ss {handler_start}'.format(
                handler_start=stream_handler_start
            )
        else:
            offset_config = '-ss {handler_start} -t {handler_duration}'.format(
                handler_start=stream_handler_start,
                handler_duration=stream_handler_duration
            )
        if transcode_params is None:
            transcode_params = "-c copy"
        cmd_origin = FFmpegVodsToRtmp
        local_path = '/tmp/local_file.txt'
        if os.path.exists(local_path):
            os.remove(local_path)
        os.mknod(local_path)
        f = open(local_path, 'w')
        logger.info("source_urls: %s", str(source_urls[0]))
        for i in range(0, loop):
            for source_url in source_urls[0]:
                logger.info("source_url: %s", str(source_url))
                f.write("file "+ source_url)
                f.write("\n")
        cmd = cmd_origin.format(file_path=local_path,
                                transcode_params=transcode_params,
                                target_url=self.task_struct.get('TargetUrl'))
        logger.info(msg='[{time} {task_id} FFmpeg Cmds] {message}'.format(
            time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            task_id=self.task_id,
            message=cmd
        ))
        f.close()
        self.ffmpeg_cmd_list = cmd.split(' ')

    def refresh_handler(self, event):
        pass

    def paused_handler(self, event):
        self.ffmpeg_exit_by_sig = True
        self.task_struct.update('Status', TaskPaused)
        duration_update = int(self.task_struct.get('StreamHandlerDuration') -
                              self.task_struct.stream_handler_offset)
        if duration_update < 0:
            duration_update = 0
        self.task_struct.update('StreamHandlerDuration', duration_update)
        start_live_update = int(self.task_struct.get('StreamHandlerStart') +
                                self.task_struct.stream_handler_offset)
        self.task_struct.update('StreamHandlerStart', start_live_update)
        self.task_struct.stream_handler_offset = 0
        self.task_struct.save()


class RtmpToRtmpHandler(MainHandler):

    def __init__(self, inputs):
        super(RtmpToRtmpHandler, self).__init__(inputs)

    def ffmpeg_cmd(self):
        cmd_origin = FFmpegRtmpToRtmp
        cmd = cmd_origin.format(stream_idle_timeout=self.stream_idle_timeout,
                                source_url=self.task_struct.get('SourceUrl'),
                                target_url=self.task_struct.get('TargetUrl'))
        logger.info(msg='[{time} {task_id} FFmpeg Cmd] {message}'.format(
            time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            task_id=self.task_id,
            message=cmd
        ))
        self.ffmpeg_cmd_list = cmd.split(' ')

    def paused_handler(self, event):
        self.ffmpeg_exit_by_sig = True
        self.task_struct.update('Status', TaskPaused)
        self.task_struct.stream_handler_offset = 0
        self.task_struct.save()








