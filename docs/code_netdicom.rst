########################
DICOM networking modules
########################

*********************
Query-retrieve module
*********************

Query function
==============

..  autotask:: openrem.remapp.netdicom.qrscu.qrscu

Move function
=============

..  autotask:: openrem.remapp.netdicom.qrscu.movescu

openrem_qr.py script
====================

..  argparse::
    :module: openrem.remapp.netdicom.qrscu
    :func: _create_parser
    :prog: openrem_qr.py

*******************************
Alternative documentation style
*******************************

..  method:: qrscu(
    qr_scp_pk=None, store_scp_pk=None,
    implicit=False, explicit=False, move=False, query_id=None,
    date_from=None, date_until=None, modalities=None, inc_sr=False, remove_duplicates=True, filters=None,
    get_toshiba_images=False,
    *args, **kwargs):

    Queries a pre-configured remote query retrieve service class provider for dose metric related objects,
    making use of the filter parameters provided. Can automatically trigger a c-move (retrieve) operation.