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




is it even there?
=================

.. autofunction:: openrem.remapp.netdicom.sample.my_func_that_return_parser

argparse
========

.. argparse::
   :module: openrem.remapp.netdicom.qrscu
   :func: _process_args
   :prog: qrscu
