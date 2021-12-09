# -*- coding -*-

import os
import json
import time
import logging
import traceback
import threading

from etc.config import *
from error.errors import *
from api.scf import qcloud_caller
from module.task_struct import JobStruct
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import uuid_generator, cron_descriptor
from module.request_module import CreatePresetStreamRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CreatePresetLivePullStreamTaskWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = uuid_generator()
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        preset_stream_request = CreatePresetStreamRequest(data)
        preset_stream_data = preset_stream_request.get_value(is_common_check=True)

        try:
            self.preset_live_stream(preset_stream_data)

            response = {
                "JobId": self.job_id,
            }
            return response

        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def preset_live_stream(self, preset_stream_data):
        job_struct = None
        create_time = int(time.time())
        job_name = preset_stream_data['JobName']
        preset_time = int(preset_stream_data['PresetStartTime'])
        source_type = preset_stream_data['SourceType']
        source_url = preset_stream_data['SourceUrl']
        callback_url = preset_stream_data['CallbackUrl']
        stream_handler_start = preset_stream_data['Outputs']['StartLive']
        stream_handler_duration = preset_stream_data['Outputs']['Duration']
        stream_target_urls = preset_stream_data['Outputs']['TargetUrls']
        failure_retry_times = preset_stream_data['FailureRetryTimes']
        stream_idle_timeout = preset_stream_data['StreamIdleTimeout']
        stream_broken_sleep_interval = preset_stream_data['StreamBrokenSleepInterval']


        try:
            job_metadata = {
                "JobName": job_name,
                "JobId": self.job_id,
                "JobType": JobOfPreset,
                "PresetStartTime": preset_time,
                "SourceType": source_type,
                "SourceUrl": source_url,
                "TargetUrls": stream_target_urls,
                "CallbackUrl": callback_url,
                "StreamHandlerStart": stream_handler_start,
                "StreamHandlerDuration": stream_handler_duration,
                "FailureRetryTimes": failure_retry_times,
                "StreamIdleTimeout": stream_idle_timeout,
                "StreamBrokenSleepInterval": stream_broken_sleep_interval,
                "CreateTime": create_time
            }
            job_struct = JobStruct(job_metadata, self.redis_client)
            job_struct.data_sync()
            self.redis_client.zadd(key=PushLiveJobsSet, score=create_time, name=self.job_id)
            resp = self.create_timer(job_name, preset_time)

            if not resp['success']:
                error_message = resp['err_msg']
                job_struct.delete()
                raise PresetCronTaskError(message=error_message)

        except Exception as e:
            print(traceback.print_exc())
            if job_struct is not None:
                job_struct.delete()
            raise e

    def create_timer(self, job_name, preset_time):
        worker_params = {
            'FunctionName': 'livestream_dispatch',
            'Namespace': os.environ.get('WorkerNameSpace'),
            'Type': 'timer',
            'TriggerName': '{name}_{time}'.format(name=job_name, time=str(preset_time)),
            'TriggerDesc': cron_descriptor(preset_time),
            'Enable': 'OPEN',
            'CustomArgument': json.dumps({'JobId': self.job_id})
        }

        resp = qcloud_caller('CreateTrigger', worker_params)
        return resp

