OpenREM Release Notes version 0.4.3
***********************************

Headline changes
================

* Export of study information is now handled by a task queue - no more export time-outs.
* Patient size information in csv files can now be uploaded and imported via a web interface.
* Proprietary projection image object created by Hologic tomography units can now be interrogated for details of the tomosynthesis exam.
* Settings.py now ships with its proper name, this will overwrite important local settings if upgrade is from 0.3.9 or earlier.
* Time since last study is no longer wrong just because of daylight saving time!

Specific upgrade instructions
=============================

Upgrading from 0.4.0 or above
-----------------------------

* Install RabbitMQ
* Add the ``MEDIA_ROOT`` path to the ``local_settings.py``
* Then follow the :ref:`generic-upgrade-instructions`. A database migration is required.

RabbitMQ
````````

The message broker RabbitMQ needs to be installed to enable the export and upload features

* Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
* Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html

Edit the location setting for imports and exports in the local_settings.py file
```````````````````````````````````````````````````````````````````````````````

The ``MEDIA_ROOT`` path needs to be defined in the ``local_settings.py`` file. This is
the place where the study exports will be stored for download and where the
patient size information csv files will be stored temporarily whilst they
are bing processed.

The ``local_settings.py`` file will be in the ``openrem/openrem`` folder, for example:

* Linux: ``/usr/lib/python2.7/dist-packages/openrem/openrem/local_settings.py``
* Linux with virtualenv: ``/home/myname/openrem/lib/python2.7/site-packages/openrem/openrem/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openrem\local_settings.py``

The path set for ``MEDIA_ROOT`` is up to you, but the user that runs the
webserver must have read/write access to the location specified because
it is the webserver than reads and writes the files. In a debian linux,
this is likely to be ``www-data`` for a production install.




Upgrading from 0.3.9 or earlier
-------------------------------

It is essential that you upgrade to at least 0.4.2 first, then upgrade to
0.4.3. Otherwise the settings file will be overwritten and you will lose
your database settings. There is also a trickier than usual database
migration and instructions for setting up users.

*Instructions for upgrading to 0.4.3, something like* ``sudo pip install openrem==0.4.2``

Follow the instructions in :doc:`release-0.4.0`
