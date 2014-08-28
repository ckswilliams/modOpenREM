=======
OpenREM
=======

OpenREM is a Django app to extract, store and export Radiation Exposure
Monitoring related information, primarily from DICOM files.

Full documentation can be found on Read the Docs: http://docs.openrem.org

**For upgrades**, please look at the `version 0.4.3 release notes <http://docs.openrem.org/en/latest/release-0.4.3.html>`_

Quick start - please refer to the `full documentation <http://docs.openrem.org>`_ for details
---------------------------------------------------------------------------------------------

*(Linux path notation - use back slashes for Windows paths except in config files)*

#. Install python 2.7
#. Install `setuptools and pip <http://www.pip-installer.org/en/latest/installing.html>`_
#. Install `RabbitMQ <http://www.rabbitmq.com/>`_
#. Install OpenREM::

    pip install openrem

#. Configure OpenREM
    + Locate install location, typically ``something/lib/python2.7/site-packages/openrem``
    + There are two files that need renaming:

        ``openrem/openrem/local_settings.py.example`` to ``openrem/openrem/local_settings.py`` and
        ``openrem/openrem/wsgi.py.example`` to ``openrem/openrem/wsgi.py``

    + in the ``local_settings.py`` file, set the database details.
    + For testing purposes, use::

        'ENGINE': 'django.db.backends.sqlite3'
        'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO.db'

    + in the ``local_settings.py`` file, set the upload and download folder ``MEDIA_ROOT``
#. Create the database::

    python path/to/openrem/manage.py syncdb

#. Start test web server::

    python path/to/openrem/manage.py runserver

#. Start the Celery task queue. For testing purposes, in a shell go to the openrem folder and use::

    celery -A openrem worker -l info

#. Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)
#. Create some users and add them to the ``viewgroup``, ``exportgroup`` or ``admingroup`` in the admin interface, eg http://localhost:8000/admin
#. Add some data::

    openrem_rdsr.py rdsrfile.dcm