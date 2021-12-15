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
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import uuid_generator, cron_descriptor, job_identifier
from module.request_module import DeletePresetStreamRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DeletePresetLivePullStreamTaskWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        delete_preset_stream_request = DeletePresetStreamRequest(data)
        delete_preset_stream_data = delete_preset_stream_request.get_value(is_common_check=True)

        try:
            self.delete_preset_live_stream(delete_preset_stream_data)

            response = {
            }
            return response

        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def delete_preset_live_stream(self, delete_preset_stream_data):

        job_id = delete_preset_stream_data['JobId']
        job_data = self.redis_client.get(key=job_identifier(job_id=job_id))['data']

        if not job_data:
            raise ResourceNotFoundJob()
        else:
            job_data = json.loads(job_data)
        job_name = job_data['JobName']
        preset_time = job_data['JobDetail']['PresetStartTime']
        self.redis_client.delete(list_of_key=[job_identifier(job_id=job_id)])
        self.redis_client.zrem(key=PushLiveJobsSet, list_of_value=[job_id])

        now = int(time.time())
        if now < int(preset_time):
            resp = self.delete_timer(job_name, preset_time)
            if not resp['success']:
                error_message = resp['err_msg']
                raise PresetCronTaskError(message=error_message)

    def delete_timer(self, job_name, preset_time):
        worker_params = {
            'FunctionName': os.environ.get('SCF_FUNCTIONNAME'),
            'Namespace': os.environ.get('SCF_NAMESPACE'),
            'Type': 'timer',
            'TriggerName': '{name}_{time}'.format(name=job_name, time=str(preset_time)),
        }

        resp = qcloud_caller('DeleteTrigger', worker_params)
        return resp

