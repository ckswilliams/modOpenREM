***************************************
Upgrade an offline OpenREM installation
***************************************

Upgrading OpenREM requires new Python packages to be available as well as the latest
version of OpenREM. These can be downloaded on any computer with Python 2.7 installed and an internet connection,
though if you have trouble when installing the packages you might need to use a similar computer to the one you are
installing on - same operating system and matching 32-bit or 64-bit.

On a computer with internet access
==================================

In a console, navigate to a suitable place and create a directory to collect all the packages in, then use pip to
download them all:

.. sourcecode:: console

    mkdir openremfiles
    pip install -d openremfiles openrem==0.8.0b1

Copy everything to the OpenREM server
-------------------------------------

* Copy the directory to the OpenREM server

On the OpenREM server without internet access
=============================================

* Back up your database

    * For PostgreSQL you can refer to :ref:`backup-psql-db`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers
* If you are using a virtualenv, activate it now, then

.. sourcecode:: console

    pip install --no-index --find-links=openremfiles openrem==0.8.0b1

Now go back to :ref:`upgradefrom074` and update the configuration.