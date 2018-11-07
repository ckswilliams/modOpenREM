########################
Upgrade to OpenREM 0.8.2
########################

****************
Headline changes
****************

* Interface: added feature to display workload stats in the home page modality tables
* Query-retrieve: handle non-return of ModalitiesInStudy correctly
* Imports: fix for empty NumericValues in RDSR
* Imports: fix for Toshiba RDSR with incorrect multiple values in SD field for vHP
* Imports: fix for Philips Azurion RDSR with incorrect AcquisitionDeviceType
* Administration: added facility to list and delete failed import studies
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


Restart all the services
========================

Follow the guide at :doc:`startservices`.


