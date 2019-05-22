########################
Upgrade to OpenREM 0.9.1
########################

****************
Headline changes
****************

* Imports: fixed imports for GE surgical flat panel c-arm with irregular value types and value meanings
* Interface: added feature to filter by specific number of exposure types -- CT only
* Query-retrieve: new option to get SR series when PACS returns empty series level response
* Query-retrieve: handle illegal missing instance number in image level response
* Query-retrieve: improved logging
* Exports: added export to UK PHE 2019 CT survey format
* General documentation and interface improvements, bug fixes, and changes to prepare for Python 3

*******************
Upgrade preparation
*******************

Version 0.9 of OpenREM has a minimum Python version of 2.7.9 (still needs to be 2.7 not 3) and a minimum version of
setuptools. If your installation was originally for OpenREM 0.6 in 2014 or earlier, these may now be too old and need
updating.

To check the Python version, activate the virtualenv if you are using one, then:

.. code-block:: console

    python -V

If the version is earlier than ``2.7.9``, then an upgrade is needed.

**Ubuntu Linux**

* Check which version of Ubuntu is installed (``lsb_release -a``)
* If it is 14.04 LTS (Trusty), then an operating system upgrade or migration to a new server is required. If migrating,
  ensure the version of OpenREM installed on the new server is the same as the one on the old server, then
  :ref:`restore-psql-linux` following the instructions and when up and running again perform the upgrade on the new
  server
* 16.04 LTS (Xenial) or later should have 2.7.11 or later available.
* For other Linux distributions check in their archives for which versions are available.

**Windows**

* A newer version of Python 2.7 can be downloaded from `python.org <https://www.python.org/downloads>`_ and installed
  over the current version.

**Linux and Windows**

* With a version of Python 2.7.9 or later, setuptools can be updated (activate virtualenv if using one):

    .. code-block:: console

        pip install setuptools -U

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions found at :doc:`upgrade-offline`, before returning here to update the configuration, migrate the
database and complete the upgrade.

***************************************
Upgrading from version 0.7.1 or earlier
***************************************

Follow the instructions to :doc:`release-0.7.3` first, then return to these instructions to upgrade to 0.9.1.


*************************************
Upgrading from version 0.7.3 or later
*************************************

Upgrade
=======

* Back up your database

    * For PostgreSQL on linux you can refer to :ref:`backup-psql-db`
    * For PostgreSQL on Windows you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* Consider temporarily disabling your DICOM Store SCP, or redirecting the data to be processed later

* If you are using a virtualenv, activate it

* Install specific version of Celery:

    **Linux server:**

    .. code-block:: console

        pip install celery==4.2.2

    **Windows server:**

    .. code-block:: console

        pip install celery==3.1.25

* Install the new version of OpenREM:

    .. code-block:: console

        pip install openrem==0.9.1

.. _update_configuration091:

Update the configuration
========================

Locate and edit your local_settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\openremproject\local_settings.py``


Date format - changed with 0.8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set the date format for xlsx exports (need to check csv situation). Copy the following code into your
``local_settings.py`` file if you want to change it from ``dd/mm/yyy``:

.. code-block:: python

    # Date format for exporting data to Excel xlsx files.
    # Default in OpenREM is dd/mm/yyyy. Override it by uncommenting and customising below; a full list of codes is available
    # at https://msdn.microsoft.com/en-us/library/ee634398.aspx.
    # XLSX_DATE = 'mm/dd/yyyy'

Time zone and language - changed with 0.8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider setting the timezone and language in ``local_settings.py``. See ``local_settings.py.example``.

Add additional log file configuration - changed with 0.8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    If the configuration is not added for the new ``openrem_extractor.log`` you will find it being created where ever
    you start the webserver from, and starting the webserver may fail.

Add the new extractor log file configuration to the ``local_settings.py`` - you can copy the 'Logging
configuration' section from  ``local_settings.py.example`` if you haven't made many changes to this section. See the
:ref:`local_settings_logfile` settings in the install instructions.

.. warning::

    If you are upgrading from an earlier beta with the Toshiba RDSR creation logs defined, this has changed names
    and must be modified in ``local_settings.py`` before the migration below. It should be changed to::

        LOGGING['loggers']['remapp.extractors.ct_toshiba']['level'] = 'INFO'  # Toshiba RDSR creation extractor logs

    substituting ``INFO`` for whichever level of logging is desired.

