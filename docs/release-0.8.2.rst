########################
Upgrade to OpenREM 0.8.2
########################

****************
Headline changes
****************

* Interface: added feature to display workload stats in the home page modality tables
* Interface: added :doc:`i_fluoro_high_dose_alerts` feature
* Administration: automatic e-mail alerts sent when fluoroscopy studies exceed a dose alert level
* Query-retrieve: handle non-return of ModalitiesInStudy correctly
* Imports: fix for empty NumericValues in RDSR
* Imports: fix for Toshiba RDSR with incorrect multiple values in SD field for vHP
* Imports: fix for Philips Azurion RDSR with incorrect AcquisitionDeviceType
* Imports: fix for Varian RDSRs
* Administration: added facility to list and delete failed import studies
* Administration: added interface to RabbitMQ queues
* Documentation: further refinement of the linux one-page install
* Web server: :doc:`virtual_directory`


***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions found at :doc:`upgrade-offline`, before returning here to update the database and configuration.

*************************************
Upgrading from version 0.7.4 or 0.8.x
*************************************

Upgrade
=======

* Back up your database

    * For PostgreSQL on linux you can refer to :ref:`backup-psql-db`
    * For PostgreSQL on Windows you can refer to :ref:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* Consider temporarily disabling your DICOM Store SCP, or redirecting the data to be processed later

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.8.2


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
    # if changes are detected (not expected between most beta versions)
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


Update the configuration
========================

Locate and edit your local_settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\openremproject\local_settings.py``

E-mail server settings
^^^^^^^^^^^^^^^^^^^^^^
If you want selected OpenREM users to be automatically sent fluroscopy high
dose alerts then set the details of the e-mail server to be used in the
`E-mail server settings` part of your ``local_settings.py`` file:

.. sourcecode:: python

    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = 'a.user.that.can.send'
    EMAIL_HOST_PASSWORD = 'the.above.user.password'
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False
    EMAIL_DOSE_ALERT_SENDER = 'your.alert@email.address'
    EMAIL_OPENREM_URL = 'http://your.openrem.server'

See the :ref:`email_configuration` documentation for full details.


Restart all the services
========================

Follow the guide at :doc:`startservices`.


