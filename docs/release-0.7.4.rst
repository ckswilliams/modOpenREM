###################################
OpenREM Release Notes version 0.7.4
###################################

****************
Headline changes
****************

* Imports: DX images now import with multiple filters that are MultiValue as well as comma separated
* Exports: DX data now correctly exports to csv and xlsx if studies include multiple filters (eg Cu+Al)
* Install: New release of dependency django-filter breaks OpenREM. Pegged at previous version for now

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Follow the instructions to :doc:`release-0.7.0` and to :doc:`release-0.7.3` first.

Then use the instructions found at :doc:`upgrade-offline` again, but this time change the pip commands from
``openrem==0.7.1`` to ``openrem==0.7.4``.


*************************
Upgrading from 0.6 series
*************************

Follow the instructions to :doc:`release-0.7.0` and to :doc:`release-0.7.3` first.

Finally, return to these instructions to upgrade to 0.7.4.


****************************
Upgrading from version 0.7.1
****************************

Follow the instructions to :doc:`release-0.7.3` first, then return to these instructions to upgrade to 0.7.4.


****************************
Upgrading from version 0.7.3
****************************

* Back up your database

    * For PostgreSQL you can refer to :ref:`backup-psql-db`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.7.4

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem\``

Check for any migrations
========================

.. sourcecode:: bash

    python manage.py makemigrations remapp

The expected response should is: ``No changes detected in app 'remapp'``

Restart all the services
========================

Follow the guide at :doc:`startservices`.


