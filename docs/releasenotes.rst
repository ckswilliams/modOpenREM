OpenREM Release Notes
************************

Version history change log
==========================

    ..  toctree::
        :maxdepth: 1
        
        changes

Release notes and upgrade instructions
======================================
    
Version specific information
----------------------------

    ..  toctree::
        :maxdepth: 1
        
        release-0.4.0

Generic upgrade instructions
----------------------------

*   Make sure you have setup South before you upgrade -- see :ref:`Database migrations <convert-to-south>` for details.
*   Always consult the specific version release notes linked above before upgrading.

Code upgrade
^^^^^^^^^^^^
``pip install openrem -U``

*Note* - this will upgrade OpenREM **and all** the programs it depends on (e.g. Django)

Database migration
^^^^^^^^^^^^^^^^^^

Always do a database migration using South after an upgrade in case any of the
database models have changed. This will normally not be the case.

* Linux: ``python /usr/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp``
* Windows: ``C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp``

If response to the last command is 'Nothing seems to have changed', no migration is required. Else, follow the instructions to migrate:

* Linux: ``python /usr/lib/python2.7/dist-packages/openrem/manage.py migrate remapp``
* Windows: ``C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp``    

Restart the web server
^^^^^^^^^^^^^^^^^^^^^^

Restart the web server to enable any changes that have been made to the web interface.


Contributing authors
====================

The following people have contributed to OpenREM - either with code, documentation or ideas.

* `Ed McDonagh <https://bitbucket.org/edmcdonagh>`_
* `David Platten <https://bitbucket.org/dplatten>`_
* `Jonathan Cole <https://bitbucket.org/jacole>`_
* Elly Castellano
* Laurence King
* Daniel Gordon
