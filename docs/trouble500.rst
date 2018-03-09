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
in place, the system is likely to run out of memory as database queries are cached.