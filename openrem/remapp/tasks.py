from __future__ import absolute_import

from celery import shared_task

from celery import task, current_task
from time import sleep


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def do_work():
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(100):
        sleep(0.1)
        print i
        current_task.update_state(state='PROGRESS',
            meta={'process_percent': i})

from remapp.exports.exportcsv import exportCT2excel
