# -*- coding: utf-8 -*-

import os
from peewee import *
from playhouse.shortcuts import (dict_to_model, model_to_dict)
import traceback

try:
    _host = os.environ.get('mysql_host')
    _user = os.environ.get('mysql_user')
    _passwd = os.environ.get('mysql_pwd')
    _db = os.environ.get('mysql_dbName')
    _port = int(os.environ.get('mysql_port'))


    class MyRetryDB(MySQLDatabase):
        def execute_sql(self, sql, params=None, commit=object()):
            try:
                if not self.is_closed():
                    self.close()
                self.connect()
                cursor = super(MyRetryDB, self).execute_sql(sql, params, commit)
            except Exception as e:
                raise e
            return cursor


    database = MyRetryDB(_db,
                         host=_host,
                         port=_port,
                         user=_user,
                         password=_passwd,
                         charset='utf8')


    class BaseModel(Model):
        @classmethod
        def create_from_dict(cls, data):
            return dict_to_model(cls, data, ignore_unknown=True)

        def dict(self):
            return model_to_dict(self)

        class Meta:
            database = database
            only_save_dirty = True


    class TServerlessGrayscaleModuleInfo(BaseModel):

        appId = CharField()
        region = CharField()
        namespace = CharField()
        module = CharField()
        status = CharField()
        lastVersion = CharField()
        addTime = TimestampField()
        modTime = CharField()

        class Meta:
            db_table = 'serverless_grayscale_module_info'

except Exception as e:
    print(traceback.format_exc())
