# -*- coding: utf-8 -*-

import re
import time

from etc.config import *
from module.validate import *


class RequestBaseMethod:

    def __init__(self, data):
        self.request_data = data

    def common_check(self):
        try:
            self.request_data.check()
        except Exception as e:
            raise e

    def get_value(self, is_common_check=False):
        if is_common_check:
            self.common_check()
        return self.request_data.value


class CreateStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'JobName': StringModule(name='JobName', data=data.get('JobName', '')),
            'JobId': StringModule(name='JobId', data=data.get('JobId', ''), empty=True),
            'SourceType': StringModule(name='SourceType', data=data.get('SourceType', ''),
                                       option=self._source_type_validate),
            'SourceUrl': StringModule(name='SourceUrl', data=data.get('SourceUrl', None), null=True),
            'SourceUrls': ListModule(name='SourceUrls', data=data.get('SourceUrls', []), null=True),
            'Loop': IntModule(name='Loop', data=data.get('Loop', 1), null=True),
            'CallbackUrl': StringModule(name='CallbackUrl', data=data.get('CallbackUrl', '')),
            'Outputs': ObjectIterableModule(name='Outputs', data={
                'Type': StringModule(name='Type', data=data.get('Outputs', {}).get('Type', ''),
                                     option=self._type_validate),
                'TargetUrls': ListModule(name='TargetUrls', data=data.get('Outputs', {}).get('TargetUrls', [])),
                'StartLive': IntModule(name='StartLive', data=data.get('Outputs', {}).get('StartLive', 0),
                                       empty=True, option=self._start_live_validate),
                'Duration': IntModule(name='Duration', data=data.get('Outputs', {}).get('Duration', 0),
                                      empty=True, option=self._duration_validate)
            }),
            'StreamBrokenSleepInterval': IntModule(name='StreamBrokenSleepInterval',
                                                   data=data.get('StreamBrokenSleepInterval', 10),
                                                   null=True),
            'FailureRetryTimes': IntModule(name='FailureRetryTimes',
                                           data=data.get('FailureRetryTimes', 3),
                                           null=True),
            'StreamIdleTimeout': IntModule(name='StreamIdleTimeout',
                                           data=data.get('StreamIdleTimeout', 30),
                                           null=True),
        }
        self.request_data = ObjectIterableModule(name='data', data=inputs, is_copy=True)

    @staticmethod
    def _start_live_validate(key, data):
        if data < 0:
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)

    @staticmethod
    def _duration_validate(key, data):
        if data < 0:
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)

    @staticmethod
    def _type_validate(key, data):
        if data != 'rtmp':
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)

    @staticmethod
    def _target_url_validate(key, data):
        if len(data) > StreamMax or len(data) == 0:
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)

    @staticmethod
    def _source_type_validate(key, data):
        if data not in ['PullLivePushLive', 'PullVideoPushLive']:
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)


