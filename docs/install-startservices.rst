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
    celery multi start stores default -A openremproject -c:stores 2 -c 3 \
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



Windows::

    cd C:\Python27\Lib\site-packages\openrem\
    celery multi start stores default -A openremproject -c:stores 2 -c 3 ^
    -Q:stores stores -Q default ^
    --pidfile=C:\path\to\media\celery\%N.pid --logfile=C:\path\to\media\celery\%N.log

This is the same as for Linux, but this time the line continuation character is ``^``.

For production use, see `Daemonising Celery`_ below

To stop the celery queues::

    celery multi stop stores default --pidfile=/path/to/media/celery/%N.pid


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

Database options
----------------

SQLite is great for getting things running quickly and testing if the setup works,
but is really not recommended for production use on any scale. Therefore it is
recommended to use a different database such as `PostgreSQL <http://www.postgresql.org>`_ or 
`MySQL <http://www.mysql.com>`_.

Here are instructions for installing PostgreSQL on linux and on Windows:

..  toctree::
    :maxdepth: 1
    
    postgresql
    postgresql_windows

..  _convert-to-south:

Database migrations
-------------------

South is a django application to manage database migrations. Using
South means that future changes to the database model can be calculated
and executed automatically with simple commands when OpenREM is upgraded.

Production webservers
---------------------

Unlike the database, the production webserver can be left till later and
can be changed again at any time.

For performance it is recommended that a production webserver is used instead of the inbuilt 'runserver'.
Popular choices would be either `Apache <http://httpd.apache.org>`_ or you can do as the cool kids
do and use `Gunicorn with nginx <http://www.robgolding.com/blog/2011/11/12/django-in-production-part-1---the-stack/>`_.

The `django website <https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/>`_ 
has instructions and links to get you set up with Apache.

Daemonising Celery
------------------

In a production environment, Celery will need to start automatically and
not depend on a particular user being logged in. Therefore, much like
the webserver, it will need to be daemonised. For now, please refer to the
instructions and links at http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html.

Virtualenv and virtualenvwrapper
--------------------------------

If the server is to be used for more than one python application, or you 
wish to be able to test different versions of OpenREM or do any development,
it is highly recommended that you use `virtualenv`_ or maybe `virtualenvwrapper`_

Virtualenv sets up an isolated python environment and is relatively easy to use.

If you do use virtualenv, all the paths referred to in the documentation will
be changed to:

* Linux: ``lib/python2.7/site-packages/openrem/``
* Windows: ``Lib\site-packages\openrem``

In Windows, even when the virtualenv is activated you will need to call `python`
and provide the full path to script in the `Scripts` folder. If you call the
script (such as `openrem_rdsr.py`) without prefixing it with `python`, the
system wide Python will be used instead. This doesn't apply to Linux, where
once activated, the scripts can be called without a `python` prefix from anywhere. 


Related guides
==============

    ..  toctree::
        :maxdepth: 1
        
        conquestAsWindowsService
        backupMySQLWindows
        backupRestorePostgreSQL
        conquestImportConfig
        conquestAddRDSR

Advanced guides for developers
------------------------------

    ..  toctree::
        :maxdepth: 1
        
        apache_on_windows


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _(What is south?): `Database migrations`_
.. _consider virtualenv: `Virtualenv and virtualenvwrapper`_
