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
            logging.info("Keep_alive echo for {0} is {1}".format(store.aetitle, echo))
            if echo is "AssocFail":
                logging.warning("Starting {0} on port {1} due to Association Request failure.".format(store.aetitle, store.port))
                store.status = "Store not running, but keep-alive is set!"
                store.save()
                web_store.delay(store_pk=store.pk)
