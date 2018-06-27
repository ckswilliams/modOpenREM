***************
Troubleshooting
***************

..  toctree::
    :maxdepth: 1

    trouble500
    troubleencoding
    trouble_dictionary
    troubledbtlaterality

If you have a modality where every study has one event (usually CT), review

.. toctree::
    :maxdepth: 1

    import_multirdsr

If planar X-ray studies are appearing in fluoroscopy or vice-versa, review

* :doc:`i_displaynames`

For DICOM networking:

* :ref:`qrtroubleshooting` for query retrieve
* :ref:`storetroubleshooting` for DICOM store

Log files
=========

Log file location, naming and verbosity were configured in the ``local_settings.py`` configuration - see the
:ref:`local_settings_logfile` configuration docs for details.

If the defaults have not been modified, then there will be three log files in your ``MEDIAROOT`` folder which you
configured at installation. See the install config section on :ref:`mediarootsettings` for details.

The ``openrem.log`` has general logging information, the other two are specific to the DICOM store and DICOM
query-retrieve functions if you are making use of them.

You can increase the verbosity of the log files by changing the log 'level' to ``DEBUG``, or you can decrease the
verbosity to ``WARNING``, ``ERROR``, or ``CRITICAL``. The default is ``INFO``.

Starting again!
===============

If for any reason you want to start again with the database, then this is how you might do it:

SLQite3 database
----------------

* Delete or rename your existing database file (location will be described in your ``local_settings.py`` file)
* :ref:`database_creation`

Any database
------------

These instructions will also allow you to keep any user settings if you use an SQLite3 database.

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``cd /usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``cd /usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``cd virtualenvfolder/lib/python2.7/site-packages/openrem/``
* Windows: ``cd C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``cd virtualenvfolder\Lib\site-packages\openrem\``

Run the django python shell:

.. sourcecode:: python

    python manage.py shell

    from remapp.models import GeneralStudyModuleAttr
    a = GeneralStudyModuleAttr.objects.all()
    a.count()  # Just to see that we are doing something!
    a.delete()
    a.count()
    exit()