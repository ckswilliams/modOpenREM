Configuring Conquest DICOM server to accept x-ray radiation dose structured reports
***********************************************************************************

The Conquest DICOM server only accepts incoming DICOM objects if they have a service-object pair (SOP) unique identifier that appears in the ``dgatesop.lst`` file, located in the root of the Conquest installation folder.

By default this file does not contain the SOP information for x-ray radiation dose structured reports (RDSRs). It is easy to add this: open the ``dgatesop.lst`` file in a text editor and add the following line::

    XRayRadiationDoseSR	1.2.840.10008.5.1.4.1.1.88.67	sop

After a restart, Conquest will now accept incoming RDSR objects.