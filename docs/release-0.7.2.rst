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

Install using the instructions found at :doc:`upgrade-offline`, but change the pip commands from ``openrem==0.7.1`` to
``openrem==0.7.2b1``. If you are still on a 0.6 series install, upgrade to 0.7.1 first.

****************************
Upgrading from version 0.7.1
****************************

* Back up your database

    * For PostgreSQL you can refer to :ref:`backup-psql-db`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Stop any Celery workers

* If you are using a virtualenv, activate it

* Install the new version of OpenREM:

.. sourcecode:: bash

    pip install openrem==0.7.2b1

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem\``

Check the current status of your migrations
===========================================

.. sourcecode:: bash

    python manage.py showmigrations

If you have an installation that has been upgraded from the 0.6 series, it should have a ``remapp`` section that looks
like this::

    remapp
     [X] 0001_initial
     [X] 0002_upgrade_0_7_from_0_6

Alternatively, if you are using the PostgreSQL database and installed 0.7.1 as a fresh install, the ``remapp``
section should look like this::

    remapp
     [X] 0001_initial
     [X] 0002_0_7_fresh_install_add_median

Finally, if you are using a different database – including the built-in test database SQLite3 – with a fresh install the
``remapp`` section should look like this::

    remapp
     [X] 0001_initial

If your migrations list is different from this, particularly if there are any migrations listed with an empty ``[ ]``
check box and you don't know why, please ask a question on the
`Google group <https://groups.google.com/d/forum/openrem>`_ before continuing. Don't forget to tell us what is in the
``remapp`` section of your ``showmigrations`` listing and what upgrades you have done so far.

Apply the new migration
=======================

Rename the file

.. sourcecode:: console

    remapp/migrations/000x_delete_060_acq_field.py.inactive

to:

.. sourcecode:: console

    remapp/migrations/000x_delete_060_acq_field.py

.. Note:: You can optionally change the ``000x`` to ``0003`` or similar, but it is not important. The important thing is
          that the end of the filename is ``.py`` and not ``.inactive``. You can che3ck that the renaming has been
          been successful by running the ``showmigrations`` command again - it should now be listed with an empty pair of
          square brackets.

and then run

.. sourcecode:: console

    python manage.py migrate remapp

This migration will make changes that are only applicable to upgrades from 0.6 series databases, but they do no harm to
0.7.1 fresh installs, so should be run anyway. You might like to run the ``showmigrations`` command to confirm it has
been applied.

Restart all the services
========================

Follow the guide at :doc:`startservices`.

Import all the failed studies since 0.6 series upgrade
======================================================

Re-import any fluoroscopy, radiography or mammography data that has not imported since the upgrade from the 0.6 series.
This relates to `issue #415 <https://bitbucket.org/openrem/openrem/issue/415/>`_ on the Bitbucket issue tracker.

If you have any studies complaining ::

    remapp.models.DoesNotExist: ProjectionXRayRadiationDose matching query does not exist.

You should check to see if the study you are importing has been partially imported before the database was fixed. If it
has, you might need to delete it using the delete function in the web interface. You will only see the delete function
if you have admin privileges - see :ref:`user-settings` for details.

*************************
Upgrading from 0.6 series
*************************

Follow the instructions to :doc:`release-0.7.0` first, then return to these instructions to upgrade to 0.7.2.
