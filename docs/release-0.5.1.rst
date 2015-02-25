OpenREM Release Notes version 0.5.1
***********************************

*Document is being created - please do not attempt to follow!*

Headline changes
================

* Major database modification to remove table name length errors
* Extended the field value lengths to better incorporate all possible values and decimal places
* Improved import of grid and filter information from DX images
* Improved DX summary and detail web pages


Specific upgrade instructions
=============================

**Always make sure you have converted your database to South before attempting an upgrade**

Quick reminder of how, if you haven't done it already

.. sourcecode:: bash

    # Linux: Debian/Ubuntu and derivatives
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    python /usr/local/lib/python2.7/site-packages/openrem/manage.py convert_to_south remapp

    # Windows, assuming no virtualenv
    python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp


Upgrading from version 0.3.9 or earlier
```````````````````````````````````````

*Back up your database*

*  ``pip install openrem==0.4.2``
*  Migrate the schema

    .. sourcecode:: bash

        # Linux: Debian/Ubuntu and derivatives
        python /usr/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
        # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
        python /usr/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
        # Windows:
        C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp

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

*  Create and populate the database settings in the new local_settings.py file

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
    created the database (the ``manage.py syncdb`` command - `Do you want to superuser`)

    * Create some users and add them to the appropriate groups (if there are no groups, go to the OpenREM homepage and
    they should be there when you go back to admin).

        + ``viewgroup`` can browse the data only
        + ``exportgroup`` can do as view group plus export data to a spreadsheet, and will be able to import height and weight data in due course (See `Issue #21 <https://bitbucket.org/openrem/openrem/issue/21/>`_)
        + ``admingroup`` can delete studies in addition to anything the export group can do


Upgrading from versions 0.4.0 - 0.4.3
`````````````````````````````````````
*Versions 0.4.0 - 0.4.2*

Install RabbitMQ, move settings from ``openrem`` to ``openremproject``

*Back up your database*

* Install version 0.4.3

    * ``pip install openrem==0.4.3``

* Install RabbitMQ

    * Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
    * Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html


*Versions 0.4.0 - 0.4.3*

Upgrade to 0.5.0, database migration

Upgrading from version 0.5.0
````````````````````````````
Find out how many migration files you have

Method 1:

    Use a file browser or terminal to list the contents of the ``migrations`` folder, eg::

        # Linux Debian/Ubuntu - for others/virtualenv substitute 'site-packages' for 'dist-packages'
        ls /usr/local/lib/python2.7/dist-packages/openrem/remapp/migrations/

Method 2:

    Use the Django ``manage.py`` program to list the existing migrations::

        # Linux Debian/Ubuntu - for others/virtualenv substitute 'site-packages' for 'dist-packages'
        python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate --list remapp

        # Windows
        python C:\Python27\Lib\site-packages\openrem\manage.py migrate --list remapp

    The output should look something like this::

        remapp
        (*) 0001_initial
        (*) 0002_auto__chg_field_ct_accumulated_dose_data_ct_dose_length_product_total_
        (*) 0003_auto__chg_field_general_equipment_module_attributes_station_name
        (*) 0004_auto__chg_field_ct_radiation_dose_comment__chg_field_accumulated_proje
        (*) 0005_auto__add_exports__add_size_upload
        (*) 0006_auto__chg_field_exports_filename
        (*) 0007_auto__add_field_irradiation_event_xray_detector_data_relative_xray_exp


Rename the two 050 migration files to follow on from the existing migrations, for example ``0008_051schemamigration.py``
and ``0009_051datamigration.py``. The ``051schemamigration`` **must** come before the ``051datamigration``
If you now re-run ``migrate --list remapp`` you should get a listing similar to this::

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

Now execute the migrations::

    # Linux Debian/Ubuntu - for others/virtualenv substitute 'site-packages' for 'dist-packages'
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp

    # Windows
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp


If you are upgrading from 0.3.9 or earlier, you will need to upgrade to
version 0.4.2 first. See the :doc:`release-0.4.3`.

If you are upgrading from 0.4.0 or later, the instructions in :doc:`release-0.4.3`
still need to be followed to install/setup RabbitMQ and Celery and to update
the configuration files, but you can go straight to 0.5.0 rather than
installing 0.4.3.

Upgrading from version 0.4.3
````````````````````````````
.. sourcecode:: bash

    pip install openrem==0.5.0

(Will need ``sudo`` or equivalent if using linux without a virtualenv)


Database migration
``````````````````
*Assuming no virtualenv*

Linux::

    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp

Windows::

    C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
    C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

Restart the web server
``````````````````````
If you are using the built-in test web server (`not for production use`)::

    python manage.py runserver x.x.x.x:8000 --insecure

Otherwise restart using the command for your web server

Restart the Celery task queue
`````````````````````````````

For testing, in a new shell: *(assuming no virtualenv)*

Linux::

    cd /usr/local/lib/python2.7/dist-packages/openrem/
    celery -A openremproject worker -l info

Windows::

    cd C:\Python27\Lib\site-packages\openrem\
    celery -A openremproject worker -l info

For production use, see http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html

