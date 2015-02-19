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

.. code-block:: bash

    # Linux Debian/Ubuntu - for others/virtualenv substitute 'site-packages' for 'dist-packages'
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp

    # Windows
    python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp


Upgrading from version 0.3.9 or earlier
```````````````````````````````````````
Upgrade to 0.4.2 - add local_settings, transfer db settings

Upgrading from versions 0.4.0 - 0.4.3
`````````````````````````````````````
*Versions 0.4.0 - 0.4.2*

Install RabbitMQ, move settings from ``openrem`` to ``openremproject``

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

