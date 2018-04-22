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




argparse
========

.. argparse::
   :module: openrem.remapp.netdicom.sample
   :func: my_func_that_return_parser
   :prog: openrem_qr.py

autoprogram
===========

.. autoprogram:: openrem.remapp.netdicom.sample:m_func_that_returns_parser
   :prog: sample.py