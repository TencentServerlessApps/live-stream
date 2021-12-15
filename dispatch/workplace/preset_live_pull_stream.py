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
        err = self.check_params(preset_stream_data)
        if err:
            logger.error(msg='[{time} check params error {err}'.format(
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                err=err
            ))
            return err
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

    def check_params(self, preset_stream_data):
        try:
            err_message = ""
            if 'Outputs' not in preset_stream_data:
                err_message = "Outputs is empty"
            if 'JobName' not in preset_stream_data:
                err_message = "JobName is empty"
            if 'TargetUrls' not in preset_stream_data["Outputs"]:
                err_message = "TargetUrls is empty"
            if 'SourceType' not in preset_stream_data:
                err_message = "SourceType is empty"
            if 'SourceUrl' not in preset_stream_data and 'SourceUrls' not in preset_stream_data:
                err_message = "Source is empty"
            if 'SourceUrls' in preset_stream_data and len(preset_stream_data["SourceUrls"]) != 0:
                if preset_stream_data["SourceType"] != "PullVodPushLive":
                    err_message = "vod only support SourceType:PullVodPushLive"
                if len(preset_stream_data["Outputs"]["TargetUrls"]) != 1:
                    err_message = "SourceUrls loop only support one target"
            if 'Loop' in preset_stream_data and preset_stream_data["Loop"] < 1:
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

    def preset_live_stream(self, preset_stream_data):
        try:
            job_struct = None
            create_time = int(time.time())
            job_metadata = {
                "JobId": self.job_id,
                "JobType": JobOfPreset,
                "SourceType": preset_stream_data['SourceType'],
                "PresetStartTime": preset_stream_data['PresetStartTime'],
                "CreateTime": create_time,
                "TargetUrls": preset_stream_data['Outputs']['TargetUrls'],
            }
            if 'JobName' in preset_stream_data and preset_stream_data['JobName'] != "":
                job_metadata["JobName"] = preset_stream_data['JobName']
            if 'SourceUrl' in preset_stream_data and preset_stream_data['SourceUrl'] != "":
                job_metadata["SourceUrl"] = preset_stream_data['SourceUrl']
            logger.info("preset_stream_data['SourceUrls']:"+ str(preset_stream_data['SourceUrls']))
            if 'SourceUrls' in preset_stream_data and len(preset_stream_data['SourceUrls']) > 0:
                job_metadata["SourceUrls"]  = preset_stream_data['SourceUrls']
            if 'Loop' in preset_stream_data and preset_stream_data['Loop'] > 0:
                job_metadata["Loop"]  = preset_stream_data['Loop']
            if 'CallbackUrl' in preset_stream_data and preset_stream_data['CallbackUrl'] != "":
                job_metadata["CallbackUrl"] = preset_stream_data['CallbackUrl']
            if 'TranscodeParams' in preset_stream_data and preset_stream_data['TranscodeParams'] != "":
                job_metadata["TranscodeParams"] = preset_stream_data['TranscodeParams']
            if 'FailureRetryTimes' in preset_stream_data:
                job_metadata["FailureRetryTimes"]  = preset_stream_data['FailureRetryTimes']
            if 'StreamIdleTimeout' in preset_stream_data:
                job_metadata["StreamIdleTimeout"]  = preset_stream_data['StreamIdleTimeout']
            if 'StreamBrokenSleepInterval' in preset_stream_data:
                job_metadata["StreamBrokenSleepInterval"]  = preset_stream_data['StreamBrokenSleepInterval']
            if 'StartLive' in preset_stream_data['Outputs']:
                job_metadata["StreamHandlerStart"] = preset_stream_data['Outputs']['StartLive']
            if 'Duration' in preset_stream_data['Outputs']:
                job_metadata["StreamHandlerDuration"] = preset_stream_data['Outputs']['Duration']
            job_struct = JobStruct(job_metadata, self.redis_client)
            job_struct.data_sync()
            self.redis_client.zadd(key=PushLiveJobsSet, score=create_time, name=self.job_id)
            resp = self.create_timer(preset_stream_data['JobName'], preset_stream_data['PresetStartTime'])

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
            'FunctionName': os.environ.get('SCF_FUNCTIONNAME'),
            'Namespace': os.environ.get('SCF_NAMESPACE'),
            'Type': 'timer',
            'TriggerName': '{name}_{time}'.format(name=job_name, time=str(preset_time)),
            'TriggerDesc': cron_descriptor(int(preset_time)),
            'Enable': 'OPEN',
            'CustomArgument': json.dumps({'JobId': self.job_id})
        }

        resp = qcloud_caller('CreateTrigger', worker_params)
        return resp

