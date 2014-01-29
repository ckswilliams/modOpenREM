Installation instructions
*************************


Quick setup
===========

#. Install python (might need to be 2.7)
#. Install `setuptools and pip <http://www.pip-installer.org/en/latest/installing.html>`_
#. Install OpenREM
    + ``pip install OpenREM-ver.tar.gz``
#. Configure OpenREM
    + Locate install location, typically ``something/lib/python2.7/site-packages/openrem``
    + There are two files that need renaming:
        + ``openrem/openrem/settings.py.example`` to ``openrem/openrem/settings.py.example``
        + ``openrem/openrem/wsgi.py.example`` to ``openrem/openrem/wsgi.py.example``
    + in the ``settings.py`` file, set the database details.
    + For testing ONLY, use 
        + ``'ENGINE': 'django.db.backends.sqlite3',``
        + ``'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO'``
#. Create the database
    + ``python path/to/openrem/manage.py syncdb``
    + (optional for a test database) ``python path/to/openrem/manage.py convert_to_south remapp``
#. Start test web server
    + ``python path/to/openrem/manage.py runserver``
#. Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)
#. Add some data!
    + ``openrem_rdsr rdsrfile.dcm``

More in depth process
=====================

+ Install `virtualenv`_ or maybe `virtualenvwrapper`_
    Recommended if the server is ever going to be used for more than one 
    python application -- virtualenv sets up an isolated python environment

+ Install OpenREM
    As per the `Quick setup`_ instructions above. Don't configure OpenREM yet

+ Install and configure a production database
    SQLite is great for getting things running quickly and testing if the setup works,
    but is really not recommended for production use on any scale. Therefore it is
    recommended to use a different database such as PostgreSQL or MySQL.
    
    Instructions for installing and configuring these can be found at these links:

    + PostgreSQL
    + MySQL
    
    Alternatively, here are the authors instructions for installing PostgreSQL on linux:
    

    ..  toctree::
        :maxdepth: 1
        
        postgresql


Install and configure a production webserver
--------------------------------------------

Configure OpenREM
-----------------

Create the database
-------------------



.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
