import logging
from celery import shared_task


@shared_task
def keep_alive():
    from remapp.models import DicomStoreSCP
    from remapp.netdicom.storescp import web_store
    from remapp.netdicom.tools import echoscu
    stores = DicomStoreSCP.objects.all()
    for store in stores:
        if store.keep_alive:
            echo = echoscu(scp_pk=store.pk, store_scp=True)
            logging.warning("echo is {0}".format(echo))
            if echo is "AssocFail":
                logging.warning("in not echo")
                store.run = True
                store.save()
                web_store.delay(store_pk=store.pk)
