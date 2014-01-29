Upgrade instructions
*************************


Upgrading from tar.gz package
=============================

#. ``pip install OpenREM-version.tar.gz``
#. ``python path/to/openrem/manage.py schemamigration --auto remapp``
    #. eg ``python lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp``
#. If response to the last command is 'Nothing seems to have changed', no migration is reuired. Else, follow the instructions to migrate.
#. Restart the web server, in case changes have been made to the web interface.
