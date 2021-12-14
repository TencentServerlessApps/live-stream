# coding:utf-8

import json
import time
import traceback
import logging

from route.route import get_worker

time.tzset()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def render_response(data=None, err=None, request_id=None):
    if not data:
        data = {}

    if err:
        response_body = data
        response_body["Error"] = {
            "Code": err.code,
            "Message": "{0}".format(err.message),
        }
    else:
        response_body = data
    if "RequestId" not in response_body:
        response_body["RequestId"] = request_id
    return response_body


def main_handler(scf_event, scf_context):
    request_id = scf_context.get('request_id', None)
    try:
        req_source = scf_event.get('Type', 'None')
        if req_source == 'Timer':
            data_raw = {
                'Action': 'CronTask',
                'Data': {
                    'JobId': json.loads(scf_event['Message'])['JobId']
                }
            }
        else:
            data_raw = json.loads(scf_event.get('body', '{}'))
            logger.info("inputs data_raw:"+ str(data_raw))
            if data_raw == {}:
                pass  # 这里应该抛出异常，但是由于数据是从云API输入的所以数据不能是{}

        worker_type = data_raw.get('Action', '')
        worker = get_worker(worker_type, data_raw)

        if worker is None:
            raise

        before_api = worker.get('before')
        if before_api is not None and \
                callable(before_api):
            before_api(data_raw)

        process_api = worker.get('process')
        if process_api is not None and \
                callable(process_api):
            resp = process_api()

        after_api = worker.get('after')
        if after_api is not None and \
                callable(after_api):
            after_api(data_raw, resp)

        return render_response(data=resp, request_id=request_id)

    except Exception as e:
        print(traceback.format_exc())
