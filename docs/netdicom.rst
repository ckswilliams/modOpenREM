##################
DICOM Store and QR
##################

To make the most of OpenREM, you need a DICOM store node and maybe use DICOM query-retrieve too. The documents below
walk you though how to set this up.

We are recommending that production installations make use of a third party provided DICOM store node as the in-built
one has not yet proved to be reliable enough though some users have reported a good experience with it. Future versions
of OpenREM will make use of a more modern DICOM library at which point we should be able to recommend using the in-built
DICOM store.

..  toctree::
    :maxdepth: 2

    netdicom-nodes
    netdicom-qr

The following instructions might also be useful with a Conquest setup, but they need review and updating:

..  toctree::
    :maxdepth: 2

    conquestAsWindowsService
    conquestImportConfig
    conquestExampleDicomIni

