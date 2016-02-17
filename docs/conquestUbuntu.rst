###################################
Conquest DICOM store node on Ubuntu
###################################

************
Installation
************

Ubuntu has reasonably up to date versions of the Conquest DICOM server `in its repositories,`_ so this makes
installation very easy.

There are options to install with different database options - for OpenREM we're not really going to use the
database so the easiest option is to use SQLite:

.. sourcecode:: console

    sudo apt-get install conquest-sqlite

The install process will create a folder ``/etc/conquest-dicom-server``, then create the database file and
settings files there.


*************
Configuration
*************

Modify dgatesop.lst
===================

Edit the ``dgatesop.lst`` file in the ``/etc/conquest-dicom-server`` folder, for example

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/dgatesop.lst

And add the following line

.. sourcecode:: console

    XRayRadiationDoseSR 1.2.840.10008.5.1.4.1.1.88.67   sop

It isn't critical where it goes, but I tend to add it where it belongs between
``KeyObjectSelectionDocument`` and ``PETStorage``. I also add in the spaces to make it line up, but
again this is just for aesthetic reasons!

Save the file and exit - if you used nano the commands are ``Ctrl-o`` and ``Ctrl-x``.

Configure the Store SCP
=======================

Edit the ``dicom.ini`` file in the ``/etc/conquest-dicom-server`` folder, for example

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/dicom.ini

Modify the following lines as required. The server name field, with the Conquest default of ``CONQUESTSRV1`` is the AE
Title, so should be 16 characters or less and consist of letters and numbers with no spaces. It is case
insensitive. The ``TCPPort`` is normally either 104, the standard DICOM port, or any number greater than
1023.

.. sourcecode:: console

    # Network configuration: server name and TCP/IP port#
    MyACRNema                = CONQUESTSRV1
    TCPPort                  = 11112

Again, save and exit.


.. _`in its repositories,`: http://packages.ubuntu.com/search?keywords=conquest