# -*- coding: utf-8 -*-

import json
import pprint
import requests

url = 'https://service-8gayt3pd-1253970226.sh.apigw.tencentcs.com/release/livestream_dispatch'

taskIds = []

for i in range(0, 40):
    taskIds.append(str(i))
print(len(taskIds))
data = {
    "Action": "DeletePresetLivePullStreamTask",
    "Data": {
        'JobId': '6e07179c-e331-44eb-b02d-e030460addd9',
    }
}

resp = requests.post(url=url, data=json.dumps(data))
r = resp.json()
pprint.pprint(r)


