# -*- coding: utf-8 -*-
import traceback


class BaseWorker:

    def __call__(self):
        try:
            self.main_handler()
        except Exception as e:
            print(traceback.format_exc())
            return
        finally:
            return

    def main_handler(self):
        pass

