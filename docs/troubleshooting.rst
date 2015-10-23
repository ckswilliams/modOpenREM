***************
Troubleshooting
***************

Server 500 errors
=================

Turn on debug mode
------------------

Locate your settings file

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem``

Edit local_settings.py

* Change the line::

    # DEBUG = True

* to::

    DEBUG = True

This will render a debug report in the browser - usually revealing the problem.

Once the problem is fixed, change ``DEBUG`` to ``False``, or comment it again using a ``#``. If you leave debug mode
in place, the system is likely to run out of memory.
