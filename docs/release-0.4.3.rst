OpenREM Release Notes version 0.4.3
***********************************

Headline changes
================

* Export of study information is now handled by a task queue
* Patient size information in csv files can now be uploaded and imported via a web interface.
* Proprietary projection image object created by Hologic tomography units can now be interrogated for details of the tomosynthesis exam.
* Settings.py now ships with its proper name, this will overwrite important local settings if upgrade is from 0.3.9 or earlier.
* Time since last study is no longer wrong just because of daylight saving time!

Specific upgrade instructions
=============================

Upgrading from 0.4.0 or above
-----------------------------

The message broker RabbitMQ needs to be installed in addition to the usual upgrade steps:

* Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
* Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html

Then follow the :ref:`generic-upgrade-instructions`. A database migration is required.

*Add in instructions for local settings file*

Upgrading from 0.3.9 or earlier
-------------------------------

It is essential that you uprade to 0.4.0 first, then upgrade to 0.4.3. Otherwise the settings file
will be overwritten and you will lose your database settings.

Follow the instructions in :doc:`release-0.4.0`
