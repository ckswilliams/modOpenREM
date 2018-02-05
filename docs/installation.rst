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