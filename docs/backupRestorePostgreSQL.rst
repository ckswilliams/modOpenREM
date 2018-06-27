Backing up a PostgreSQL database (Windows)
==========================================

..  Note::  Content contributed by DJ Platten

These instructions are based on PostgreSQL 9.1 and OpenREM 0.5.0 running on Windows Server 2008. The database restore has been tested on Ubuntu 12.04 LTS.


Create a PostgreSQL user called ``backup`` with a password of ``backup``. This is easiest to do using the ``pgAdminIII`` tool: you'll need to create a new login role.
In the role privileges ensure that at least ``Can login``, ``Superuser`` and ``Can initiate streaming replication and backups`` are checked.

The ``pgAdminIII`` tool is available by default on Windows, but needs to be explicitly installed if using Ubuntu with the following command:

..  code-block:: posh

    sudo apt-get install pgadmin3

For the remainder of this article I'm going to assume that your OpenREM database is called ``openrempostgresql``.

To backup the contents of ``openrempostgresql`` to a file called ``backup.sql`` run the following at the command line in a command prompt (Windows), or terminal window (Ubuntu):

..  code-block:: posh

    pg_dump -U backup -F c -b -v -f backup.sql openrempostgresql

You will need to add your ``C:\path\to\postgres\bin`` folder to the ``path`` environment variable for this to work. Make sure to use the actual path to your PostgreSQL ``bin``
folder rather than the example text provided here. See http://www.computerhope.com/issues/ch000549.htm for instructions on editing the path environment variable.


The ``-U backup`` indicates that the ``backup`` user is to carry out the task. The ``-F c`` option archives in a suitable format for input into the ``pg_restore`` command. Further information on ``pg_dump`` and backing up a PostgreSQL database can be found here: http://www.postgresql.org/docs/9.3/static/app-pgdump.html and here: http://www.postgresql.org/docs/9.3/static/backup-dump.html

Restoring a PostgreSQL database (Windows)
=========================================

The ``pg_restore`` command can be used to restore the database using one of the backed-up SQL files that were produced using the ``pg_dump`` command.

Use the ``pgAdminIII`` tool to ensure that there is a PostgreSQL user called ``openremuser``.

Use ``pgAdminIII`` to create a database called ``openrempostgresql``; set the owner to ``openremuser`` and the encoding to ``UTF8``.

Run the following command in a command prompt window (Windows) or terminal window (Ubuntu) to restore the contents of ``backupFile`` to the ``openrempostgresql`` database, where ``backupFile`` is the file created by the ``pg_dump`` command:

..  code-block:: posh

    pg_restore -U postgres -d openrempostgresql backupFile

Ensure that ``openremuser`` has an entry in PostgreSQL’s ``pg_hpa.conf`` file for md5 authentication:

..  code-block:: posh

    local all openremuser md5

The PostgreSQL server will need to be restarted if you have changed ``pg_hpa.conf``.

See http://www.postgresql.org/docs/9.3/static/backup-dump.html#BACKUP-DUMP-RESTORE for further details.
