******************
Installing OpenREM
******************

Install OpenREM 0.7 beta version
================================

.. Warning::

    This is a beta version for developer testing. It is not suitable for general use, and the instructions below are
    likely to be incorrect.

.. sourcecode:: bash

    pip install openrem==0.7.0b12

*Will need ``sudo`` or equivalent if installing on linux without using a virtualenv*

Configuration
=============

Locate install location
-----------------------

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``Lib\site-packages\openrem\``


There are two files that need renaming:

+ ``openremproject/local_settings.py.example`` to ``openremproject/local_settings.py``
+ ``openremproject/wsgi.py.example`` to ``openremproject/wsgi.py``


Edit local_settings.py
----------------------

..  Note::

    Windows notepad will not recognise the Unix style line endings.
    Please use an editor such as Notepad++ or Notepad2 if you can, else use WordPad –
    on the View tab you may wish to set the Word wrap to 'No wrap'

..  Important::
    In local_settings.py, always use forward slashes and not backslashes, even for paths on
    Windows systems.

    The directories in this local_settings file must already exist - OpenREM will not create them for you.

Database
^^^^^^^^

.. Note::

    SQLite is great for getting things running quickly and testing if the setup works,
    but is not recommended for production use.

    We recommend using `PostgreSQL <http://www.postgresql.org>`_ as it is the best supported
    database for Django, **and the only one for which the median value will be calculated and
    displayed in OpenREM charts.** Alternatively, other databases such as MySQL/MariaDB, Oracle, and
    some others with lower levels of support can be used.

    There are some further guides to setting up PostgreSQL – see `Database guides`_ below

If you are using SQLite:

.. sourcecode:: python

    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO',

* Linux example: ``'NAME': '/home/user/openrem/openrem.db',``
* Windows example: ``'NAME': 'C:/Users/myusername/Documents/OpenREM/openrem.db',``

If you are using PostgreSQL:

.. sourcecode:: python

    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'openremdb',
    'USER': 'openremuser',
    'PASSWORD': 'openrem_pw',

Location for imports and exports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Csv and xlsx study information exports and patient size csv imports are
written to disk at a location defined by ``MEDIA_ROOT``.

The path set for ``MEDIA_ROOT`` is up to you, but the user that runs the
webserver must have read/write access to the location specified because
it is the webserver than reads and writes the files. In a debian linux,
this is likely to be www-data for a production install. Remember to use
forward slashes for the config file, even for Windows.

Linux example::

    MEDIA_ROOT = "/var/openrem/media/"

Windows example::
    
    MEDIA_ROOT = "C:/Users/myusername/Documents/OpenREM/media/"


Secret key
^^^^^^^^^^

Generate a new secret key and replace the one in the ``local_settings.py`` file. You can use
http://www.miniwebtool.com/django-secret-key-generator/ for this.

Allowed hosts
^^^^^^^^^^^^^

The ``ALLOWED_HOSTS`` needs to be defined, as the ``DEBUG`` mode is now
set to ``False``. This needs to contain the server name or IP address that
will be used in the URL in the web browser. For example::

    ALLOWED_HOSTS = [
        '192.168.56.102',
        '.doseserver.',
        'localhost',
    ]

A dot before a hostname allows for subdomains (eg www.doseserver), a dot
after a hostname allows for FQDNs (eg doseserver.ad.trust.nhs.uk).
Alternatively, a single ``'*'`` allows any host, but removes the security
the feature gives you.

.. _local_settings_logfile:

Log file
^^^^^^^^

There are two places logfiles need to be configured - here and when starting Celery. The logs defined here capture
most of the information; the Celery logs just capture workers starting and tasks starting and finishing.

Configure the filename to determine where the logs are written. In linux, you might want to send them to a sub-folder of
``/var/log/``. In this example, they are written to the ``MEDIA_ROOT``; change as appropriate:

.. sourcecode:: python

    import os
    logfilename = os.path.join(MEDIA_ROOT, "openrem.log")
    qrfilename = os.path.join(MEDIA_ROOT, "openrem_qr.log")
    storefilename = os.path.join(MEDIA_ROOT, "openrem_store.log")
    LOGGING['handlers']['file']['filename'] = logfilename          # General logs
    LOGGING['handlers']['qr_file']['filename'] = qrfilename        # Query Retrieve SCU logs
    LOGGING['handlers']['store_file']['filename'] = storefilename  # Store SCP logs

