# -*- coding: utf-8 -*-

import os
import json
import traceback

from tencentcloud.common import credential
from tencentcloud.common.profile import client_profile
from tencentcloud.common.profile import http_profile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client


def qcloud_caller(action, call_params={}, req_timeout=5):
    secret_id = os.environ.get('SecretId')
    secret_key = os.environ.get('SecretKey')
    if secret_id:
        user_cred = credential.Credential(secret_id, secret_key)
    else:
        secret_id = os.getenv("TENCENTCLOUD_SECRETID")
        secret_key = os.getenv("TENCENTCLOUD_SECRETKEY")
        token = os.getenv("TENCENTCLOUD_SESSIONTOKEN")
        user_cred = credential.Credential(secret_id, secret_key, token)

    region = os.environ.get('WorkerRegion')

    result = {
        'success': True,
        'response': None,
        'err_msg': ''
    }

    try:
        # 强制限定超时时长
        hp = http_profile.HttpProfile(reqTimeout=req_timeout)
        hp.reqMethod = "POST"
        cp = client_profile.ClientProfile()
        cp.signMethod = "TC3-HMAC-SHA256"
        cp.httpProfile = hp
        client = scf_client.ScfClient(user_cred, region, profile=cp)
        resp = client.call(action, call_params)

        resp_format = json.loads(resp)
        print(resp_format)
        if 'Error' in resp_format['Response']:
            result['success'] = False

        result['response'] = resp_format['Response']
    except TencentCloudSDKException as e:
        print(traceback.format_exc())
        result['success'] = False
        result['err_msg'] = e.message
    finally:
        return result
