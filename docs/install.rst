Installation instructions
*************************


Basic guide
===========

Non-operating system specific path names are represented using the linux 
convention of a ``/`` separator. If you are installing in a Windows environment 
you will need to use the Windows ``\`` separator.

Installation prerequisites
--------------------------

Install python 2.7
``````````````````

* Linux - likely to be installed already
* Windows - https://www.python.org/download/releases

Install `setuptools and pip <http://www.pip-installer.org/en/latest/installing.html>`_

..  Note::

    Before continuing, `consider virtualenv`_

Install RabbitMQ
````````````````
*(New for version 0.4.3)*

* Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
* Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html

For either install, just follow the defaults - no special configurations required.

Install OpenREM
---------------

* ``pip install openrem`` (Needs internet connection)

Configure OpenREM
-----------------

Locate install location

* Linux: ``/usr/lib/python2.7/dist-packages/openrem/`` or ``/usr/lib/python2.7/site-packages/openrem/``
* Windows: ``C:\Python27\Lib\site-packages\openrem\``

There are three files that need renaming: *(changed for 0.4.0)*

+ ``openrem/local_settings.py.example`` to ``openrem/local_settings.py``
+ ``openrem/wsgi.py.example`` to ``openrem/wsgi.py``
+ ``openrem/settings.py.new`` to ``openrem/settings.py`` *Not applicable from 0.4.3 onwards*

In the ``local_settings.py`` file, set the database details, the ``MEDIA_ROOT`` path and the secret key.

Database settings
`````````````````

For testing you can use the SQLite3 database::

    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO',

* Linux example: ``'NAME': '/var/openrem/openrem.db',``
* Windows example: ``'NAME': 'C:\Documents\User\OpenREM\openrem.db',``

For production use, see `Database options`_ below

Location settings for imports and exports
`````````````````````````````````````````

Csv and xlsx study information exports and patient size csv imports are
written to disk at a location defined by ``MEDIA_ROOT``.

The path set for ``MEDIA_ROOT`` is up to you, but the user that runs the
webserver must have read/write access to the location specified because
it is the webserver than reads and writes the files. In a debian linux,
this is likely to be www-data for a production install.


Secret key
``````````

Generate a new secret key and replace the one in the ``local_settings.py`` file. You can use
http://www.miniwebtool.com/django-secret-key-generator/ for this.

Create the database
-------------------

* Linux: ``python /usr/lib/python2.7/dist-packages/openrem/manage.py syncdb``
* Windows: ``python C:\Python27\Lib\site-packages\openrem\manage.py syncdb``

Answer each question as it is asked, do setup a superuser. This username and
password wil be used to log into the admin interface to create the usernames
for using the web interface. See the `Start using it!`_ section below.

Help! I get a ``value too long for type character varying(50)`` error!
    This error with part of the Django auth_permissions system that we are not using, and can safely be ignored.
    This is being tracked as `Issue 62 <https://bitbucket.org/edmcdonagh/openrem/issue/62>`_

For production installs, convert to South `(What is south?)`_

* Linux: ``python /usr/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp``
* Windows: ``python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp``



Start test web server
---------------------

* Linux: ``python /usr/lib/python2.7/dist-packages/openrem/manage.py runserver``
* Windows: ``python C:\Python27\Lib\site-packages\openrem\manage.py runserver``

If you are using a headless server and need to be able to see the 
web interface from another machine, use 
``python /usr/lib/python2.7/dist-packages/openrem/manage.py runserver x.x.x.x:8000`` 
(or Windows equivalent) replacing the ``x`` with the IP address of the server 
and ``8000`` with the port you wish to use.

Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)

Start using it!
---------------

Add some data! (See the :doc:`import` for adding the scripts to the path if this doesn't work)

* ``openrem_rdsr.py rdsrfile.dcm``

Add some users *(New in version 0.4.0)*

* Go to the admin interface (eg http://localhost:8000/admin) and log in with the user created when you created the database (``syncdb``)
* Create some users and add them to the appropriate groups (if there are no groups, go to the OpenREM homepage and they should be created).

    + ``viewgroup`` can browse the data only
    + ``exportgroup`` can do as view group plus export data to a spreadsheet, and will be able to import height and weight data in due course (See `Issue #21 <https://bitbucket.org/edmcdonagh/openrem/issue/21/>`_)
    + ``admingroup`` can delete studies in addition to anything the export group can do

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


Related guides
==============

    ..  toctree::
        :maxdepth: 1
        
        conquestAsWindowsService
        backupMySQLWindows

Advanced guides for developers
------------------------------

    ..  toctree::
        :maxdepth: 1
        
        apache_on_windows


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _(What is south?): `Database migrations`_
.. _consider virtualenv: `Virtualenv and virtualenvwrapper`_
