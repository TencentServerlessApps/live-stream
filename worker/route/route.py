# coding:utf-8

from workplace.business import RtmpToRtmpHandler, VodToRtmpHandler


def get_process_list(process, before=None, after=None):
    return {
        'before': before,
        'process': process,
        'after': after,
    }


WORKER_MAP = {
    'PullLivePushLive': RtmpToRtmpHandler,
    'PullVodPushLive': VodToRtmpHandler
}


def get_worker(worker_type, event):
    _worker = WORKER_MAP.get(worker_type)
    _process = get_process_list(_worker)
    _process['process'] = _process['process'](event)
    return _process
