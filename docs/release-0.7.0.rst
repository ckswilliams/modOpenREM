###################################
OpenREM Release Notes version 0.7.0
###################################

****************
Headline changes
****************

* NB: I haven't checked if the following method works. In particular, need to ensure that the first schema migration and migration don't include the new data migration
* Database modification to add study time in datetime format for use with workload charts
* Addition of some new charts

****************************
Upgrading from version 0.6.0
****************************

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* The 0.7.0 upgrade must be made from a 0.6.0 (or later) database, and a schema migration is required:

.. sourcecode:: bash

    pip install openrem==0.7.0

    # Linux: Debian/Ubuntu and derivatives
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    python /usr/local/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
    python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp
    # Windows:
    python C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
    python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

* You now need to run a data migration to populate the new database field

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
        ( ) 00xx_study_workload_chart_time_datamigration.py

*   Rename the 00xx migration file to follow on from the existing migrations, for example ``0008_study_workload_chart_time_datamigration.py``
    for the existing migrations above.

    If you are using linux, you might like to do it like this (from within the ``openrem`` folder):

    .. sourcecode:: bash

        mv remapp/migrations/00{xx,08}_study_workload_chart_time_datamigration.py

*   If you now re-run ``migrate --list remapp`` you should get a listing with the ``study_workload_chart_time_datamigration``
    listed at the end::

         remapp
          (*) 0001_initial
          (*) 0002_auto__chg_field_ct_accumulated_dose_data_ct_dose_length_product_total_
          (*) 0003_auto__chg_field_general_equipment_module_attributes_station_name
          (*) 0004_auto__chg_field_ct_radiation_dose_comment__chg_field_accumulated_proje
          (*) 0005_auto__add_exports__add_size_upload
          (*) 0006_auto__chg_field_exports_filename
          (*) 0007_auto__add_field_irradiation_event_xray_detector_data_relative_xray_exp
          ( ) 0008_study_workload_chart_time_datamigration.py

    The star indicates that a migration has already been completed. If you have any that are not completed apart from the
    ``study_workload_chart_time_datamigration`` then please resolve these first.

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

