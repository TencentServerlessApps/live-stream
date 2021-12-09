# -*- coding: utf-8 -*-

import uuid
import datetime

from etc.config import JobKey, TaskKey, EventQueue


def uuid_generator():
    return str(uuid.uuid4())


def job_identifier(job_id):
    return JobKey.format(job_id=job_id)


def task_identifier(task_id):
    return TaskKey.format(task_id=task_id)


def event_queue_identifier(task_id):
    return EventQueue.format(task_id=task_id)


def cron_descriptor(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    second = time.second
    minute = time.minute
    hour = time.hour
    day = time.day
    month = time.month
    week = '*'
    year = '*'

    cron = '{S} {M} {H} {d} {m} {w} {y}'.format(S=second, M=minute, H=hour, d=day, m=month, w=week, y=year)
    return cron


if __name__ == "__main__":
    import time
    print(cron_descriptor(int(time.time())))



