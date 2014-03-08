Upgrade instructions
*************************


Upgrading from tar.gz package
=============================

..  note:: Make sure you have setup South before you upgrade -- see :ref:`7. Convert the database to use South <convert-to-south>` for details.

Code upgrade
------------
#. ``pip install OpenREM-version.tar.gz``

Database migration
------------------
Always do a database migration using South after an upgrade in case any of the
database models have changed. This will normally not be the case.

#. ``python path/to/openrem/manage.py schemamigration --auto remapp``
    eg ``python lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp``
#. If response to the last command is 'Nothing seems to have changed', no migration is required. Else, follow the instructions to migrate.

Restart the web server
----------------------
#. Restart the web server to enable any changes that have been made to the web interface.
