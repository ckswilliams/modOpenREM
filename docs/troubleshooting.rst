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