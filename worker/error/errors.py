# -*- coding: utf-8 -*-


class BaseError(Exception):
    message = 'default'
    code = ''

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


class InternalError(BaseError):
    code = 'InternalError'
    message = '服务处理出错，请稍后重试。若无法解决，请联系智能客服或提交工单。'


class ResourceNotFoundTask(BaseError):
    code = 'ResourceNotFound.Task'
    message = 'The specified task was not found'


class InternalErrorWithRedis(BaseError):
    code = 'InternalError.Redis'
    message = 'Database access error'


if __name__ == "__main__":
    try:
        raise ResourceNotFoundTask()
    except Exception as e:
        print(e.message)