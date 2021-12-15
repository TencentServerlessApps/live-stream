# -*- coding -*-

import os
import json
import time
import logging
import traceback
import threading
import datetime
from etc.config import *
from error.errors import *
from api.scf import qcloud_caller
from module.task_struct import JobStruct, TaskStruct
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import uuid_generator, job_identifier
from module.request_module import CreateStreamRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CreateLivePullStreamTaskWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

        self.job_struct = None

    def main_handler(self):

        data = self.inputs.get('Data', {})
        create_stream_request = CreateStreamRequest(data)
        create_stream_data = create_stream_request.get_value(is_common_check=True)
        err = self.check_params(create_stream_data)
        if err:
            logger.error(msg='[{time} check params error {err}'.format(
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                err=err
            ))
            return err
        target_urls = create_stream_data['Outputs']['TargetUrls']
        source_url = create_stream_data['SourceUrl']
        self.job_id = create_stream_data['JobId']
        try:
            # 判断是否需要创建JobStruct
            if self.job_id == '':
                self.job_id = uuid_generator()
                self.init_job(create_stream_data)
            else:
                job_data = self.redis_client.get(key=job_identifier(job_id=self.job_id))['data']
                if not job_data:
                    raise ResourceNotFoundJob()
                self.job_struct = JobStruct(metadata=json.loads(job_data),
                                            data_sync_client=self.redis_client,
                                            is_init_from_db=True)

            # 多线程分发任务，确保快速拉起转推任务
            unit_count = self.worker_estimate(target_urls)
            worker_list = []
            invoke_worker_count = 0
            while True:
                if len(target_urls) == 0:
                    break
                url_list = []
                for i in range(unit_count):
                    if len(target_urls) > 0:
                        target_url = target_urls.pop(-1)
                    else:
                        break
                    url_list.append(target_url)
                    self.task_map[target_url] = {}
                stream_worker = threading.Thread(target=self.create_live_stream,
                                                 args=(create_stream_data, url_list,))
                worker_list.append(stream_worker)

            for task in worker_list:
                invoke_worker_count += 1
                task.start()

            for task in worker_list:
                task.join()

            task_info = []
            task_list = []
            for k, v in self.task_map.items():
                task_list.append(v['TaskId'])
                task_info.append(v)
            self.job_struct.update('TaskIds', task_list)
            self.job_struct.data_sync()

            response = {
               "JobId": self.job_id,
               "SourceUrl": source_url,
               "TaskInfos": task_info,
            }
            return response

        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def check_params(self, create_stream_data):
        try:
            err_message = ""
            if 'Outputs' not in create_stream_data:
                err_message = "Outputs is empty"
            if 'JobName' not in create_stream_data:
                err_message = "JobName is empty"
            if 'TargetUrls' not in create_stream_data["Outputs"]:
                err_message = "TargetUrls is empty"
            if 'SourceType' not in create_stream_data:
                err_message = "SourceType is empty"
            if 'SourceUrl' not in create_stream_data and 'SourceUrls' not in create_stream_data:
                err_message = "Source is empty"
            if 'SourceUrls' in create_stream_data and len(create_stream_data["SourceUrls"]) != 0:
                if create_stream_data["SourceType"] != "PullVodPushLive":
                    err_message = "vod only support SourceType:PullVodPushLive"
                if len(create_stream_data["Outputs"]["TargetUrls"]) != 1:
                    err_message = "SourceUrls loop only support one target"
            if 'Loop' in create_stream_data and create_stream_data["Loop"] < 1:
                err_message = "Loop num is invalid"
            if err_message != "":
                return {
                    'ErrorCode': "InvalidParameter",
                    'ErrorMessage': err_message,
                }
            return None
        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def worker_estimate(self, basic_factor):
        except_workers = os.environ.get('InvokeThreads', InvokeDefaultThreads)
        if except_workers > InvokeMaxThreads:
            except_workers = InvokeDefaultThreads

        unit_count = len(basic_factor) / except_workers
        if unit_count > int(unit_count):
            unit_count = int(unit_count) + 1
        else:
            unit_count = int(unit_count)
        return unit_count
    
    def init_job(self, create_stream_data):
        try:
            preset_time = 0
            create_time = int(time.time())
            job_metadata = {
                "JobName": create_stream_data['JobName'],
                "JobId": self.job_id,
                "JobType": JobOfRealTime,
                "PresetStartTime": preset_time,
                "SourceType": create_stream_data['SourceType'],
                "TargetUrls": create_stream_data['Outputs']['TargetUrls'],
                "CreateTime": create_time,
            }
            if 'SourceUrl' in create_stream_data and create_stream_data['SourceUrl'] != "":
                job_metadata["SourceUrl"] = create_stream_data['SourceUrl']
            logger.info("create_stream_data['SourceUrls']:"+ str(create_stream_data['SourceUrls']))
            if 'SourceUrls' in create_stream_data and len(create_stream_data['SourceUrls']) > 0:
                job_metadata["SourceUrls"]  = create_stream_data['SourceUrls']
            if 'Loop' in create_stream_data:
                job_metadata["Loop"]  = create_stream_data['Loop']
            if 'CallbackUrl' in create_stream_data and create_stream_data['CallbackUrl'] != "":
                job_metadata["CallbackUrl"] = create_stream_data['CallbackUrl']
            if 'TranscodeParams' in create_stream_data and create_stream_data['TranscodeParams'] != "":
                job_metadata["TranscodeParams"] = create_stream_data['TranscodeParams']
            if 'FailureRetryTimes' in create_stream_data:
                job_metadata["FailureRetryTimes"]  = create_stream_data['FailureRetryTimes']
            if 'StreamIdleTimeout' in create_stream_data:
                job_metadata["StreamIdleTimeout"]  = create_stream_data['StreamIdleTimeout']
            if 'StreamBrokenSleepInterval' in create_stream_data:
                job_metadata["StreamBrokenSleepInterval"]  = create_stream_data['StreamBrokenSleepInterval']
            if 'StartLive' in create_stream_data['Outputs']:
                job_metadata["StreamHandlerStart"] = create_stream_data['Outputs']['StartLive']
            if 'Duration' in create_stream_data['Outputs']:
                job_metadata["StreamHandlerDuration"] = create_stream_data['Outputs']['Duration']
            self.job_struct = JobStruct(job_metadata, self.redis_client)
            self.job_struct.data_sync()
            self.redis_client.zadd(key=PushLiveJobsSet, score=create_time, name=self.job_id)
        except Exception as e:
            print(traceback.print_exc())
            raise e

    def create_live_stream(self, create_stream_data, url_list):
        for stream_target_url in url_list:
            task_id = uuid_generator()
            try:
                task_metadata = {
                    "JobId": self.job_id,
                    "TaskId": task_id,
                    "RequestId": '',
                    "SourceType": create_stream_data['SourceType'],
                    "TargetUrl": stream_target_url,
                    "TaskStartTime": '',
                    "TaskPausedTime": '',
                    "TaskFinishTime": '',
                    "Status": TaskRunning,
                    "StreamHandlerOffset": 0,
                    "ErrorMessage": '',
                }
                event = {
                    'WorkType': create_stream_data['SourceType'],
                    'TaskId': task_id,
                }
                if 'SourceUrl' in create_stream_data and create_stream_data['SourceUrl'] != "":
                    task_metadata["SourceUrl"] = create_stream_data['SourceUrl']
                if 'SourceUrls' in create_stream_data and len(create_stream_data['SourceUrls']) >0:
                    task_metadata["SourceUrls"]  = create_stream_data['SourceUrls']
                if 'Loop' in create_stream_data:
                    task_metadata["Loop"]  = create_stream_data['Loop']
                if 'CallbackUrl' in create_stream_data and create_stream_data['CallbackUrl'] != "":
                    task_metadata["CallbackUrl"] = create_stream_data['CallbackUrl']
                if 'TranscodeParams' in create_stream_data and create_stream_data['TranscodeParams'] != "":
                    task_metadata["TranscodeParams"] = create_stream_data['TranscodeParams']
                if 'StartLive' in create_stream_data['Outputs']:
                    task_metadata["StreamHandlerStart"] = create_stream_data['Outputs']['StartLive']
                if 'Duration' in create_stream_data['Outputs']:
                    task_metadata["StreamHandlerDuration"] = create_stream_data['Outputs']['Duration']
                if 'FailureRetryTimes' in create_stream_data:
                    event["FailureRetryTimes"]  = create_stream_data['FailureRetryTimes']
                if 'StreamIdleTimeout' in create_stream_data:
                    event["StreamIdleTimeout"]  = create_stream_data['StreamIdleTimeout']
                if 'StreamBrokenSleepInterval' in create_stream_data:
                    event["StreamBrokenSleepInterval"]  = create_stream_data['StreamBrokenSleepInterval']
                task_struct = TaskStruct(task_metadata, self.redis_client)
                task_struct.data_sync()

                resp = self.worker_caller(event)
                if not resp['success']:
                    error_message = resp['err_msg']
                    task_struct.update('Status', TaskFailed)
                    task_struct.update('ErrorMessage', error_message)
                    task_struct.data_sync()
                    raise InvokeWorkerError()

                self.task_map[stream_target_url] = {
                    "TargetUrl": stream_target_url,
                    "TaskId": task_id,
                    "Result": "Ok"
                }

            except Exception as e:
                print(traceback.print_exc())
                self.task_map[stream_target_url] = {
                    "TargetUrl": stream_target_url,
                    "TaskId": task_id,
                    "Result": "Error"
                }

    def worker_caller(self, event):
        worker_params = {
            'FunctionName': os.environ.get('WOKER_NAME'),
            'Event': json.dumps(event),
            'Namespace': os.environ.get('SCF_NAMESPACE')
        }

        resp = qcloud_caller('InvokeFunction', worker_params)
        return resp

