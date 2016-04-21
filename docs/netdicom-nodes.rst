###########################
DICOM Network Configuration
###########################

****************************************
Configuring DICOM store nodes in OpenREM
****************************************

You need to configure one or more DICOM Store nodes (Store Service Class Provider, or Store SCP) if you want either of
the following:

* OpenREM to provide DICOM store functionality
* OpenREM to be able to query retrieve a third-party system (PACS or modality), using the OpenREM Store SCP or a third
  party one, such as Conquest

To configure a DICOM Store SCP, on the ``Config`` menu select ``DICOM network configuration``, then click
``Add new Store`` and fill in the details:

.. image:: img/netdicomstorescp.png
    :align: center
    :alt: DICOM Store SCP configuration

* Name of local store node: This is the *friendly name*, such as ``OpenREM store``
* Application Entity Title of the node: This is the DICOM name for the store, and must be letters or numbers only, no
  spaces, and a maximum of 16 characters
* Port for store node: Port 104 is the reserved DICOM port, but it is common to use *high* ports such as 8104, partly
  because ports up to 1024 usually need more privileges than for the high ports. However, if there is a firewall
  between the remote nodes (modalities, PACS) and the OpenREM server, then you need to make sure that the firewall is
  configured to allow the port you choose here


******************************************
Native DICOM store node with direct import
******************************************

.. Warning::

    Native DICOM store functionality has not proved to be stable over long periods. Therefore we cannot recommend that
    you use this feature in a production environment. However, please do test it and help us to improve it if you are
    able to!


An OpenREM DICOM Store SCP (service class provider) enable modalities or PACS to send DICOM structured reports and images
directly to OpenREM where they are imported into the database.

The Store SCP service receives the data, checks whether it is one of the objects that OpenREM can extract data from,
and starts an import task if applicable.

The object is then left in the ``dicom_in`` folder in the ``media`` folder, or it is deleted, depending on the policy
set in :doc:`i_deletesettings`.


For native DICOM store nodes, you need to open the ``Advanced - test/development use only`` section:

* Control the server using OpenREM: this checkbox will enable OpenREM to create and control the node
* Autostart and keep-alive: Using celery beat the server can be started automatically and restarted automatically if
  this box is ticked..
* Auto-start the server using celery beat: if checked, and if :ref:`celery-beat` is running, then OpenREM will attempt
  to start the store node whenever it finds it not to be running.



************************************************************
Third-party DICOM store node with scripted import to OpenREM
************************************************************

If you are using Conquest or another third-party Store SCP to collect DICOM data, simply fill in the basic details as
above without configuring the settings in the ``Advanced`` section. This will enable you to request remote hosts send
data to your Store SCP in the *retrieve* part of the query-retrieve operation.



****************************************************************
Query retrieve of third-party system, such as a PACS or modality
****************************************************************

To Query-Retrieve a remote host, you will need both a local Store SCP configured as well as a remote host.