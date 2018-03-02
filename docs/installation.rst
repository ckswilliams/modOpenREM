************
Installation
************

..  toctree::
    :maxdepth: 2

    install-prep
    install

A standard installation assumes access to the internet from the computer where OpenREM is being installed. Sometimes
this isn't possible, so we've added instructions for an offline installation too. Currently it focuses on Windows only
(for the server - the computer connected to the internet can be running any operating system).

..  toctree::
    :maxdepth: 2

    install-offline

Upgrading an existing installation
==================================

..  toctree::
    :maxdepth: 2

    release-0.8.0

.. _databaselinks:

Databases
=========

During the installation process, you will need to install a database. For testing only, you can use the built in
SQLite3 database, but for production use you will need a production grade database. This is covered in the
:doc:`install-prep` documentation, but as you will probably want to find the database instructions again, the links
are repeated here.

..  toctree::
    :maxdepth: 2

    postgresql
    postgresql_windows
    backupMySQLWindows


Web servers
===========

Unlike the database, the production webserver can be left till later and can be changed again at any time. However,
for performance it is recommended that a production webserver is used instead of the inbuilt 'runserver'.

On Windows or Linux, it is possible to use `Apache <http://httpd.apache.org>`_, however for reasons relating to how
Python, Apache and mod_wsgi are compiled using old Microsoft tools, this is now nearly impossible to do on the Windows
platform. There is no reason for existing Windows installs with Apache to change webserver, but in case it is useful our
guide to :doc:`apache_on_windows` is available, but no longer recommended for new installs.

For Apache installs on Linux, the
`django website <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/>`_ has instructions and links to
get you set up.

Our recommendations for Windows and Linux are:

..  toctree::
    :maxdepth: 1

    iis_on_windows
    nginx_on_linux
