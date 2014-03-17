Installation instructions
*************************


Quick setup
===========
..  Note::
    Most path names are represented using the linux convention of a ``/`` separator.
    If you are installing in a Windows environment you will need to use the Windows ``\`` separator.


#. Install python (might need to be 2.7)
#. Install `setuptools and pip <http://www.pip-installer.org/en/latest/installing.html>`_
#. Install OpenREM
    + ``pip install OpenREM-ver.tar.gz``
#. Configure OpenREM
    + Locate install location, typically ``something/lib/python2.7/site-packages/openrem``
    + There are two files that need renaming:
        + ``openrem/openrem/settings.py.example`` to ``openrem/openrem/settings.py``
        + ``openrem/openrem/wsgi.py.example`` to ``openrem/openrem/wsgi.py``
    + in the ``settings.py`` file, set the database details.
    + For testing ONLY, use 
        + ``'ENGINE': 'django.db.backends.sqlite3',``
        + ``'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO'``
            + Windows example: ``'NAME': 'C:\Documents\User\OpenREM\openrem.db'``
            + Linux example: ``'NAME': '/var/openrem/openrem.db'``
#. Create the database
    + ``python path/to/openrem/manage.py syncdb``
    + (optional when just testing) ``python path/to/openrem/manage.py convert_to_south remapp``
#. Start test web server
    + ``python path/to/openrem/manage.py runserver``
    + If you are using a headless server and need to be able to see the 
      web interface from another machine, use 
      ``python path/to/openrem/manage.py runserver x.x.x.x:8000`` replacing the 
      'x' with the IP address of the server and '8000' with the port you wish to use.
#. Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)
#. Add some data!
    + ``openrem_rdsr.py rdsrfile.dcm``
#. Add some users *New in version 0.4.0*
    + Go to the admin interface (eg http://localhost:8000/admin) and log in with the user created when you created the database (``syncdb``)
    + Create some users and add them to the appropriate groups (if there are no groups, go to the OpenREM homepage and they should be created).
        + ``viewgroup`` can browse the data only
        + ``exportgroup`` can do as view group plus export data to a spreadsheet, and will be able to import height and weight data in due course (See `Issue #21 <https://bitbucket.org/edmcdonagh/openrem/issue/21/>`_)
        + ``admingroup`` can do as export group, and will be able to delete studies in due course (See `Issue #18 <https://bitbucket.org/edmcdonagh/openrem/issue/18/>`_)

More in depth process
=====================

#. Install `virtualenv`_ or maybe `virtualenvwrapper`_
    Recommended if the server is ever going to be used for more than one 
    python application -- virtualenv sets up an isolated python environment

#. Install OpenREM
    As per the `Quick setup`_ instructions above. Don't configure OpenREM yet

#. Install a production database
    SQLite is great for getting things running quickly and testing if the setup works,
    but is really not recommended for production use on any scale. Therefore it is
    recommended to use a different database such as `PostgreSQL <http://www.postgresql.org>`_ or 
    `MySQL <http://www.mysql.com>`_.
    
    Here are instructions for installing PostgreSQL on linux and on Windows:
    
    ..  toctree::
        :maxdepth: 1
        
        postgresql
        postgresql_windows


#. Install and configure a production webserver
    Unlike the database, the production webserver can be left till later and
    can be changed again at any time.
    
    However, for performance it is recommended that a production webserver is
    used. Popular choices would be either `Apache <http://httpd.apache.org>`_ or you can do as the cool kids
    do and use `Gunicorn with nginx <http://www.robgolding.com/blog/2011/11/12/django-in-production-part-1---the-stack/>`_.

#. Configure OpenREM
    Follow the 'Configure OpenREM' instuctions in the `Quick setup`_ section above, but this time with 
    the production database details.
    
    Configure the production webserver too.

#. Create the database
    + ``python path/to/openrem/manage.py syncdb``

    .. _convert-to-south:
#. Convert the database to use South
    South is a django application to manage database migrations. Using
    South means that future changes to the database model can be calculated
    and executed automatically with simple commands when OpenREM is upgraded.

    + ``python path/to/openrem/manage.py convert_to_south remapp``

Related guides
==============

    ..  toctree::
        :maxdepth: 1
        
        conquestAsWindowsService
        backupMySQLWindows


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
