###################################
OpenREM Release Notes version 0.7.3
###################################

****************
Headline changes
****************

* Database: New migration file for upgrades from 0.6 series databases
* Charts: Fixed display and export errors, improved layout and increased the number of data points that can be plotted
* Interface: Fixed multi-line cells in tables so that the links work in IE8
* Interface: Fixed delete cancel button in firefox
* Exports: Fixed export of non-ASCII characters to csv file

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************

Upgrade using the instructions found at :doc:`upgrade-offline`, but change the pip commands from ``openrem==0.7.1`` to
``openrem==0.7.3``. If you are still on a 0.6 series install, upgrade to 0.7.1 first.

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

    pip install openrem==0.7.3

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

If you are using the PostgreSQL database and installed 0.7.1 as a fresh install, the ``remapp``
section should look like this::

    remapp
     [X] 0001_initial
     [X] 0002_0_7_fresh_install_add_median

If you installed 0.7.1 as a fresh install and are using a different database – such as MySQL or the built-in test
database SQLite3 – the ``remapp`` section should look like this::

    remapp
     [X] 0001_initial

**For both of these scenarios your upgrade is complete** and you can :doc:`startservices`.

If you have an installation that has been upgraded from the 0.6 series, it should have a ``remapp`` section that looks
like this::

    remapp
     [X] 0001_initial
     [X] 0002_upgrade_0_7_from_0_6

For this scenario, please continue and apply the new migration using the instructions below.

If your migrations list is different from these, particularly if there are any migrations listed with an empty ``[ ]``
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

Check that the rename was successful by running ``python manage.py showmigrations`` again. The new migration should
be listed with an empty pair of square brackets.

Now run

.. sourcecode:: console

    python manage.py migrate remapp

This should result in an error similar to this:

.. sourcecode:: console

    CommandError: Conflicting migrations detected (0002_upgrade_0_7_from_0_6, 000x_delete_060_acq_field in remapp).
    To fix them run 'python manage.py makemigrations --merge'

Now run

.. sourcecode:: console

    python manage.py makemigrations --merge

This will then list the merge actions, finishing with the following text:

.. sourcecode:: console

    Merging will only work if the operations printed above do not conflict
    with each other (working on different fields or models)
    Do you want to merge these migration branches? [y/N]

Respond with a ``y``, then run ``python manage.py showmigrations`` again. This should result in the following listing::

    remapp
     [X] 0001_initial
     [ ] 000x_delete_060_acq_field
     [X] 0002_upgrade_0_7_from_0_6
     [ ] 0003_merge

Now run the migration:

.. sourcecode:: console

    python manage.py migrate remapp

A final ``python manage.py showmigrations`` should show::

    remapp
     [X] 0001_initial
     [X] 000x_delete_060_acq_field
     [X] 0002_upgrade_0_7_from_0_6
     [X] 0003_merge

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

Follow the instructions to :doc:`release-0.7.0` first, then return to these instructions to upgrade to 0.7.3.
