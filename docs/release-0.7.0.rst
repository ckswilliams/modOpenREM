########################################
OpenREM Release Notes version 0.7.0 beta
########################################

.. Warning::

    This is a beta version for developer testing. It is not suitable for general use, and the instructions below are
    likely to be incorrect.

****************
Headline changes
****************

* NB: I haven't checked if the following method works. In particular, need to ensure that the first schema migration and migration don't include the new data migration
* Database modification to add study time in datetime format for use with workload charts
* Addition of some new charts

****************************
Upgrading from version 0.6.0
****************************

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* The 0.7.0 upgrade must be made from a 0.6.0 (or later) database, and a schema migration is required:

.. sourcecode:: bash

    pip install openrem==0.7.0b3

    # Windows:
    python C:\Python27\Lib\site-packages\openrem\manage.py makemigrations remapp
	python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp --fake

* Now rename the `0002_upgraded_openrem_add_median_function_and_populate_display_name_table.py.inactive` file
to `0002_upgraded_openrem_add_median_function_and_populate_display_name_table.py` and then run:

.. sourcecode:: bash

    # Windows:
    python C:\Python27\Lib\site-packages\openrem\manage.py makemigrations remapp
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp


Restart the web server
======================

If you are using the built-in test web server (`not for production use`)::

    python manage.py runserver x.x.x.x:8000 --insecure

Otherwise restart using the command for your web server

Restart the Celery task queue
=============================

For testing, in a new shell:

.. sourcecode:: bash

    # Linux: Debian/Ubuntu and derivatives
    cd /usr/local/lib/python2.7/dist-packages/openrem/
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    cd /usr/local/lib/python2.7/site-packages/openrem/
    # Windows
    cd C:\Python27\Lib\site-packages\openrem\

    # All
    celery -A openremproject worker -l info

For production use, see http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html

