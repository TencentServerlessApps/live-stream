# -*- coding: utf-8 -*-


class BaseError(Exception):
    message = 'internal error'
    code = 'InternalError'

    def __init__(self, code=None, message=None):
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message
        Exception.__init__(self, self.code, self.message)

    def __str__(self):
        return self.message


class ParameterError(BaseError):
    code = 'ParameterError'
    message = '''参数与规范不符'''


class InvalidParameter(BaseError):
    code = 'InvalidParameter'
    message = ''


class InternalError(BaseError):
    code = 'InternalError'
    message = 'Service processing error, please try again later. If it cannot be resolved, please contact us'


class InvokeWorkerError(BaseError):
    code = 'InvokeWorkerError'
    message = 'Invoke worker failed'


class PresetCronTaskError(BaseError):
    code = 'PresetCronError'
    message = 'Preset cron task error'


class ResourceNotFoundTask(BaseError):
    code = 'ResourceNotFound.Task'
    message = 'The specified task was not found'


class ResourceNotFoundJob(BaseError):
    code = 'ResourceNotFound.Job'
    message = 'The specified job was not found'


class TaskPausedStatusError(BaseError):
    code = 'TaskStatusChangeError.Paused'
    message = 'Paused failed, task status not in Running'


class TaskResumeStatusError(BaseError):
    code = 'TaskStatusChangeError.Resume'
    message = 'Paused failed, task status not in Paused'


class TaskRefreshStatusError(BaseError):
    code = 'TaskStatusChangeError.Refresh'
    message = 'Paused failed, task status not in Running'


class NotSupportActionError(BaseError):
    code = 'NotSupportActionError.PushLiveToLive'
    message = 'The source file protocol type does not support the operation'


class InternalErrorWithRedis(BaseError):
    code = 'InternalError.Redis'
    message = 'Database access error'


class NotSupportOperation(BaseError):
    code = 'NotSupportOperation'
    message = 'not support operation'
