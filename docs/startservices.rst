**********************
Start all the services
**********************

Test web server
===============

Linux::

    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py runserver --insecure

Windows::

    python C:\Python27\Lib\site-packages\openrem\manage.py runserver --insecure

If you are using a headless server and need to be able to see the 
web interface from another machine, use 
``python /usr/lib/python2.7/dist-packages/openrem/manage.py runserver x.x.x.x:8000 --insecure`` 
(or Windows equivalent) replacing the ``x`` with the IP address of the server 
and ``8000`` with the port you wish to use.

Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)

..  Note::

    Why are we using the ``--insecure`` option? With ``DEBUG`` mode set to ``True``
    the test web server would serve up the static files. In this release,
    ``DEBUG`` mode is set to ``False``, which prevents the test web server
    serving those files. The ``--insecure`` option allows them to be served again.

Celery task queue
=================

Celery will have been automatically installed with OpenREM, and along with
RabbitMQ allows for asynchronous task processing for imports and exports.

..  Note::

    The webserver and Celery both need to be able to read and write to the
    ``MEDIA_ROOT`` location. Therefore you might wish to consider starting
    Celery using the same user or group as the webserver, and setting the
    file permissions accordingly.

In a new shell:

Linux::

    cd /usr/local/lib/python2.7/dist-packages/openrem/
    celery multi start stores default -A openremproject -c:stores 1 -c 3 \
    -Q:stores stores -Q default \
    --pidfile=/path/to/media/celery/%N.pid --logfile=/path/to/media/celery/%N.log

If you intend to use OpenREM to provide a DICOM Store SCP (ie you can DICOM send things to OpenREM without using
any other program, such as Conquest), then we need a Celery Queue just for the store. The node (and queue) created for
this is called ``stores`` and it needs to have a concurrency equal or greater than the number of store SCPs. This would
normally be just one. So set ``-c:stores 1`` or ``-c:stores 2`` etc as you see fit. The ``-c 3`` specifies how many
workers should be available for all the other jobs - exports; and imports when using the OpenREM Store SCP.

You must also specify the location for the pid file and for the log file. You might put these in the media folder, or
the logs might go in ``/var/log/``.

The ``\`` is added in to allow the single command to go over several lines.

The command above doesn't work on Windows, so we have to use two separate commands that stay running in the command
window - see `Daemonising Celery`_ below and follow the link to see a guide to running Celery as a Windows service.

Windows::

    cd C:\Python27\Lib\site-packages\openrem\


    celery multi start stores default -A openremproject -c:stores 2 -c 3 ^
    -Q:stores stores -Q default ^
    --pidfile=C:\path\to\media\celery\%N.pid --logfile=C:\path\to\media\celery\%N.log

This is the same as for Linux, but this time the line continuation character is ``^``.

For production use, see `Daemonising Celery`_ below

To stop the celery queues::

    celery multi stop stores default --pidfile=/path/to/media/celery/%N.pid


Celery periodic tasks: beat
===========================

Celery beat is a scheduler. If it is running, then every 60 seconds a task is run to check if any of the DICOM
Store SCP nodes are set to ``keep_alive``, and if they are, it tries to verify they are running with a DICOM echo.
If this is not successful, then the Store SCP is started.

To run celery beat, open a new shell:
Linux::

    cd /usr/local/lib/python2.7/dist-packages/openrem/

    celery -A openremproject beat -s /path/to/media/celery/celerybeat-schedule -f /path/to/media/celery/celerybeat.log \
    --pidfile=/path/to/media/celery/celerybeat.pid

Windows::

    cd C:\Python27\Lib\site-packages\openrem\

    celery -A openremproject beat -s C:\path\to\media\celery\celerybeat-schedule -f C:\path\to\media\celery\ ^
    --pidfile=C:\path\to\media\celery\celerybeat.pid




Start the DICOM Store SCP
-------------------------

See :doc:`netdicom` - documentation not yet up to date with features.

Start using it!
---------------

Add some data!

.. sourcecode:: bash

    openrem_rdsr.py rdsrfile.dcm

Add some users *(New in version 0.4.0)*

* Go to the admin interface (eg http://localhost:8000/admin) and log in with the user created when you created the database (``syncdb``)
* Create some users and add them to the appropriate groups (if there are no groups, go to the OpenREM homepage and they should be created).

    + ``viewgroup`` can browse the data only
    + ``exportgroup`` can do as view group plus export data to a spreadsheet
    + ``admingroup`` can delete studies and import height and weight data in addition to anything the export group can do

* Return to the OpenREM interface (eg http://localhost:8000/openrem) and log out of the superuser in the top right corner and log in again using one of the new users you have just created.

Further instructions
====================


Daemonising Celery
------------------

In a production environment, Celery will need to start automatically and
not depend on a particular user being logged in. Therefore, much like
the webserver, it will need to be daemonised. For now, please refer to the
instructions and links at http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html.

