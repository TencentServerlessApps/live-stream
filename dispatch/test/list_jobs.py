# -*- coding: utf-8 -*-

import json
import time
import pprint
import requests

url = 'https://service-8gayt3pd-1253970226.sh.apigw.tencentcs.com/release/livestream_dispatch'

taskIds = []

for i in range(0, 40):
    taskIds.append(str(i))
print(len(taskIds))
now = int(time.time())
data = {
    "Action": "ListLivePullStreamJob",
    "Data": {
        'StartTime': now - (31 * 86400),
        'EndTime': now
    }
}
resp = requests.post(url=url, data=json.dumps(data))
print(len(resp.text))
r = resp.json()
pprint.pprint(r)