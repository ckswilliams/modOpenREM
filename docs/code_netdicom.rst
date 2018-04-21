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


Command line script
===================

..  autofunction:: openrem.remapp.netdicom.qrscu.qrscu_script

With the args parsed by:

..  autofunction:: openrem.remapp.netdicom.qrscu.parse_args


As program output
=================

..  program-output:: openrem_qr.py -h

..  program-output:: openrem_rdsr.py

..  program-output:: python -V


argparse
========

..  autoprogram:: openrem.remapp.netdicom.qrscu:parse_args
    :prog: qrscu