###############################################
PostgreSQL database for OpenREM on Ubuntu linux
###############################################

.. _create-psql-db:

*********************
Creating the database
*********************

Install PostgreSQL and the python connector
===========================================
    
+ ``sudo apt-get install postgresql libpq-dev``

If you are using a virtualenv, make sure you are in it and it is active (``source bin/activate``)

+ ``pip install psycopg2``

Create a user for the database
==============================

+ ``sudo -u postgres createuser -P openremuser``
+ Enter password, twice

Optional: Specify the location for the database
-----------------------------------------------

You might like to do this if you want to put the database on an encrypted location instead of ``/var/lib/postgresql``.

For this example, I'm going to assume all the OpenREM programs and data are in the folder ``/var/openrem/`` and
postgresql is at version 9.4 (change both as appropriate)::

    sudo /etc/init.d/postgresql stop
    mkdir /var/openrem/database
    sudo cp -aRv /var/lib/postgresql/9.4/main /var/openrem/database/
    sudo nano /etc/postgresql/9.4/main/postgresql.conf

Change the line::

    data_directory = '/var/lib/postgresql/9.4/main'

to::

    data_directory = '/var/openrem/database/main'

then restart the database::

    sudo /etc/init.d/postgresql start

Create the database
===================

.. code-block::

    sudo su postgres
    createdb -T template1 -O openremuser -E 'UTF8' openremdb
    exit

Change the security configuration
=================================

The default security settings are too restrictive to allow access to the database.

+ ``sudo nano /etc/postgresql/9.4/main/pg_hba.conf``
+ Add the following line, and comment out the other 'local' line:
    + ``local openrem_db openrem_user md5``
+ ``sudo /etc/init.d/postgresql restart``

Configure OpenREM to use the database
=====================================

Find and edit the settings file, eg
    + ``nano local/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``

Set the following (changing name, user and password as appropriate)::

    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'openremdb',
    'USER': 'openremuser',
    'PASSWORD': 'openrem_pw',


********************
Back up the database
********************

********************
Restore the database
********************

If the restore is taking place on a different system, ensure that PostgreSQL is installed and the same user has been
added as was used to create the initial database (see :ref:`create-psql-db`)

Create a fresh database and restore from the backup
===================================================

.. sourcecode:: console

    sudo su postgres
    createdb -T template0 new_openremdb_name
    psql new_openremdb_name < path/to/backup.bak
    exit