class CreatePresetStreamRequest(CreateStreamRequest):

    def __init__(self, data):
        inputs = {
            'JobName': StringModule(name='JobName', data=data.get('JobName', '')),
            'SourceType': StringModule(name='SourceType', data=data.get('SourceType', ''),
                                       option=self._source_type_validate),
            'SourceUrl': StringModule(name='SourceUrl', data=data.get('SourceUrl', '')),
            'SourceUrls': ListModule(name='SourceUrls', data=data.get('SourceUrls', []), null=True),
            'Loop': IntModule(name='Loop', data=data.get('Loop', 1), null=True),
            'CallbackUrl': StringModule(name='CallbackUrl', data=data.get('CallbackUrl', '')),
            'Outputs': ObjectIterableModule(name='Outputs', data={
                'Type': StringModule(name='Type', data=data.get('Outputs', {}).get('Type', ''),
                                     option=self._type_validate),
                'TargetUrls': ListModule(name='TargetUrls', data=data.get('Outputs', {}).get('TargetUrls', [])),
                'StartLive': IntModule(name='StartLive', data=data.get('Outputs', {}).get('StartLive', 0),
                                       empty=True, option=self._start_live_validate),
                'Duration': IntModule(name='Duration', data=data.get('Outputs', {}).get('Duration', 0),
                                      empty=True, option=self._duration_validate)
            }),
            'PresetStartTime': StringModule(name='PresetStartTime', data=data.get('PresetStartTime', ''),
                                         option=self._preset_validate),
            'StreamBrokenSleepInterval': IntModule(name='StreamBrokenSleepInterval',
                                                   data=data.get('StreamBrokenSleepInterval', None),
                                                   null=True),
            'FailureRetryTimes': IntModule(name='FailureRetryTimes',
                                           data=data.get('FailureRetryTimes', None),
                                           null=True),
            'StreamIdleTimeout': IntModule(name='StreamIdleTimeout',
                                           data=data.get('StreamIdleTimeout', None),
                                           null=True),
        }
        self.request_data = ObjectIterableModule(name='data', data=inputs, is_copy=True)

    @staticmethod
    def _preset_validate(key, data):
        code = 'InvalidParameter.{key}'.format(key=key)
        message = 'The parameter {key} do not match the specification'.format(key=key)
        if re.search(r'^\d{1,10}$', data) is None:
            raise BaseError(code=code, message=message)

        if int(time.time()) >= int(data):
            raise BaseError(code=code, message=message)


class DeletePresetStreamRequest(RequestBaseMethod):
    def __init__(self, data):
        inputs = {
            'JobId': StringModule(name='JobId',
                                  data=data.get('JobId', ''))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class DescribeJobRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'JobId': StringModule(name='JobId',
                                  data=data.get('JobId', ''))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class ListJobsRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'StartTime': IntModule(name='StartTime',
                                   data=data.get('StartTime', 0)),
            'EndTime': IntModule(name='EndTime',
                                 data=data.get('EndTime', 0))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)

    @staticmethod
    def _start_time_validate(key, data):
        now = int(time.time())
        if (data + 30 * 86400) < now:
            code = 'InvalidParameter.{key}'.format(key=key)
            message = 'The parameter {key} do not match the specification'.format(key=key)
            raise BaseError(code=code, message=message)


class DescribeStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'TaskIds': ListModule(name='TaskIds',
                                  data=data.get('TaskIds', []))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class TerminateStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'TaskIds': ListModule(name='TaskIds',
                                  data=data.get('TaskIds', []))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class PauseStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'TaskIds': ListModule(name='TaskIds',
                                  data=data.get('TaskIds', []))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class ResumeStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'TaskIds': ListModule(name='TaskIds',
                                  data=data.get('TaskIds', []))
        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


class RefreshStreamRequest(RequestBaseMethod):

    def __init__(self, data):
        inputs = {
            'StartLive': IntModule(name='StartLive',
                                   data=data.get('Outputs', {}).get('StartLive', 0),
                                   empty=True),
            'Duration': IntModule(name='Duration',
                                  data=data.get('Outputs', {}).get('Duration', 0),
                                  empty=True),
            'TaskIds': ListModule(name='TaskIds', data=data.get('TaskIds', []))

        }
        self.request_data = ObjectIterableModule(name='data',
                                                 data=inputs, is_copy=True)


if __name__ == "__main__":
    import pprint
    c = CreateStreamRequest(data={
        'JobName': 'dd',
        'SourceType': 'PullVideoPushLive',
        'SourceUrl': 'sadfdsaf',
        'CallbackUrl': 'dsafdsaf',
        'Outputs': {
            'Type': 'rtmp',
            'TargetUrls': ['xxx'],
        },
        'PresetStartTime': '1635342275',
        'StreamBrokenSleepInterval': None,
        'FailureRetryTimes': None,
        'StreamIdleTimeout': None,
    })

    c.common_check()
    pprint.pprint(c.get_value())

    c1 = DescribeJobRequest(data={
        'JobId': '',
    })

    c1.common_check()
    pprint.pprint(c1.get_value())

    import time

    s = int(time.time())
    print(s)
    print('re', re.search(r'^\d{1,10}$', str(s)))


