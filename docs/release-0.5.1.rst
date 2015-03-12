####################
Release Notes v0.5.1
####################

****************
Headline changes
****************

* Major database modification to remove table name length errors
* Extended the field value lengths to better incorporate all possible values and decimal places
* Improved import of grid and filter information from DX images
* Improved DX summary and detail web pages
* Any item in a row can now be clicked to move between the home and filtered pages

**************************
Upgrades: Convert to South
**************************

**Always make sure you have converted your database to South before attempting an upgrade**

Quick reminder of how, if you haven't done it already

.. sourcecode:: bash

    # Linux: Debian/Ubuntu and derivatives
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    python /usr/local/lib/python2.7/site-packages/openrem/manage.py convert_to_south remapp

    # Windows, assuming no virtualenv
    python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp

***************************
Upgrading from before 0.5.0
***************************

Upgrading from version 0.3.9 or earlier
=======================================

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

*  ``pip install openrem==0.4.2``
*  Migrate the schema

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        python /usr/local/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
        # Windows:
        python C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp

    When South has considered the changes to the schema, you will see the following message::

     ? The field 'Observer_context.device_observer_name' does not have a default specified, yet is NOT NULL.
     ? Since you are making this field nullable, you MUST specify a default
     ? value to use for existing rows. Would you like to:
     ?  1. Quit now.
     ?  2. Specify a one-off value to use for existing columns now
     ?  3. Disable the backwards migration by raising an exception; you can edit the migration to fix it later
     ? Please select a choice: 3

    * As per the final line above, please select option 3, and then execute the migration:

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp

        # Windows, assuming no virtualenv
        python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

*  Create and populate the database settings in the new ``local_settings.py`` file

    The ``openrem/openrem`` folder can be found at:

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        /usr/lib/python2.7/dist-packages/openrem/openrem
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        /usr/lib/python2.7/site-packages/openrem/openrem
        # Windows:
        C:\Python27\Lib\site-packages\openrem\openrem

    In the ``openrem/openrem`` folder, create a new file called ``local_settings.py`` and copy the `contents of this link
    <https://bitbucket.org/openrem/openrem/raw/a37540ba88a5e9b383cf0ea03a3e77fb35638f43/openrem/openremproject/local_settings.py.example>`_
    into a the file and save it. Alternatively, rename ``local_settings.py.example`` to ``local_settings.py`` - this is
    an older version of the file.

    Copy the database details from ``settings.py`` into ``local_settings.py``

