# -*- coding: utf-8 -*-

import json
import pprint
import requests

url = 'https://service-8gayt3pd-1253970226.sh.apigw.tencentcs.com/release/livestream_dispatch'

taskIds = []

for i in range(0, 100):
    taskIds.append(str(i))
print(len(taskIds))
data = {
    "Action": "RefreshLivePullStreamTask",
    "Data": {
        'TaskIdse': taskIds,
    }
}

resp = requests.post(url=url, data=json.dumps(data))
r = resp.json()
pprint.pprint(r)
print(len(r['Response']['TaskInfos']))


