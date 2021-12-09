# coding:utf-8

from dispatch.workplace.create_live_pull_stream import CreateLivePullStreamTaskWorker
from workplace.terminate_live_pull_stream import TerminateLivePullStreamTaskWorker
from workplace.pause_live_pull_stream import PauseLivePullStreamTaskWorker
from workplace.resume_live_pull_stream import ResumeLivePullStreamTaskWorker
from workplace.refresh_live_pull_stream import RefreshLivePullStreamTaskWorker
from workplace.describe_live_pull_stream import DescribeLivePullStreamTaskWorker
from workplace.preset_live_pull_stream import CreatePresetLivePullStreamTaskWorker
from workplace.delete_preset_live_pull_stream import DeletePresetLivePullStreamTaskWorker
from workplace.describe_job import DescribeJobWorker, ListJobsWorker
from workplace.crontab_task import CronTaskWorker


def get_process_list(process, before=None, after=None):
    return {
        'before': before,
        'process': process,
        'after': after,
    }


WORKER_MAP = {
    'CreateLivePullStreamTask': CreateLivePullStreamTaskWorker,
    'TerminateLivePullStreamTask': TerminateLivePullStreamTaskWorker,
    'PauseLivePullStreamTask': PauseLivePullStreamTaskWorker,
    'ResumeLivePullStreamTask': ResumeLivePullStreamTaskWorker,
    'RefreshLivePullStreamTask': RefreshLivePullStreamTaskWorker,
    'DescribeLivePullStreamTask': DescribeLivePullStreamTaskWorker,

    'CreatePresetLivePullStreamTask': CreatePresetLivePullStreamTaskWorker,
    'DeletePresetLivePullStreamTask': DeletePresetLivePullStreamTaskWorker,
    'DescribeLivePullStreamJob': DescribeJobWorker,
    'ListLivePullStreamJob': ListJobsWorker,

    'CronTask': CronTaskWorker,
}


def get_worker(worker_type, event):
    _worker = WORKER_MAP.get(worker_type)
    _process = get_process_list(_worker)
    _process['process'] = _process['process'](event)
    return _process