* Change the secret key - you can use http://www.miniwebtool.com/django-secret-key-generator/ to generate a new one
* Move the existing ``settings.py`` out of the python directories (delete or move somewhere as a backup)
* Rename the ``settings.py.new`` to ``settings.py``
* Restart your webserver to check everything looks ok
* Add some users

    * Go to the admin interface (eg http://localhost:8000/admin) and log in with the user created when you originally
      created the database (the ``manage.py syncdb`` command - *Do you want to create a superuser*)

    * Create some users and add them to the appropriate groups (if there are no groups, go to the OpenREM homepage and
      they should be there when you go back to admin).

        + ``viewgroup`` can browse the data only
        + ``exportgroup`` can do as view group plus export data to a spreadsheet, and will be able to import height and weight data in due course (See `Issue #21 <https://bitbucket.org/openrem/openrem/issue/21/>`_)
        + ``admingroup`` can delete studies in addition to anything the export group can do


Upgrading from versions 0.4.0 - 0.4.2
=====================================

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Install version 0.5.0

    * ``pip install openrem==0.5.0``

* Install RabbitMQ

    * Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
    * Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html

* Move ``local_settings.py`` details from ``openrem`` to ``openremproject``

    The inner ``openrem`` Django project folder has now been renamed ``openremproject``
    The customised ``local_settings.py`` file and the ``wsgi.py`` file have
    remain in the old ``openrem`` folder. The ``openrem/openrem`` folder can be found as detailed in the upgrade from
    '0.3.9 or earlier' instructions above, and the new ``openrem/openremproject`` folder is in the same place.

    * Move ``local_settings.py`` to ``openremproject``. If you have kept the older local_settings file, you may like to
      instead rename the ``local_settings.py.example`` file instead, then transfer the database settings and change the
      secret key.

    * Set the path for ``MEDIA_ROOT``. The webserver needs to be able to write to this location - it is where OpenREM
      will store export files etc so that they can be downloaded. For suggestions, see the main _install instructions.

    * Set ``ALLOWED_HOSTS``. For details see the `Django docs <https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts>`_
      A ``'*'`` allows any host - see the Django docs for the risk of this.

* Move ``wsgi.py`` from ``openrem`` to ``openremproject`` or rename ``wsgi.py.example`` in ``openremproject``

    If you haven't edited it, simply rename the new version in ``openremproject``. Otherwise, move the old version and
    edit the following line as follows:

    .. sourcecode:: bash

        # Old:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openrem.settings")
        # New:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openremproject.settings")


* Tidying up - you should delete the old ``openrem`` folder - you might like to take a backup first!

* Update web server configuration

    The configuration of the webserver will need to be updated to reflect the new location for the ``settings.py`` file
    and the ``wsgi.py`` file.

    If you are using the built-in test webserver, static files will no-longer be served unless you use the ``insecure``
    option:

    .. sourcecode:: bash

        python manage.py runserver x.x.x.x:8000 --insecure

*  Migrate the schema

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        python /usr/local/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
        python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp
        # Windows:
        python C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
        python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

After restarting the webserver, you should now have OpenREM 0.5.0 up and running. If you wish to test export
functionality at this stage, start the Celery task queue - instructions in the :doc:`install` docs or at the end of this
guide.

Now move to `Upgrading from version 0.5.0`_.

Upgrading from version 0.4.3
============================

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* The 0.5.1 upgrade `must` be made from a 0.5.0 database, so a schema migration is required:

    .. sourcecode:: bash

        pip install openrem==0.5.0

            # Linux: Debian/Ubuntu and derivatives
            python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
            python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
            # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
            python /usr/local/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
            python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp
            # Windows:
            python C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
            python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp


****************************
Upgrading from version 0.5.0
****************************

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* Install 0.5.1:

    .. sourcecode:: bash

        pip install openrem==0.5.1

* Find out how many migration files you have

    Method 1:

        Use a file browser or terminal to list the contents of the ``migrations`` folder, eg:

        .. sourcecode:: bash

            # Linux: Debian/Ubuntu and derivatives
            ls /usr/local/lib/python2.7/dist-packages/openrem/remapp/migrations/
            # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
            ls /usr/local/lib/python2.7/site-packages/openrem/remapp/migrations/
            # Windows (alternatively use the file browser):
            dir C:\Python27\Lib\site-packages\openrem\remapp\migrations\

    Method 2:

        Use the Django ``manage.py`` program to list the existing migrations:

        .. sourcecode:: bash

            # Linux: Debian/Ubuntu and derivatives
            python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate --list remapp
            # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
            python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate --list remapp
            # Windows
            python C:\Python27\Lib\site-packages\openrem\manage.py migrate --list remapp

    The output should look something like this - there can be any number of existing migrations (though 0001_initial
    will always be present)::

        remapp
        (*) 0001_initial
        (*) 0002_auto__chg_field_ct_accumulated_dose_data_ct_dose_length_product_total_
        (*) 0003_auto__chg_field_general_equipment_module_attributes_station_name
        (*) 0004_auto__chg_field_ct_radiation_dose_comment__chg_field_accumulated_proje
        (*) 0005_auto__add_exports__add_size_upload
        (*) 0006_auto__chg_field_exports_filename
        (*) 0007_auto__add_field_irradiation_event_xray_detector_data_relative_xray_exp


*   Rename the two 050 migration files to follow on from the existing migrations, for example ``0008_051schemamigration.py``
    and ``0009_051datamigration.py`` for the existing migrations above, or ``0002_051schemamigration.py`` and
    ``0003_051datamigration.py`` if the only migration is the initial migration. The ``051schemamigration`` **must**
    come before the ``051datamigration``.

*   If you now re-run ``migrate --list remapp`` you should get a listing with the ``051schemamigration`` and the
    ``051datamigration`` listed at the end::

         remapp
          (*) 0001_initial
          (*) 0002_auto__chg_field_ct_accumulated_dose_data_ct_dose_length_product_total_
          (*) 0003_auto__chg_field_general_equipment_module_attributes_station_name
          (*) 0004_auto__chg_field_ct_radiation_dose_comment__chg_field_accumulated_proje
          (*) 0005_auto__add_exports__add_size_upload
          (*) 0006_auto__chg_field_exports_filename
          (*) 0007_auto__add_field_irradiation_event_xray_detector_data_relative_xray_exp
          ( ) 0008_051schemamigration
          ( ) 0009_051datamigration

    The star indicates that a migration has already been completed. If you have any that are not completed apart from the
    ``051schemamigration`` and the ``051datamigration`` then please resolve these first.

*   Now execute the migrations:

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp
        # Windows
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

