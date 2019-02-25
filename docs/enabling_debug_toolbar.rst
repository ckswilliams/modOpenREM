Enabling debug toolbar
======================

Django Debug Toolbar can be very useful when troubleshooting or optimising the web interface, showing all the queries
that have been run, the timings and lots more.

More information about Django Debug Toolbar can be found at https://django-debug-toolbar.readthedocs.io

Installation
------------

* Activate the virtualenv (assuming you are using one...)
* Install from pip:

..  code-block:: console

    pip install django-debug-toolbar==1.9.1

The version is fixed for now due to the version of Django being used.

Configuration
-------------

* Open ``openremproject/local_settings.py`` and add the lines:

..  code-block:: console

    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ['127.0.0.1']

If you wish to make use of the debug toolbar on machines other than the one the code is running on, change the
INTERNAL_IPS address list to include your client machine.

Using Django Debug Toolbar
--------------------------

When ``DEBUG = True`` in ``openremproject/local_settings.py`` the toolbar should appear.