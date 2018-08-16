#############################
PostgreSQL database (Windows)
#############################

..  Note:: Original author JA Cole

Get PostgreSQL and the python connector
=======================================
    
+ Download the installer from http://www.enterprisedb.com/products-services-training/pgdownload#windows
+ Install the Python PostgreSQL connector (activate the virtualenv first if using)::

    pip install psycopg2-binary

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
+ Create the openremuser (or whatever you want your user to be called) and under "Definition" add a password
+ Under "Privileges" ensure that "Can login" and "Create databases" are set to "Yes"
+ Click OK
+ Right click on databases and choose "New database"
+ Name the database (openremdb is fine) and assign the the owner to the user you just created


**If this is your initial install**, you are now ready to install OpenREM, so go to the :doc:`install` docs.

If you are replacing a SQLite test install with PostgreSQL, continue here.

Configure OpenREM to use the database
=====================================

Find and edit the settings file (notepad works fine). The path depends on your python install, but could be something like:
    + ``C:\lib\python2.7\site-packages\openrem\openremproject\local_settings.py``

Set the following (changing name, user and password as appropriate):
    + ``'ENGINE': 'django.db.backends.postgresql_psycopg2',``
    + ``'NAME': 'openremdb',``
    + ``'USER': 'openremuser',``
    + ``'PASSWORD': 'openrem_pw',``

