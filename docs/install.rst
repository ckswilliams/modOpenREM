*************************
Installation instructions
*************************

Install OpenREM 0.7 beta version
================================

.. Warning::

    This is a beta version for developer testing. It is not suitable for general use, and the instructions below are
    likely to be incorrect.

.. sourcecode:: bash

    pip install openrem==0.7.0b5

*Will need ``sudo`` or equivalent if installing on linux without using a virtualenv*

Configuration
=============

Locate install location
-----------------------

* Linux Ubuntu: ``/usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``
* Virtualenv: ``lib/python2.7/site-packages/openrem/``

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

Database
^^^^^^^^

For testing you can use the SQLite3 database

.. sourcecode:: python

    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO',

* Linux example: ``'NAME': '/home/user/openrem/openrem.db',``
* Windows example: ``'NAME': 'C:/Users/myusername/Documents/OpenREM/openrem.db',``

.. Note::

    SQLite is great for getting things running quickly and testing if the setup works,
    but is not recommended for production use.

    We recommend using `PostgreSQL <http://www.postgresql.org>`_ as it is the best supported
    database for Django, **and the only one for which the median value will be calculated and
    displayed in OpenREM charts.** Alternatively, other databases such as MySQL/MariaDB, Oracle, and
    some others with lower levels of support can be used.

    There are some further guides to setting up PostgreSQL – see `Database options`_ below

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

Keep or delete processed DICOM files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Should DICOM files be kept or deleted when they have been processed?

* ``RM_DCM_NOMATCH`` is only applicable if you use the DICOM Store SCP built into OpenREM
* The other settings determine whether Radiation Dose Structured Reports, Mammography images, Radiography images and
  Philips CT images are kept (``False``) or deleted (``True``) when they have been processed
* The default setting is False, to preserve behaviour from previous versions::

    RM_DCM_NOMATCH = True
    RM_DCM_RDSR = True
    RM_DCM_MG = True
    RM_DCM_DX = True
    RM_DCM_CTPHIL = True

.. Note::

    It is recommended that the image file types and ``RM_DCM_NOMATCH`` are set to ``True``, as they can fill the disk
    quickly if they are allowed to build up!

See :doc:`netdicom` (docs not yet up to date with features)

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
    sessions
     [X] 0001_initial
    sites
     [X] 0001_initial

Finally, create a Django super user::

    python manage.py createsuperuser

Answer each question as it is asked – this user is needed to set up the other users and the
permissions.

Add the median database function: PostgreSQL database only
----------------------------------------------------------

Rename the ``0002_fresh_openrem_install_add_median_function.py.inactive`` file
in the ``migrations`` folder to ``0002_fresh_openrem_install_add_median_function.py``
then do the following:

Windows::

	python manage.py makemigrations --empty remapp
	python manage.py migrate

The first command will create a skeleton ``0001_initial.py`` migration file. The
second command runs the migration files, and will display the text
``Applying remapp.0002_fresh__openrem_install_add_median_function... OK``, indicating
that the median function has been added.



Further instructions
====================

Database options
----------------

SQLite is great for getting things running quickly and testing if the setup works,
but is really not recommended for production use on any scale. Therefore it is
recommended to use a different database such as `PostgreSQL <http://www.postgresql.org>`_ or 
`MySQL <http://www.mysql.com>`_.

Here are instructions for installing PostgreSQL on linux and on Windows:

..  toctree::
    :maxdepth: 1
    
    postgresql
    postgresql_windows

..  _convert-to-south:

Database migrations
-------------------

South is a django application to manage database migrations. Using
South means that future changes to the database model can be calculated
and executed automatically with simple commands when OpenREM is upgraded.

Production webservers
---------------------

Unlike the database, the production webserver can be left till later and
can be changed again at any time.

For performance it is recommended that a production webserver is used instead of the inbuilt 'runserver'.
Popular choices would be either `Apache <http://httpd.apache.org>`_ or you can do as the cool kids
do and use `Gunicorn with nginx <http://www.robgolding.com/blog/2011/11/12/django-in-production-part-1---the-stack/>`_.

The `django website <https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/>`_ 
has instructions and links to get you set up with Apache.

Daemonising Celery
------------------

In a production environment, Celery will need to start automatically and
not depend on a particular user being logged in. Therefore, much like
the webserver, it will need to be daemonised. For now, please refer to the
instructions and links at http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html.

Virtualenv and virtualenvwrapper
--------------------------------

If the server is to be used for more than one python application, or you 
wish to be able to test different versions of OpenREM or do any development,
it is highly recommended that you use `virtualenv`_ or maybe `virtualenvwrapper`_

Virtualenv sets up an isolated python environment and is relatively easy to use.

If you do use virtualenv, all the paths referred to in the documentation will
be changed to:

* Linux: ``lib/python2.7/site-packages/openrem/``
* Windows: ``Lib\site-packages\openrem``

In Windows, even when the virtualenv is activated you will need to call `python`
and provide the full path to script in the `Scripts` folder. If you call the
script (such as `openrem_rdsr.py`) without prefixing it with `python`, the
system wide Python will be used instead. This doesn't apply to Linux, where
once activated, the scripts can be called without a `python` prefix from anywhere. 


Related guides
==============

    ..  toctree::
        :maxdepth: 1
        
        conquestAsWindowsService
        backupMySQLWindows
        backupRestorePostgreSQL
        conquestImportConfig
        conquestAddRDSR

Advanced guides for developers
------------------------------

    ..  toctree::
        :maxdepth: 1
        
        apache_on_windows


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _(What is south?): `Database migrations`_
.. _consider virtualenv: `Virtualenv and virtualenvwrapper`_
