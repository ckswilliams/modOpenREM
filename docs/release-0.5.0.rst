OpenREM Release Notes version 0.5.0b2
*************************************

Headline changes
================


* Import, display and export of CR/DX data from image headers
* Hologic tomography projection images are no longer excluded if part of a Combo exposure

Specific upgrade instructions
=============================

**Always make sure you have converted your database to South before attempting an upgrade**

Quick reminder of how, if you haven't done it already:

    Linux::

        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp

    Windows::

        python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp


Upgrading from versions before 0.4.3
````````````````````````````````````

If you are upgrading from 0.3.9 or earlier, you will need to upgrade to
version 0.4.2 first. See the :doc:`release-0.4.3`.

If you are upgrading from 0.4.0 or later, the instructions in :doc:`release-0.4.3`
still need to be followed to install/setup RabbitMQ and Celery and to update
the configuration files, but you can go straight to 0.5.0b1 rather than 
installing 0.4.3.

Upgrading from version 0.4.3
````````````````````````````
.. sourcecode:: bash

    pip install --pre openrem==0.5.0b3

(Will need ``sudo`` or equivalent if using linux without a virtualenv)


Database migration
``````````````````
*Assuming no virtualenv*

Linux::

    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp

Windows::

    C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
    C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

Restart the web server
``````````````````````
If you are using the built-in test web server (`not for production use`)::

    python manage.py runserver x.x.x.x:8000 --insecure

Otherwise restart using the command for your web server

Restart the Celery task queue
`````````````````````````````

For testing, in a new shell: *(assuming no virtualenv)*

Linux::

    cd /usr/local/lib/python2.7/dist-packages/openrem/
    celery -A openremproject worker -l info

Windows::

    cd C:\Python27\Lib\site-packages\openrem\
    celery -A openremproject worker -l info

For production use, see http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html