If you want all the logs in one file, simply set them all to the same filename.

In the settings file, there are ``simple`` and ``verbose`` log message styles. We recommend you leave these as
``verbose``:

.. sourcecode:: python

    LOGGING['handlers']['file']['formatter'] = 'verbose'        # General logs
    LOGGING['handlers']['qr_file']['formatter'] = 'verbose'     # Query Retrieve SCU logs
    LOGGING['handlers']['store_file']['formatter'] = 'verbose'  # Store SCP logs

Finally you can set the logging level. Options are ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, and ``CRITICAL``, with
progressively less logging.

.. sourcecode:: python

    LOGGING['loggers']['remapp']['level'] = 'INFO'                    # General logs
    LOGGING['loggers']['remapp.netdicom.qrscu']['level'] = 'INFO'     # Query Retrieve SCU logs
    LOGGING['loggers']['remapp.netdicom.storescp']['level'] = 'INFO'  # Store SCP logs


Create the database
-------------------

In a shell/command window, move into the openrem folder:

* Ubuntu linux: ``cd /usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``cd /usr/lib/python2.7/site-packages/openrem/``
* Windows: ``cd C:\Python27\Lib\site-packages\openrem\``
* Virtualenv: ``cd lib/python2.7/site-packages/openrem/``

Create the database::

    python manage.py makemigrations remapp
    python manage.py migrate
    python manage.py showmigrations

The last command will list each Django app migrations. Each should have a cross inside
a pair of square brackets something like below::

    admin
     [X] 0001_initial
    auth
     [X] 0001_initial
     [X] 0002_alter_permission_name_max_length
     [X] 0003_alter_user_email_max_length
     [X] 0004_alter_user_username_opts
     [X] 0005_alter_user_last_login_null
     [X] 0006_require_contenttypes_0002
    contenttypes
     [X] 0001_initial
     [X] 0002_remove_content_type_name
    remapp
     [X] 0001_initial
    sessions
     [X] 0001_initial
    sites
     [X] 0001_initial

Finally, create a Django super user::

    python manage.py createsuperuser

Answer each question as it is asked – this user is needed to set up the other users and the
permissions.

Add the median database function: PostgreSQL databases only
-----------------------------------------------------------

Rename the file

.. sourcecode:: console

    remapp/migrations/0002_fresh_openrem_install_add_median_function.py.inactive

to

.. sourcecode:: console

    remapp/migrations/0002_fresh_openrem_install_add_median_function.py

and then run

.. sourcecode:: console

    python manage.py makemigrations --empty remapp
    python manage.py migrate

The first command will create a skeleton ``0001_initial.py`` migration file. The
second command runs the migration files, and will display the text
``Applying remapp.0002_fresh__openrem_install_add_median_function... OK``, indicating
that the median function has been added.

Start all the services!
=======================

You are now ready to start the services to allow you to use OpenREM - go to :doc:`startservices` to see how!


Further instructions
====================

Database guides
---------------

Here are instructions for installing PostgreSQL on linux and on Windows, and guides to backup up PostgreSQL and MySQL:

..  toctree::
    :maxdepth: 1
    
    postgresql
    postgresql_windows
    backupMySQLWindows


Production webservers
---------------------

Unlike the database, the production webserver can be left till later and
can be changed again at any time.

For performance it is recommended that a production webserver is used instead of the inbuilt 'runserver'.
Popular choices would be either `Apache <http://httpd.apache.org>`_ or you can do as the cool kids
do and use `Gunicorn with nginx <http://www.robgolding.com/blog/2011/11/12/django-in-production-part-1---the-stack/>`_.

The `django website <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/>`_
has instructions and links to get you set up with Apache.

An advanced guide using Apache, including auto-restarting the server when the code changes, has been contributed
here: :doc:`apache_on_windows`

Conquest related guides
-----------------------

Previous releases of OpenREM have not had a DICOM Store SCP, and we have recommended using Conquest for this job.
OpenREM now has this functionality built-in, so hopefully the guides below will not be needed!

..  toctree::
    :maxdepth: 1

    conquestAsWindowsService
    conquestImportConfig
    conquestAddRDSR

