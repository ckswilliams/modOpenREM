########################
Upgrade to OpenREM 0.7.2
########################

****************
Headline changes
****************

* New migration file for upgrades from 0.6 series databases
* Fixed multi-line cells in tables so that the links work in IE8
* Charts: Increased number of points that can be plotted and fixed display of bar charts with just one data point

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

place holder

****************************
Upgrading from version 0.7.1
****************************

* Back up your database

    * For PostgreSQL you can refer to :ref:`backup-psql-db`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

.. sourcecode:: bash

    pip install openrem==0.7.2

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem\``

