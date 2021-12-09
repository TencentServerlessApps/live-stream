# -*- coding -*-

import os
import json
import logging
import traceback

from error.errors import *
from api.scf import qcloud_caller
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import job_identifier
from module.request_module import DescribeJobRequest
from workplace.create_live_pull_stream import CreateLivePullStreamTaskWorker

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CronTaskWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        describe_job_request = DescribeJobRequest(data)
        describe_job_data = describe_job_request.get_value(is_common_check=True)
        self.job_id = describe_job_data['JobId']
        try:
            # self.struct = {
            #     "JobName": metadata.get("JobName", None),
            #     "JobId": metadata.get("JobId", None),
            #     "JobType": metadata.get("JobType", JobOfRealTime),
            #     "JobDetail": {
            #         "PresetStartTime": metadata.get("PresetStartTime", ''),
            #         "StartLive": metadata.get("StartLive", 0),
            #         "SourceType": metadata.get("SourceType", ''),
            #         "SourceUrl": metadata.get("SourceUrl", ''),
            #         "TargetUrls": metadata.get("TargetUrls", []),
            #         "TaskIds": metadata.get("TaskIds", []),
            #         "CallbackUrl": metadata.get("CallbackUrl", ''),
            #         "StreamHandlerStart": metadata.get("StreamHandlerStart", 0),
            #         "StreamHandlerDuration": metadata.get("StreamHandlerDuration", 0),
            #         "FailureRetryTimes": metadata.get("FailureRetryTimes", 0),
            #         "StreamIdleTimeout": metadata.get("StreamIdleTimeout", 0),
            #         "StreamBrokenSleepInterval": metadata.get("StreamBrokenSleepInterval", 0),
            #     },
            #     "CreateTime": None
            # }

            # create_push_live_inputs = {
            #     'JobName': StringModule(name='JobName', data=data.get('JobName', '')),
            #     'SourceType': StringModule(name='SourceType', data=data.get('SourceType', ''),
            #                                option=self._source_type_validate),
            #     'SourceUrl': StringModule(name='SourceUrl', data=data.get('SourceUrl', '')),
            #     'CallbackUrl': StringModule(name='CallbackUrl', data=data.get('CallbackUrl', '')),
            #     'Outputs': ObjectIterableModule(name='Outputs', data={
            #         'Type': StringModule(name='Type', data=data.get('Outputs', {}).get('Type', ''),
            #                              option=self._type_validate),
            #         'TargetUrls': ListModule(name='TargetUrls', data=data.get('Outputs', {}).get('TargetUrls', [])),
            #         'StartLive': IntModule(name='StartLive', data=data.get('Outputs', {}).get('StartLive', 0),
            #                                empty=True),
            #         'Duration': IntModule(name='Duration', data=data.get('Outputs', {}).get('Duration', 0),
            #                               empty=True)
            #     }),
            #     'StreamBrokenSleepInterval': IntModule(name='StreamBrokenSleepInterval',
            #                                            data=data.get('StreamBrokenSleepInterval', None),
            #                                            null=True),
            #     'FailureRetryTimes': IntModule(name='FailureRetryTimes',
            #                                    data=data.get('FailureRetryTimes', None),
            #                                    null=True),
            #     'StreamIdleTimeout': IntModule(name='StreamIdleTimeout',
            #                                    data=data.get('StreamIdleTimeout', None),
            #                                    null=True),
            # }

            job_data = self.describe_live_job(describe_job_data)
            create_task_inputs = {
                'Data': {
                    'JobName': job_data['JobName'],
                    'JobId': job_data['JobId'],
                    'SourceType': job_data['JobDetail']['SourceType'],
                    'SourceUrl': job_data['JobDetail']['SourceUrl'],
                    'CallbackUrl': job_data['JobDetail']['CallbackUrl'],
                    'Outputs': {
                        'Type': 'rtmp',
                        'TargetUrls': job_data['JobDetail']['TargetUrls'],
                        'StartLive': job_data['JobDetail']['StreamHandlerStart'],
                        'Duration': job_data['JobDetail']['StreamHandlerDuration']
                    },
                    'StreamBrokenSleepInterval': job_data['JobDetail']['StreamBrokenSleepInterval'],
                    'FailureRetryTimes': job_data['JobDetail']['FailureRetryTimes'],
                    'StreamIdleTimeout': job_data['JobDetail']['StreamIdleTimeout']
                }
            }

            create_push_live_task = CreateLivePullStreamTaskWorker(create_task_inputs)
            # 开启任务
            create_push_live_task()
            # 删除触发器
            self.delete_timer(
                job_name=job_data['JobName'],
                preset_time=job_data['JobDetail']['PresetStartTime'])

        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def describe_live_job(self, describe_job_data):
        job_id = describe_job_data['JobId']
        job_data = self.redis_client.get(key=job_identifier(job_id=job_id))['data']

        if not job_data:
            raise ResourceNotFoundJob()
        else:
            job_data = json.loads(job_data)

        return job_data

    def delete_timer(self, job_name, preset_time):
        worker_params = {
            'FunctionName': 'livestream_dispatch',
            'Namespace': os.environ.get('WorkerNameSpace'),
            'Type': 'timer',
            'TriggerName': '{name}_{time}'.format(name=job_name, time=str(preset_time)),
        }

        resp = qcloud_caller('DeleteTrigger', worker_params)
        return resp

