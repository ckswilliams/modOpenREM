***************
Troubleshooting
***************

Server 500 errors
=================

**Turn on debug mode**

Locate and edit your local_settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/openremproject/local_settings.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/openremproject/local_settings.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\openremproject\local_settings.py``
* Windows virtualenv: ``Lib\site-packages\openrem\openremproject\local_settings.py``

* Change the line::

    # DEBUG = True

* to::

    DEBUG = True

This will render a debug report in the browser - usually revealing the problem.

Once the problem is fixed, change ``DEBUG`` to ``False``, or comment it again using a ``#``. If you leave debug mode
in place, the system is likely to run out of memory.


Query-retrieve issues
=====================

Refer to the :ref:`qrtroubleshooting` documentation

OpenREM DICOM storage nodes
===========================

Refer to the :ref:`storetroubleshooting` documentation

Log files
=========

Log file location, naming and verbosity were configured in the ``local_settings.py`` configuration - see the
:ref:`local_settings_logfile` configuration docs for details.

If the defaults have not been modified, then there will be three log files in your ``MEDIAROOT`` folder which you
configured at installation. See the install config section on :ref:`mediarootsettings` for details.

The ``openrem.log`` has general logging information, the other two are specific to the DICOM store and DICOM
query-retrieve functions if you are making use of them.

You can increase the verbosity of the log files by changing the log 'level' to ``DEBUG``, or you can decrease the
verbosity to ``WARNING``, 'ERROR', or 'CRITICAL'. The default is ``INFO``.

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
* Windows: ``cd C:\Python27\Lib\site-packages\openrem\``
* Virtualenv: ``cd lib/python2.7/site-packages/openrem/``

Run the django python shell:

.. sourcecode:: python

    python manage.py shell

    from remapp.models import GeneralStudyModuleAttr
    a = GeneralStudyModuleAttr.objects.all()
    a.count()  # Just to see that we are doing something!
    a.delete()
    a.count()
    exit()