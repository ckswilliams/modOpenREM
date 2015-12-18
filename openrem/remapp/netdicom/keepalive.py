import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name='remapp.netdicom.keepalive.keep_alive')
def keep_alive():
    from remapp.models import DicomStoreSCP
    from remapp.netdicom.storescp import web_store
    from remapp.netdicom.tools import echoscu
    stores = DicomStoreSCP.objects.all()
    for store in stores:
        if store.keep_alive:
            echo = echoscu(scp_pk=store.pk, store_scp=True)
            logger.debug("Keep_alive echo for {0} is {1}".format(store.aetitle, echo))
            if echo is "AssocFail":
                logger.warning("Starting {0} on port {1} due to Association Request failure.".format(store.aetitle, store.port))
                store.status = "Store not running, but keep-alive is set!"
                store.save()
                web_store(store_pk=store.pk)
