#############################
PostgreSQL database (Windows)
#############################

..  Note:: Original author JA Cole

Get PostgreSQL and the python connector
=======================================
    
+ Download the installer from http://www.enterprisedb.com/products-services-training/pgdownload#windows
+ Download the Python PostgreSQL connector from http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg

  * Find the right version - look for ``psycopg2-X-cp27-cp27m-win32.whl`` for 32-bit Windows or
  * ``psycopg2-X-cp27-cp27m-win_amd64.whl`` for 64-it Windows.
  * At the time of writing, ``X`` was ``2.7.3.2`` - choose the latest ``cp27`` version

.. _windowspsqlinstall:

Install PostgreSQL
==================

Run the the postgresql installer. It will ask for a location. Ensure the "data" directory is *not* under "Program Files"
as this can cause permissions errors. Enter a superuser password when prompted. Make sure you keep this safe as you will
need it.

Create a user and database
==========================

Open pgAdmin

+ Click on servers to expand
+ Double click on PostgreSQL 9.6 (or whichever version you have installed)
+ Enter your superuser password
+ Right click on "login roles" and choose "New login role"
+ Create the openremuser (or whatever you want your user to be called) and under definition add a password.
+ Click OK
+ Right click on databases and choose "New database"
+ Name the database (openremdb is fine) and assign the the owner to the user you just created.


Install psycopg2
================

.. sourcecode:: console

    pip install psycopg2-2.7.3.2-cp27-cp27m-win32.whl  # update the version number
    # or if you have the 64-bit version
    pip install psycopg2-2.7.3.2-cp27-cp27m-win_amd64.whl  # update the version number
    # adjusting the version number appropriately

**If this is your initial install**, you are now ready to install OpenREM, so go to the :doc:`install` docs.

If you are replacing a SQLite test install with PostgreSQL, continue here.

Configure OpenREM to use the database
=====================================

Find and edit the settings file (notepad works fine). The path depends on your python install, but could be something like:
    + ``C:\lib\python2.7\site-packages\openrem\openremproject\local_settings.py``

Set the following (changing name, user and password as appropriate):
    + ``'ENGINE': 'django.db.backends.postgresql_psycopg2',``
    + ``'NAME': 'openrem_db',``
    + ``'USER': 'openremuser',``
    + ``'PASSWORD': 'openrem_pw',``

