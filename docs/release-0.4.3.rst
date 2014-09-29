OpenREM Release Notes version 0.4.3
***********************************

Headline changes
================


* Export of study information is now handled by a task queue - no more export time-outs.
* Patient size information in csv files can now be uploaded and imported via a web interface.
* Proprietary projection image object created by Hologic tomography units can now be interrogated for details of the tomosynthesis exam.
* Settings.py now ships with its proper name, this will overwrite important local settings if upgrade is from 0.3.9 or earlier.
* Time since last study is no longer wrong just because of daylight saving time!
* Django release set to 1.6; OpenREM isn't ready for Django 1.7 yet
* The inner `openrem` Django project folder is now called `openremproject` to avoid import conflicts with Celery on Windows

Specific upgrade instructions
=============================

**Always make sure you have converted your database to South before attempting an upgrade**

Quick reminder of how, if you haven't done it already:

    Linux::

        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp

    Windows::

        python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp

Upgrading from 0.3.9 or earlier
-------------------------------

**It is essential that you upgrade to at least 0.4.0 first**, then upgrade to
0.4.3. Otherwise the settings file will be overwritten and you will lose
your database settings. There is also a trickier than usual database
migration and instructions for setting up users. *Fresh installs should start
with the latest version.*

Upgrade to version 0.4.2

.. sourcecode:: bash

    pip install openrem==0.4.2

(Will need ``sudo`` or equivalent if using linux without a virtualenv)

Then follow the instructions in :doc:`release-0.4.0` from migrating the
database onwards, before coming back to these instructions.


Upgrading from 0.4.0 or above
-----------------------------

Install OpenREM version 0.4.3
`````````````````````````````
.. sourcecode:: bash

    pip install --pre openrem==0.4.3b7

(Will need ``sudo`` or equivalent if using linux without a virtualenv)

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

The ``local_settings.py`` file will be in the ``openrem/openremproject`` folder, for example:

* Linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Linux with virtualenv: ``/home/myname/openrem/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``

The path set for ``MEDIA_ROOT`` is up to you, but the user that runs the
webserver must have read/write access to the location specified because
it is the webserver than reads and writes the files. In a debian linux,
this is likely to be ``www-data`` for a production install. Remember to use
forward slashes in the config file, even for Windows.

Linux example::

    MEDIA_ROOT = "/var/openrem/media/"

Windows example::

    MEDIA_ROOT = "C:/Users/myusername/Documents/OpenREM/media/"

Database migration
``````````````````
*Assuming no virtualenv*

Linux::

    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp

Windows::

    C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
    C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

Web server
``````````

Restart the web server.

Start the Celery task queue
```````````````````````````
..  Note::

    The webserver and Celery both need to be able to read and write to the
    ``MEDIA_ROOT`` location. Therefore you might wish to consider starting
    Celery using the same user or group as the webserver, and setting the
    file permissions accordingly.

For testing, in a new shell: *(assuming no virtualenv)*

Linux::

    cd /usr/local/lib/python2.7/dist-packages/openrem/
    celery -A openremproject worker -l info

Windows::

    cd C:\Python27\Lib\site-packages\openrem\
    celery -A openremproject worker -l info

For production use, see http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html

