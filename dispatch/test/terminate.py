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
    "Action": "TerminateLivePullStreamTask",
    "Data": {
        'TaskIds': ['de64a7a6-bcbe-44a1-8891-0b9ac841858b'],
    }
}

resp = requests.post(url=url, data=json.dumps(data))
r = resp.json()
pprint.pprint(r)
print(len(r['Response']['TaskInfos']))


