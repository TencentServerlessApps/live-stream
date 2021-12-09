# -*- coding -*-

import os
import json
import logging
import traceback
import threading

from etc.config import *
from error.errors import *
from module.redis_helper import RedisClient
from workplace.base_worker import BaseWorker
from workplace.lib.tools import job_identifier
from module.request_module import DescribeJobRequest, ListJobsRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DescribeJobWorker(BaseWorker):

    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        describe_job_request = DescribeJobRequest(data)
        describe_job_data = describe_job_request.get_value(is_common_check=True)

        try:
            job_data = self.describe_live_job(describe_job_data)

            return job_data

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


class ListJobsWorker(BaseWorker):
    def __init__(self, inputs):
        self.job_id = ''
        self.inputs = inputs
        self.task_map = {}
        self.redis_client = RedisClient()

    def main_handler(self):

        data = self.inputs.get('Data', {})
        list_jobs_request = ListJobsRequest(data)
        list_jobs_data = list_jobs_request.get_value(is_common_check=True)

        try:

            jobs_info = self.list_jobs(list_jobs_data)

            return {
                "JobsInfo": jobs_info
            }

        except BaseError as e:
            print(traceback.print_exc())
            return {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }

    def list_jobs(self, list_jobs_data):

        jobs_info = []
        start_time = list_jobs_data['StartTime']
        end_time = list_jobs_data['EndTime']
        if end_time <= start_time:
            raise NotSupportOperation(message='EndTime must be bigger then StartTime')

        jobs_data = self.redis_client.zrangbyscore(key=PushLiveJobsSet, min=start_time, max=end_time)['data']

        for item in jobs_data:
            jobs_info.append({
                'CreateTime': int(item[1]),
                'JobId': item[0]
            })

        return jobs_info


