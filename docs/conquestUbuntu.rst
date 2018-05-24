#########################################
Conquest DICOM store node on Ubuntu 16.04
#########################################

************
Installation
************

Ubuntu 16.04 has the Conquest DICOM server `in its repositories,`_ so this makes
installation very easy. However, it isn't the latest version and isn't going to be updated further. However, if you are
using Ubuntu 16.04 then it does make for a relatively easy install.

There are options to install with different databases – for OpenREM we're not really going to use the
database so the easiest option is to use SQLite:

.. sourcecode:: console

    sudo apt-get install conquest-sqlite


*******************
Basic configuration
*******************

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

If you are pasting from the clipboard into nano from within Linux, use ``Shift-Ctrl-v``. If you are using
PuTTY in Windows to interact with Ubuntu, a right click on the mouse or ``Shift-Insert`` should paste the text into the
terminal.

To save and exit from nano, use ``Ctrl-o`` (out), press return to confirm the filename and then ``Ctrl-x`` (exit).

Configuration
=============

Here will be a link to the dicom.ini config... the text below will be subsumed into it






Configure the Store SCP
=======================

Edit the ``dicom.ini`` file in the ``/etc/conquest-dicom-server`` folder, for example

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/dicom.ini

Modify the following lines as required. The server name field – with the Conquest default of ``CONQUESTSRV1`` – is the
AE Title, so should be 16 characters or less and consist of letters and numbers with no spaces. It is case
insensitive. The ``TCPPort`` is normally either 104, the standard DICOM port, or any number greater than
1023.

.. sourcecode:: console

    # Network configuration: server name and TCP/IP port#
    MyACRNema                = CONQUESTSRV1
    TCPPort                  = 11112

Again, save and exit.

If you've changed the AE Title and/or port, restart conquest:

.. sourcecode:: console

    sudo /etc/init.d/dgate restart


***************************
Testing basic configuration
***************************

Test the Store SCP by returning to OpenREM and navigating to ``Config`` -> ``DICOM network configuration``.

Click to ``Add new store`` and enter the AE title and port you have set, along with a reference name.

Click to ``Submit``, and you will return to the summary page which should inform you if the server is running.


***************************************
Configure Conquest to work with OpenREM
***************************************

The next stage is to configure Conquest to store the incoming object and ask OpenREM to process them.


Conquest configuration
======================

At the end of the ``/etc/conquest-dicom-server/dicom.ini`` file, add the following lines. You will need
to tailor them to save the file to an appropriate place. The ``_conquest`` user will need to be able to
write to that location. You will also need to make sure the path to the scripts you just created are correct.

The example below assumes images will be saved in ``/var/lib/conquest-dicom-server/incoming/``, which you can create as
follows:

.. sourcecode:: console

    sudo mkdir /var/lib/conquest-dicom-server/incoming
    sudo chown _conquest:_conquest /var/lib/conquest-dicom-server/incoming

Each instruction in the ``dicom.ini`` file below has a ``destroy`` instruction to delete Conquest's copy of the file
and to remove it from it's database. This isn't the version we've saved in ``incoming`` to process.

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/dicom.ini

.. sourcecode:: console

    # RDSR
    ImportConverter0  = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.67"; {save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-rdsr.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy}
    # Import arguments for GE CT - uses Enhanced SR instead of Radiation Dose SR
    ImportConverter1  = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.22"; {save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-rdsr.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy}

    # MG images
    ImportModality2   = MG
    ImportConverter2  = save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-mg.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy

    # DX images
    ImportModality3   = DX
    ImportConverter3  = save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-dx.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy
    # CR images
    ImportModality4   = CR
    ImportConverter4  = save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-dx.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy

    # Philips CT
    ImportConverter5  = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.7"; {save to /var/lib/conquest-dicom-server/incoming/%o.dcm; system /etc/conquest-dicom-server/openrem-ctphilips.sh /var/lib/conquest-dicom-server/incoming/%o.dcm; destroy}

    # Other objects
    ImportConverter6  = destroy

Finally, restart conquest to make use of the new settings:

.. sourcecode:: console

    sudo /etc/init.d/dgate restart


.. _`in its repositories,`: http://packages.ubuntu.com/search?keywords=conquest