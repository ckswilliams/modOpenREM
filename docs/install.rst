******************
Installing OpenREM
******************

Install OpenREM 0.8.0b1
=======================

.. sourcecode:: bash

    pip install openrem==0.8.0b1

*Will need ``sudo`` or equivalent if installing on linux without using a virtualenv*

.. _localsettingsconfig:

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

    The directories in this local_settings.py file must already exist - OpenREM will not create them for you.

Database
^^^^^^^^

.. Note::

    SQLite is great for getting things running quickly and testing if the setup works,
    but is not recommended for production use.

    We recommend using `PostgreSQL <http://www.postgresql.org>`_ as it is the best supported
    database for Django, **and the only one for which the median value will be calculated and
    displayed in OpenREM charts.** Alternatively, other databases such as MySQL/MariaDB, Oracle, and
    some others with lower levels of support can be used.

    There are some further guides to setting up PostgreSQL – see :ref:`databaselinks`

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

.. _mediarootsettings:

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

Customised date format in xlsx exports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# TODO: check csv situation
The default date form at for OpenREM xlsx exports is dd/mm/yyyy. If you wish to customise this, uncomment the
`XLSX_DATE` line, for example the standard US date format would be::

    XLSX_DATE = 'mm/dd/yyyy'

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
    LOGGING['handlers']['extractor_file']['filename'] = extractorfilename  # Extractor logs

If you want all the logs in one file, simply set them all to the same filename.

In the settings file, there are ``simple`` and ``verbose`` log message styles. We recommend you leave these as
``verbose``:

.. sourcecode:: python

    LOGGING['handlers']['file']['formatter'] = 'verbose'        # General logs
    LOGGING['handlers']['qr_file']['formatter'] = 'verbose'     # Query Retrieve SCU logs
    LOGGING['handlers']['store_file']['formatter'] = 'verbose'  # Store SCP logs
    LOGGING['handlers']['extractor_file']['formatter'] = 'verbose'  # Extractor logs

Next, you can set the logging level. Options are ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, and ``CRITICAL``, with
progressively less logging. ``INFO`` is probably a good choice for most circumstances. ``DEBUG`` is useful if something
is going wrong, but it is quite chatty for routine use!

.. sourcecode:: python

    LOGGING['loggers']['remapp']['level'] = 'INFO'                    # General logs
    LOGGING['loggers']['remapp.netdicom.qrscu']['level'] = 'INFO'     # Query Retrieve SCU logs
    LOGGING['loggers']['remapp.netdicom.storescp']['level'] = 'INFO'  # Store SCP logs
    LOGGING['loggers']['remapp.extractors.rdsr_toshiba_ct_from_dose_images']['level'] = 'INFO'  # Toshiba RDSR creation extractor logs

Finally, if you are using Linux you can set the system to start a new log file automatically when the current one
gets to a certain size. The settings described below don't work with Windows - we'll try to include Windows settings in
the next release. See `issue 483`_ to find out the progress on this!

To activate the 'rotating' log function, uncomment the remaining lines by removing the ``#`` from the beginning of
the lines. For example for the query retrieve logs:

.. sourcecode:: python

    LOGGING['handlers']['qr_file']['class'] = 'logging.handlers.RotatingFileHandler'
    LOGGING['handlers']['qr_file']['maxBytes'] = 10 * 1024 * 1024  # 10*1024*1024 = 10 MB
    LOGGING['handlers']['qr_file']['backupCount'] = 5  # number of log files to keep before deleting the oldest one

Time zone
^^^^^^^^^

Configure the local timezone in order to get correct times in the logfiles.
The default timezone is set at 'Europe/London'. Valid options can be found here:
http://en.wikipedia.org/wiki/List_of_tz_zones_by_name

.. sourcecode:: python

    TIME_ZONE = 'Europe/London'

Language
^^^^^^^^

Configure the local language. Default language is set at us-english. Valid options can be found here:
http://www.i18nguy.com/unicode/language-identifiers.html

.. sourcecode:: python

    LANGUAGE_CODE = 'en-us'

.. _toshiba_configuration:

Toshiba CT RDSR creation
^^^^^^^^^^^^^^^^^^^^^^^^

If you need to import data from older Toshiba CT scanners into OpenREM then the following tools need to be available
on the same server as OpenREM:

    * The `Offis DICOM toolkit`_
    * `Java`_
    * pixelmed.jar from the `PixelMed Java DICOM Toolkit`_

The paths to these must be set in ``local_settings.py`` for your system:

.. sourcecode:: python

    # Locations of various tools for DICOM RDSR creation from CT images
    DCMTK_PATH = 'C:/Apps/dcmtk-3.6.0-win32-i386/bin'
    DCMCONV = os.path.join(DCMTK_PATH, 'dcmconv.exe')
    DCMMKDIR = os.path.join(DCMTK_PATH, 'dcmmkdir.exe')
    JAVA_EXE = 'C:/Apps/doseUtility/windows/jre/bin/java.exe'
    JAVA_OPTIONS = '-Xms256m -Xmx512m -Xss1m -cp'
    PIXELMED_JAR = 'C:/Apps/doseUtility/pixelmed.jar'
    PIXELMED_JAR_OPTIONS = '-Djava.awt.headless=true com.pixelmed.doseocr.OCR -'

The example above is for Windows. On linux,
if you have installed the Offis DICOM toolkit with ``sudo apt install dcmtk`` or similar, you can find the path for the
configuration above using the command ``which dcmconv``. This will be something like ``/usr/bin/dcmconv``, so the
``DCMTK_PATH`` would be ``'/usr/bin`` and the ``DCMCONV`` would be ``os.path.join(DCMTK_PATH, 'dcmconv')``. Similarly
for ``DCMMKDIR`` and ``JAVA_EXE``, which might be ``/usr/bin/java``. The pixelmed.jar file should be downloaded from
the link above, and you will need to provide the path to where you have saved it.

.. _database_creation:

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

    remapp/migrations/0002_0_7_fresh_install_add_median.py.inactive

to

.. sourcecode:: console

    remapp/migrations/0002_0_7_fresh_install_add_median.py

and then run

.. sourcecode:: console

    python manage.py migrate

This command runs the migration file, and will display the text
``Applying remapp.0002_0_7_fresh_install_add_median... OK``, indicating that the median function has been added.

Start all the services!
=======================

You are now ready to start the services to allow you to use OpenREM - go to :doc:`startservices` to see how!


Further instructions
====================



DICOM Store and query-retrieve
------------------------------

The best (and only practical way in a production environment) to get DICOM data into OpenREM is to have a DICOM store
node (Store Service Class Provider/SCP) and possibly a query-retrieve service class user too.

To find out more about this, refer to the :doc:`netdicom` docs.


.. _`Offis DICOM toolkit`: http://dicom.offis.de/dcmtk.php.en
.. _`Java`: http://java.com/en/download/
.. _`PixelMed Java DICOM Toolkit`: http://www.pixelmed.com/dicomtoolkit.html
.. _`issue 483`: https://bitbucket.org/openrem/openrem/issues/483/add-automatic-zipping-of-log-files