E-mail server settings - changed with 0.9.0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want selected OpenREM users to be automatically sent fluoroscopy high
dose alerts then set the details of the e-mail server to be used in the
`E-mail server settings` part of your ``local_settings.py`` file. Locate and
edit your local_settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\openremproject\local_settings.py``

Then change the e-mail section settings to reflect the e-mail server that is to
be used:

.. code-block:: python

    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False
    EMAIL_DOSE_ALERT_SENDER = 'your.alert@email.address'
    EMAIL_OPENREM_URL = 'http://your.openrem.server'

See the :ref:`email_configuration` documentation for full details.


Migrate the database
====================

In a shell/command window, move into the ``openrem`` folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\``

.. code-block:: console

    python manage.py makemigrations remapp
    python manage.py migrate remapp


Update static files
===================

In the same shell/command window as you used above run the following command to clear the static files
belonging to your previous OpenREM version and replace them with those belonging to the version you have
just installed (assuming you are using a production web server...):

.. code-block:: console

    python manage.py collectstatic --clear

..  admonition:: Virtual directory users

    If you are running your website in a virtual directory, you also have to update the reverse.js file.
    To get the file in the correct path, take care that you insert just after the declaration of
    ``STATIC_ROOT`` the following line in your ``local_settings.py``:

    .. code-block:: console

        JS_REVERSE_OUTPUT_PATH = os.path.join(STATIC_ROOT, 'js', 'django_reverse')

    To update the reverse.js file execute the following command:

    .. code-block:: console

        python manage.py collectstatic_js_reverse

    See  :doc:`virtual_directory` for more details.

Enable task management - changed in 0.9.0
=========================================

RabbitMQ management interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To make use of the RabbitMQ queue display and purge control, the management interface needs to be enabled. To do so,
follow the instructions at :ref:`enableRabbitMQ`.

Celery management interface, Flower
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To make use of the Celery task management, Flower needs to be running. To do so, follow the instructions in
:ref:`start_flower`. For 'one-page Ubuntu' installs, add the Flower related config and create, register and start the
systemd service files as described in :ref:`one_page_linux_celery`. If you need to change the default Flower port of
5555 then make sure you do so in ``openremproject\local_settings.py`` to add/modify the line ``FLOWER_PORT = 5555`` as
well as when you start Flower.

Celery for Windows config - changed in 0.9.0
============================================

For best performance and reliability when using Celery on Windows, if your command for starting Celery specifies a pool
option, for example ``-P solo``, remove it so that Celery reverts to using the default ``prefork`` pool. This will
enable multiple tasks to run concurrently and it will be possible to terminate tasks.

If you are a Windows user you may also wish to review :doc:`celery-windows` as the example control batch files have
been updated.


Ubuntu installs that followed :doc:`quick_start_linux`
======================================================

Systemd service files have been renamed in these docs to use *openrem-function* rather than *function-openrem*. To
update the service files accordingly, follow the following steps. **This is optional**, but will make finding them
easier (e.g. ``sudo systemctl status openrem-[tab][tab]`` will list them!)

.. code-block:: console

    sudo systemctl stop gunicorn-openrem.service
    sudo systemctl stop celery-openrem.service
    sudo systemctl stop flower-openrem.service

    sudo systemctl disable gunicorn-openrem.service
    sudo systemctl disable celery-openrem.service
    sudo systemctl disable flower-openrem.service

    sudo mv /etc/systemd/system/{gunicorn-openrem,openrem-gunicorn}.service
    sudo mv /etc/systemd/system/{celery-openrem,openrem-celery}.service
    sudo mv /etc/systemd/system/{flower-openrem,openrem-flower}.service

    sudo systemctl enable openrem-gunicorn.service
    sudo systemctl enable openrem-celery.service
    sudo systemctl enable openrem-flower.service

    sudo systemctl start openrem-gunicorn.service
    sudo systemctl start openrem-celery.service
    sudo systemctl start openrem-flower.service

Restart all the services
========================

Follow the guide at :doc:`startservices`.
