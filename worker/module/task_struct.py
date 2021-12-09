# -*- coding: utf-8 -*-

import json
import datetime

from etc.config import TaskKey


class TaskStruct:

    def __init__(self, metadata, data_sync_client, is_init_from_db=False):
        self.task_id = metadata.get("TaskId")
        self.sync_client = data_sync_client
        self.stream_handler_offset = 0
        if not is_init_from_db:
            self.struct = {
                "JobId": metadata.get("JobId", None),
                "TaskId": metadata.get("TaskId", None),
                "RequestId": metadata.get("RequestId", None),
                "SourceType": metadata.get("SourceType", None),
                "Loop": metadata.get("Loop", 1),
                "SourceUrls": metadata.get("SourceUrls", None),
                "SourceUrl": metadata.get("SourceUrl", None),
                "TargetUrl": metadata.get("TargetUrl", None),
                "CallbackUrl": metadata.get("CallbackUrl", None),
                "TaskStartTime": metadata.get("StartTime", None),
                "TaskPausedTime": metadata.get("PausedTime", None),
                "TaskFinishTime": metadata.get("FinishTime", None),
                "Status": metadata.get("Status", None),
                "StreamHandlerStart": int(metadata.get("StreamHandlerStart", 0)),
                "StreamHandlerDuration": int(metadata.get("StreamHandlerDuration", 0)),
                "ErrorMessage": metadata.get("ErrorMessage", ''),
                "LastUpdateTime": ''
            }
        else:
            pass

    def identifier(self):
        return TaskKey.format(task_id=self.task_id)

    def get(self, key):
        return self.struct.get(key, None)

    def update(self, key, value):
        self.struct[key] = value

    def sync_from_db(self):
        pass

    def save(self):
        key = self.identifier()
        self.struct['LastUpdateTime'] = datetime.datetime.now()\
            .strftime('%Y-%m-%d %H:%M:%S')

        data = json.dumps(self.struct)
        self.sync_client.set(key, data)

