########################
Upgrade to OpenREM 0.9.0
########################

****************
Headline changes
****************

* Interface: added feature to display workload stats in the home page modality tables
* Interface: added :doc:`i_fluoro_high_dose_alerts` feature
* Interface: dual-plane DX studies can now be handled in summary list and study detail pages
* Interface: new option to set display name when unique fields change based on device observer UID in RDSR
* Charts: added fluoroscopy charts of DAP and frequency per requested procedure, fixed bugs in links for others
* Query-retrieve: handle non-return of ModalitiesInStudy correctly
* Query-retrieve: increased query logging and summary feedback
* Query-retrieve: use time range in search (command line only)
* Imports: fix for empty NumericValues in RDSR
* Imports: fix for Toshiba RDSR with incorrect multiple values in SD field for vHP
* Imports: fix for Philips Azurion RDSR with incorrect AcquisitionDeviceType
* Imports: fix for Varian RDSRs
* Exports: made more robust for exporting malformed studies, fixed filtering bugs
* Administration: automatic e-mail alerts sent when fluoroscopy studies exceed a dose alert level
* Administration: added facility to list and delete studies where the import failed
* Administration: added interface to RabbitMQ queues and Celery tasks
* Administration: short-term fix for task performance and control on Windows
* Documentation: further refinement of the linux one-page install
* Installation: :doc:`virtual_directory`


***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions found at :doc:`upgrade-offline`, before returning here to update the database and configuration.

****************************
Upgrading from version 0.8.x
****************************

Upgrade
=======

* Back up your database

    * For PostgreSQL on linux you can refer to :ref:`backup-psql-db`
    * For PostgreSQL on Windows you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* Consider temporarily disabling your DICOM Store SCP, or redirecting the data to be processed later

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.9.0

.. _migratethedatabase090:

Migrate the database
====================

In a shell/command window, move into the ``openrem`` folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\``

.. sourcecode:: bash

    python manage.py makemigrations remapp
    python manage.py migrate remapp


Update static files
===================

In the same shell/command window as you used above run the following command to clear the static files
belonging to your previous OpenREM version and replace them with those belonging to the version you have
just installed (assuming you are using a production web server...):

.. sourcecode:: bash

    python manage.py collectstatic --clear


Enable the RabbitMQ management interface
========================================

To make use of the RabbitMQ queue display and purge control, the management interface needs to be enabled. To do so,
follow the instructions at :ref:`enableRabbitMQ`.

Enable the Celery management interface, Flower
==============================================

To make use of the Celery task management, Flower needs to be running. To do so, follow the instructions in
:ref:`start_flower`. For 'one-page Ubuntu' installs, add the Flower related config and create, register and start the
systemd service files as described in :ref:`one_page_linux_celery`. If you need to change the default Flower port of
5555 then make sure you do so in ``openremproject\local_settings.py`` to add/modify the line ``FLOWER_PORT = 5555`` as
well as when you start Flower.

Changes to Celery for Windows
=============================

For best performance and reliability when using Celery on Windows, it is recommended to do the following from the
openrem folder (activate virtualenv if using one):

.. sourcecode:: bash

    pip install celery==3.1.25

If your command for starting Celery specifies a pool option, for example ``-P solo``, remove it so that Celery reverts
to using the default ``prefork`` pool. This will enable multiple tasks to run concurrently and it will be possible to
terminate tasks.

If you are a Windows user you may also wish to review :doc:`celery-windows` as the example control batch files have
been updated.

E-mail server settings
======================
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

.. sourcecode:: python

    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False
    EMAIL_DOSE_ALERT_SENDER = 'your.alert@email.address'
    EMAIL_OPENREM_URL = 'http://your.openrem.server'

See the :ref:`email_configuration` documentation for full details.


Restart all the services
========================

Follow the guide at :doc:`startservices`.


