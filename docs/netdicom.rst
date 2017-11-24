##################
DICOM Store and QR
##################

To make the most of OpenREM, you need a DICOM store node and maybe use DICOM query-retrieve too. The documents below
walk you though how to set this up.

We are recommending that production installs make use of a third party provided DICOM store node as the in-built one has
not yet proved reliable enough at this time - any help with testing and improvement would be most welcome! This is why
we have provided documentation to work with conquest too.

..  toctree::
    :maxdepth: 2

    netdicom-nodes
    conquestUbuntu
    netdicom-qr

The following instructions might also be useful with a Conquest setup, but they need review and updating:

..  toctree::
    :maxdepth: 2

    conquestAsWindowsService
    conquestImportConfig
    conquestExampleDicomIni

