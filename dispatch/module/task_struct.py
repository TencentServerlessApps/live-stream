# -*- coding: utf-8 -*-

import json
import datetime

from etc.config import JobOfRealTime
from workplace.lib.tools import task_identifier, job_identifier


class JobStruct:

    def __init__(self, metadata, data_sync_client, is_init_from_db=False):
        self.job_id = metadata.get("JobId")
        self.sync_client = data_sync_client
        self.stream_handler_offset = 0
        self.create_time = metadata.get('CreateTime', None)
        if not is_init_from_db:
            self.struct = {
                "JobName": metadata.get("JobName", None),
                "JobId": metadata.get("JobId", None),
                "JobType": metadata.get("JobType", JobOfRealTime),
                "JobDetail": {
                    "PresetStartTime": metadata.get("PresetStartTime", ''),
                    "StartLive": metadata.get("StartLive", 0),
                    "SourceType": metadata.get("SourceType", ''),
                    "SourceUrl": metadata.get("SourceUrl", ''),
                    "TargetUrls": metadata.get("TargetUrls", []),
                    "TaskIds": metadata.get("TaskIds", []),
                    "CallbackUrl": metadata.get("CallbackUrl", ''),
                    "StreamHandlerStart": metadata.get("StreamHandlerStart", 0),
                    "StreamHandlerDuration": metadata.get("StreamHandlerDuration", 0),
                    "FailureRetryTimes": metadata.get("FailureRetryTimes", 0),
                    "StreamIdleTimeout": metadata.get("StreamIdleTimeout", 0),
                    "StreamBrokenSleepInterval": metadata.get("StreamBrokenSleepInterval", 0),
                },
                "CreateTime": None
            }
        else:
            self.struct = metadata

    def identifier(self):
        return job_identifier(job_id=self.job_id)

    def get(self, key):
        return self.struct['JobDetail'].get(key, None)

    def update(self, key, value):
        self.struct['JobDetail'][key] = value

    def data_sync(self):
        key = self.identifier()
        if self.struct['CreateTime'] is None:
            if self.create_time is None:
                self.struct['CreateTime'] = datetime.datetime.now() \
                    .strftime('%Y-%m-%d %H:%M:%S')
            else:
                date = datetime.datetime.fromtimestamp(self.create_time)
                self.struct['CreateTime'] = date.strftime('%Y-%m-%d %H:%M:%S')

        data = json.dumps(self.struct)
        self.sync_client.set(key, data)

    def delete(self):
        key = self.identifier()
        self.sync_client.delete(key)


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
                "SourceUrl": metadata.get("SourceUrl", None),
                "TargetUrl": metadata.get("TargetUrl", None),
                "CallbackUrl": metadata.get("CallbackUrl", None),
                "TaskStartTime": metadata.get("StartTime", None),
                "TaskPausedTime": metadata.get("PausedTime", None),
                "TaskFinishTime": metadata.get("FinishTime", None),
                "Status": metadata.get("Status", None),
                "StreamHandlerStart": metadata.get("StreamHandlerStart", 0),
                "StreamHandlerDuration": metadata.get("StreamHandlerDuration", 0),
                "ErrorMessage": metadata.get("ErrorMessage", ''),
                "LastUpdateTime": ''
            }
        else:
            pass

    def identifier(self):
        return task_identifier(task_id=self.task_id)

    def get(self, key):
        return self.struct.get(key, None)

    def update(self, key, value):
        self.struct[key] = value

    def data_sync(self):
        key = self.identifier()
        self.struct['LastUpdateTime'] = datetime.datetime.now() \
            .strftime('%Y-%m-%d %H:%M:%S')

        data = json.dumps(self.struct)
        self.sync_client.set(key, data)


if __name__ == "__main__":
    metadata = {
                "JobId": "JobId",
                "TaskId": "TaskId",
                "RequestId": "RequestId",
                "SourceType": "SourceType",
                "SourceUrl": "SourceUrl",
                "TargetUrl": "TargetUrl",
                "CallbackUrl": "CallbackUrl",
                "TaskStartTime": "StartTime",
                "TaskPausedTime": "PausedTime",
                "TaskFinishTime": "FinishTime",
                "Status": "Status",
                "StreamHandlerStart": "StreamHandlerStart",
                "StreamHandlerDuration": "StreamHandlerDuration",
                "ErrorMessage": "ErrorMessage",
                "LastUpdateTime": 123456
    }

    task_status = TaskStruct(metadata=metadata, data_sync_client=None)

    print(task_status.LastUpdateTime)


