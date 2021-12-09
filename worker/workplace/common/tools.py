# -*- coding: utf-8 -*-

import uuid

from etc.config import TaskKey, EventQueue


def uuid_generator():
    return uuid.uuid4()


def task_identifier(task_id):
    return TaskKey.format(task_id=task_id)


def event_queue_identifier(task_id):
    return EventQueue.format(task_id=task_id)


def time_to_num(time_str):
    h, m, s = time_str.split(':')
    return int(float(h) * 60 * 60 + float(m) * 60 + float(s))

