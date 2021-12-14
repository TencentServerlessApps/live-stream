# coding:utf-8

import json
import os, stat
import traceback
import logging
from etc.config import *
from route.route import get_worker

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
    return {
        "Response": response_body,
    }


def main_handler(scf_event, scf_context):
    try:
        if scf_event == {}:
            pass  # 这里应该抛出异常，但是由于数据是从云API输入的所以数据不能是{}

        worker_type = scf_event.get('WorkType', None)
        worker = get_worker(worker_type, scf_event)

        if worker is None:
            raise
        os.chmod(ffmpeg_path, stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        before_api = worker.get('before')
        if before_api is not None and callable(before_api):
            before_api(scf_event)

        process_api = worker.get('process')
        if process_api is not None and callable(process_api):
            resp = process_api()

        after_api = worker.get('after')
        if after_api is not None and callable(after_api):
            after_api(scf_event, resp)

        return resp

    except Exception as e:
        print(traceback.format_exc())
