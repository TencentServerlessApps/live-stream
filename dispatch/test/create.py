# -*- coding: utf-8 -*-

import json
import requests

url = 'https://service-8gayt3pd-1253970226.sh.apigw.tencentcs.com/release/livestream_dispatch'

data = {
    "Action": "CreateLivePullStreamTask",
    "Data": {
        'JobName': 'test3',
        'CallbackUrl': 'dsafdsaf',
        'Outputs': {'Duration': 0,
                    'StartLive': 0,
                    'TargetUrls': ['rtmp://66679.livepush.myqcloud.com/live/new?txSecret=55545edb0399ea3ef2b17ca639585e3e&txTime=617E400F'],
                    'Type': 'rtmp'},
        'SourceType': 'PullVideoPushLive',
        'SourceUrl': 'https://chris-demo-test-1253970226.cos.ap-beijing.myqcloud.com/test.mp4'
    }
}

resp = requests.post(url=url, data=json.dumps(data))

print(resp.json())




