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
    "Action": "DescribeLivePullStreamJob",
    "Data": {
        'JobId': '957a92b8-72de-45a2-b467-ac1eb27209f4',
    }
}
resp = requests.post(url=url, data=json.dumps(data))
print(len(resp.text))
r = resp.json()
pprint.pprint(r)


