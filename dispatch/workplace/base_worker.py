# -*- coding: utf-8 -*-
import traceback


class BaseWorker:

    def __call__(self):
        response = {
            'Response': None
        }
        try:
            result = self.main_handler()
            response['Response'] = result
        except Exception as e:
            print(traceback.format_exc())
            response['Response'] = {
                'ErrorCode': e.code,
                'ErrorMessage': e.message,
            }
        finally:
            return response

    def main_handler(self):
        pass

