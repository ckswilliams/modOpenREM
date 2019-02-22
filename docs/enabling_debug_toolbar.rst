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

* Copy the tuple ``MIDDLEWARE_CLASSES`` from ``openremproject/settings.py`` to ``openremproject/local_settings.py``
* In ``openremproject/local_settings.py``, add ``'pagination.middleware.PaginationMiddleware',``, before the
  ``pagination`` middleware works well:

..  code-block:: console

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'pagination.middleware.PaginationMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

* Copy the tuple ``INSTALLED_APPS`` from ``openremproject/settings.py`` to ``openremproject/local_settings.py``
* In ``openremproject/local_settings.py``, add ``'debug_toolbar',``. The order is not important:

..  code-block:: console

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'remapp',
    'django_filters',
    'pagination',
    'django.contrib.humanize',
    'solo',
    'crispy_forms',
    'django_js_reverse',
    'debug_toolbar',
)

Add the following line to ``openremproject/local_settings.py``:

.. sourcecode:: console

    INTERNAL_IPS= ['127.0.0.1']

If you wish to make use of the debug toolbar on machines other than the one the code is running on, change the
INTERNAL_IPS address list to include your client machine.

Using Django Debug Toolbar
--------------------------

When ``DEBUG = True`` in ``openremproject/local_settings.py`` the toolbar should appear.