###########################
DICOM Network Configuration
###########################

*******
General
*******

OpenREM can operate in the following ways regarding DICOM network interfaces:

* Native DICOM store node with direct import
* Third-party DICOM store node with scripted import to OpenREM
* Query retrieve of third-party system, such as a PACS or modality

************************
Native DICOM store nodes
************************

.. Warning::

    Native DICOM store functionality has not proved to be stable over long periods. Therefore we cannot recommend that
    you use this feature in a production environment. However, please do test it and help us to improve it if you are
    able to!

OpenREM DICOM Store SCPs (service class provider) enable modalities or PACS to send DICOM structured reports and images
directly to OpenREM where they are imported into the database.

The Store SCP service receives the data, checks whether it is one of the objects that OpenREM can extract data from,
and starts an import task if applicable.

The object is then left in the ``dicom_in`` folder in the ``media`` folder, or it is deleted, depending on the policy
set in :doc:`i_deletesettings`.

To configure a DICOM Store SCP, click ``Add new Store`` and fill in the details:

* Name of local store node: This is the *friendly name*, such as ``OpenREM store``
* Application Entity Title of the node: This is the DICOM name for the store, and must be letters or numbers only, no
  spaces, and a maximum of 16 characters
* Port for store node: Port 104 is the reserved DICOM port, but it is common to use *high* ports such as 8104, partly
  because ports up to 1024 usually need more privileges than for the high ports. However, if there is a firewall
  between the remote nodes (modalities, PACS) and the OpenREM server, then you need to make sure that the firewall is
  configured to allow the port you choose here.
* Autostart and keep-alive: Using celery beat the server can be started automatically and restarted automatically if
  this box is ticked..
