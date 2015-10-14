import logging
from celery import shared_task

@shared_task
def alive_example(a, b):

    logging.warning("Answer is still {0}".format(a+b))