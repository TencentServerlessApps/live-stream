# -*- coding: utf-8 -*-

from peewee import SQL

from .models import TServerlessGrayscaleModuleInfo


def create_module_data(appId, region, namespace, module, status, lastVersion):
    TServerlessGrayscaleModuleInfo.insert(**{
        'appId': appId,
        'region': region,
        'namespace': namespace,
        'module': module,
        'status': status,
        'lastVersion': lastVersion,
        "addTime": SQL("CURRENT_TIMESTAMP"),
        "modTime": SQL("CURRENT_TIMESTAMP"),
    }).execute()


def update_module_data(appId, region, namespace, module, change={}):
    cond = [
        TServerlessGrayscaleModuleInfo.appId == appId,
        TServerlessGrayscaleModuleInfo.region == region,
        TServerlessGrayscaleModuleInfo.namespace == namespace,
        TServerlessGrayscaleModuleInfo.module == module
    ]

    return TServerlessGrayscaleModuleInfo.update(change).where(*cond).execute()


def select_module_data(appId, region, namespace, module):
    for info in TServerlessGrayscaleModuleInfo.select().where(*[
        TServerlessGrayscaleModuleInfo.appId == appId,
        TServerlessGrayscaleModuleInfo.region == region,
        TServerlessGrayscaleModuleInfo.namespace == namespace,
        TServerlessGrayscaleModuleInfo.module == module
    ]).dicts():
        data = {
            'appId': info['appId'],
            'region': info['region'],
            'namespace': info['namespace'],
            'module': info['module'],
            'status': info['status'],
            'lastVersion': info['lastVersion']
        }
        return data
    return None

