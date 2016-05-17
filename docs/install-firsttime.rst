***********************
First time installation
***********************

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

We strongly recommend using PostgreSQL as the database for OpenREM, though there are other options. This is covered in
the installation prep documents at :ref:`installpreppostgres` instructions.

If you do use PostgreSQL, the following docs will be useful - there are also linked to from the installaton prep docs:

..  toctree::
    :maxdepth: 2

    postgresql
    postgresql_windows