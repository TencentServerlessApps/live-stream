# -*- coding: utf-8 -*-

import os
import json
import traceback

from etc.config import YUN_API_SLEEP, APPID_2_TEAM

from tencentcloud.common import credential
from tencentcloud.common.profile import client_profile
from tencentcloud.common.profile import http_profile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client


def call_yun_api(action, app_id, region='ap-guangzhou', params={}):

    team = APPID_2_TEAM[app_id]
    secret_id = os.environ.get(team + '_' + 'secret_id')
    secret_key = os.environ.get(team + '_' + 'secret_key')

    call_params = params
    result = {
        'success': True,
        'response': None
    }

    try:
        user_cred = credential.Credential(secret_id, secret_key)
        # 强制限定超时时长
        hp = http_profile.HttpProfile(reqTimeout=YUN_API_SLEEP)
        hp.reqMethod = "POST"
        cp = client_profile.ClientProfile()
        cp.signMethod = "TC3-HMAC-SHA256"
        cp.httpProfile = hp
        client = scf_client.ScfClient(user_cred, region, profile=cp)
        resp = client.call(action, call_params)

        resp_format = json.loads(resp)

        if 'Error' in resp_format['Response']:
            result['success'] = False

        result['response'] = resp_format['Response']
    except TencentCloudSDKException as e:
        print(traceback.format_exc())
        result['success'] = False
    finally:
        return result
