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
    "Action": "DescribeLivePullStreamTask",
    "Data": {
        'TaskIds': ['85df03ed-ae29-47d0-be7e-5979ae44aaa4'],
    }
}

resp = requests.post(url=url, data=json.dumps(data))
r = resp.json()
pprint.pprint(r)
print(len(r['Response']['TaskInfos']))


