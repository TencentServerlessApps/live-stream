# -*- coding: utf-8 -*-

import os
import json
import logging
import traceback
import threading

from etc.config import *
from error.errors import BaseError, ResourceNotFoundTask
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import task_identifier
from workplace.lib.tools import uuid_generator
from module.request_module import DescribeStreamRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DescribeLivePullStreamTaskWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        describe_stream_request = DescribeStreamRequest(data)
        describe_stream_data = describe_stream_request.get_value(is_common_check=True)

        task_ids = describe_stream_data['TaskIds']
        try:
            # 多线程分发任务，确保快速拉起转推任务
            unit_count = self.worker_estimate(task_ids)
            worker_list = []
            while True:
                if len(task_ids) == 0:
                    break
                task_list = []
                for i in range(unit_count):
                    if len(task_ids) > 0:
                        task_id = task_ids.pop(-1)
                    else:
                        break
                    task_list.append(task_id)
                    self.task_map[task_id] = {}
                stream_worker = threading.Thread(target=self.describe_live_stream,
                                                 args=(describe_stream_data, task_list,))
                worker_list.append(stream_worker)

            for task in worker_list:
                task.start()

            for task in worker_list:
                task.join()

            task_info = []
            for k, v in self.task_map.items():
                task_info.append(v)

            response = {
                "TaskInfos": task_info,
            }
            return response

        except Exception as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': 'InternalError',
                'ErrorMessage': 'InternalError',
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

    def describe_live_stream(self, describe_stream_data, task_list):
        
        for task_id in task_list:
            task_key = task_identifier(task_id)
            try:
                task_data = self.redis_client.get(task_key)['data']

                if not task_data:
                    raise ResourceNotFoundTask()
                else:
                    task_data = json.loads(task_data)
                    status = task_data['Status']

                self.task_map[task_id] = {
                    "TargetUrl": task_data['TargetUrl'],
                    "TaskId": task_id,
                    "Status": status,
                    "Error": task_data.get('ErrorMessage', '')
                }

            except BaseError as e:
                print(traceback.print_exc())
                self.task_map[task_id] = {
                    "TargetUrl": "",
                    "TaskId": task_id,
                    "Status": "",
                    "Error": e.message
                }



