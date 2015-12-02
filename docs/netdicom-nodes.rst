###########################
DICOM Network Configuration
###########################

*******
General
*******

sdfasdf

*****************
DICOM store nodes
*****************

OpenREM DICOM Store SCPs (service class provider) enable modalities or PACS to send DICOM structured reports and images
directly to OpenREM where they are imported into the database.

The Store SCP service recieves the data, checks whether it is one of the objects that OpenREM can extract data from,
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