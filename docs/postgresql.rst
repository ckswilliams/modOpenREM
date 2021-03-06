###########################
PostgreSQL database (Linux)
###########################

.. _create-psql-db:

*********************
Creating the database
*********************

Install PostgreSQL and the python connector
===========================================
    
.. sourcecode:: console

    sudo apt-get install postgresql

If you are using a virtualenv, make sure you are in it and it is active (``source bin/activate``)

.. sourcecode:: console

    pip install psycopg2-binary

Change the security configuration
=================================

The default security settings are too restrictive to allow access to the database. Assumes version ``10``, change as
appropriate.


.. sourcecode:: console

    sudo nano /etc/postgresql/10/main/pg_hba.conf

Scroll down to the bottom of the file and edit the following line from ``peer`` to ``md5``:

.. sourcecode:: console

    local    all            all                         md5

Don't worry about any lines that start with a ``#`` as they are ignored. If you can't access the database when
everything else is configured, you might need to revisit this file and see if there are other lines with a method of
``peer`` that need to be ``md5``

.. note::

    If you need to have different settings for different databases on your server, you can use the database name instead
    of the first ``all``, and/or the the database user name instead of the second ``all``.

Restart PostgreSQL so the new settings take effect:

.. sourcecode:: console

    sudo service postgresql restart

Optional: Specify the location for the database files
-----------------------------------------------------

:ref:`move_pg_files`

Create a user for the OpenREM database
======================================

.. sourcecode:: console

    sudo -u postgres createuser -P openremuser

Enter a new password for the ``openremuser``, twice

Create the OpenREM database
===========================

.. sourcecode:: console

    sudo -u postgres createdb -T template1 -O openremuser -E 'UTF8' openremdb

**If this is your initial install**, you are now ready to install OpenREM, so go to the :doc:`install` docs.

If you are replacing a SQLite test install with PostgreSQL, continue here.

Configure OpenREM to use the database
=====================================

Move to the OpenREM install directory:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``vitualenvfolder/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``virtualenvfolder\Lib\site-packages\openrem\``


Edit the settings file, eg

.. sourcecode:: console

    nano openremproject/local_settings.py

Set the following (changing database name, user and password as appropriate)

.. sourcecode:: python

    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'openremdb',
    'USER': 'openremuser',
    'PASSWORD': 'openrem_pw',

.. _backup-psql-db:

*******************
Backup the database
*******************

Ad-hoc backup from the command line
===================================

.. sourcecode:: console

    sudo -u postgres pg_dump openremdb > /path/to/backup.bak

If you are moving a backup file between systems, or keeping a few backups, you may like to compress the backup; for
example a 345 MB OpenREM database compresses to 40 MB:

.. sourcecode:: console

    tar -czf backup.bak.tar.gz backup.bak

Automated backup with a bash script
===================================

.. sourcecode:: bash

    #! /bin/bash
    rm -rf /path/to/db/backups/*
    PGPASSWORD="openrem_pw" /usr/bin/pg_dump -Uopenremuser openremdb > /path/to/db/backups/openrem.bak

This script could be called by a cron task, or by a backup system such as backuppc prior to running the system backup.

.. _restore-psql-linux:

********************
Restore the database
********************

If the restore is taking place on a different system,

* ensure that PostgreSQL is installed and the same user has been added as was used to create the initial database
  (see :ref:`create-psql-db`) -- check ``local_settings.py`` if you can't remember the the user name used!
* Ensure that the new system has the same version of OpenREM installed as the system the database was backed up from.
* Ensure the ``openrem/remapp/migrations/`` folder has no files in except __init__.py

Create a fresh database and restore from the backup:

.. sourcecode:: console

    sudo -u postgres createdb -T template0 new_openremdb_name
    sudo -u postgres psql new_openremdb_name < /path/to/db/backups/openrem.bak

Reconfigure ``local_settings.py`` with the new database details and introduce OpenREM to the restored database:

.. sourcecode:: console

    python manage.py migrate --fake-initial
    python manage.py makemigrations remapp
    python manage.py migrate remapp --fake

If you are creating a second system in order to test upgrading, you can do this now followed by the usual ``python
manage.py makemigrations remapp`` then ``python manage.py migrate remapp`` as per the upgrade instructions.


**************************
Useful PostgreSQL commands
**************************

.. sourcecode:: psql

    -- Start the PostgreSQL console
    sudo -u postgres psql

    -- List users
    \du

    -- List databases
    \l

    -- Exit the console
    \q


.. _move_pg_files:

*************************************************
Advanced: specify location for the database files
*************************************************

You might like to do this if you want to put the database on an encrypted location instead of ``/var/lib/postgresql``.

For this example, I'm going to assume all the OpenREM programs and data are in the folder ``/var/openrem/`` and
PostgreSQL is at version ``10`` (change both as appropriate)

.. sourcecode:: console

    sudo service postgresql stop
    mkdir /var/openrem/database
    sudo cp -aRv /var/lib/postgresql/10/main /var/openrem/database/
    sudo nano /etc/postgresql/10/main/postgresql.conf

Change the line

.. sourcecode:: console

    data_directory = '/var/lib/postgresql/10/main'

to

.. sourcecode:: console

    data_directory = '/var/openrem/database/main'

then restart PostgreSQL:

.. sourcecode:: console

    sudo service postgresql start