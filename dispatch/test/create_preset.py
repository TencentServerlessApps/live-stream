# -*- coding: utf-8 -*-

import json
import time
import requests

url = 'https://service-8gayt3pd-1253970226.sh.apigw.tencentcs.com/release/livestream_dispatch'

data = {
    "Action": "CreatePresetLivePullStreamTask",
    "Data": {
        'JobName': 'test_demo',
        'PresetStartTime': str(int(time.time()) + 60),
        'CallbackUrl': 'dsafdsaf',
        'Outputs': {'Duration': 0,
                    'StartLive': 0,
                    'TargetUrls': ['rtmp://66679.livepush.myqcloud.com/live/new?txSecret=954b8eef45004933d3d16afdbe7e093a&txTime=617E3E3B'],
                    'Type': 'rtmp'},
        'SourceType': 'PullVideoPushLive',
        'SourceUrl': 'https://chris-demo-test-1253970226.cos.ap-beijing.myqcloud.com/test.mp4'
    }
}
print(len(data['Data']['PresetStartTime']), data['Data']['PresetStartTime'])
resp = requests.post(url=url, data=json.dumps(data))

print(resp.json())




