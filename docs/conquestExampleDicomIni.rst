Example Windows Conquest dicom.ini file
***************************************

Below is an example ``dicom.ini`` file, including comments describing the function of some sections. The file calls
various lua scripts - see the Conquest import configuration document for an example - :doc:`conquestImportConfig`.

The example ``dicom.ini`` file::

    # This file contains configuration information for the DICOM server
    # Do not edit unless you know what you are doing

    [sscscp]
    MicroPACS                = sscscp

    # Network configuration: server name (AE title) and TCP/IP port number. You may wish to add this OpenREM DICOM
    # node to some of your imaging modalities, or to your PACS, so that you can send data to OpenREM from these systems.
    # You'll need to know the AE title, port number and IP address of this server when doing this. Port 104 is commonly
    # used for DICOM traffic. You may need to configure your server firewall to allow network traffic on this port.
    MyACRNema                = OPENREM
    TCPPort                  = 104

    # Host, database, username and password for database. "localhost" means the server that Conquest is running on.
    # The SQLServer is blank to prevent the incoming DICOM objects from being added to the Conquest database - this
    # helps to avoid storing patient-identifiable data that you don't need to keep.
    SQLHost                  = localhost
    SQLServer                =
    Username                 =
    Password                 =
    SqLite                   = 1
    DoubleBackSlashToDB      = 0
    UseEscapeStringConstants = 0

    # Configure server
    ImportExportDragAndDrop  = 1
    ZipTime                  = 05:
    UIDPrefix                = 1.2.826.0.1.3680043.2.135.736310.50024482
    EnableComputedFields     = 1

    # This option determins the folder structure used by Conquest when saving incoming DICOM objects on the server.
    # Option 4 saves as ID\seriesuid_series#_image#_timecounter.dcm. At my Trust the ID is the patient NHS number.
    FileNameSyntax           = 4

    # Configuration of compression for incoming images and archival ("ul" saves images using little endian explicit
    # encoding).
    DroppedFileCompression   = ul
    IncomingCompression      = ul
    ArchiveCompression       = ul

    # For debug information
    PACSName                 = OPENREM
    OperatorConsole          = 127.0.0.1
    DebugLevel               = 0

    # Configuration of disk(s) to store incoming DICOM objects.
    MAGDeviceFullThreshHold  = 30
    MAGDevices               = 1
    MAGDevice0               = E:\conquest\dicom\


    # Importing incoming data in to OpenREM
    # The lua scripts that are called by some of these importers must be located in the same folder as this dicom.ini
    # file.

    # DICOM Radiation Dose Structured Report (RDSR) objects
    ImportConverter0 = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.67"; {save to E:\conquest\dicom\sr\%o.dcm; openrem_import_rdsr.lua(E:\conquest\dicom\sr\%o.dcm::%V0018,1000); destroy;}

    # Mammography objects (modality MG)
    ImportConverter1 = ifequal "%m", "MG"; { save to E:\conquest\dicom\mammo\%o.dcm; openrem_import_mg.lua("E:\conquest\dicom\mammo\%o.dcm"); destroy; }

    # Digital radiography (modality DX)
    ImportConverter2 = ifequal "%m", "DX"; { save to E:\conquest\dicom\dx\%o.dcm; openrem_import_cr_or_dx.lua(E:\conquest\dicom\dx\%o.dcm::%V0008,0070::%V0008,1090::%V0008,1010::%V0018,1020::%V0008,0020::%V0010,0010::%V0010,0020); destroy; }

    # Computed radiography (modality CR). Note: some digital radiography systems send their images as "CR" rather than "DX"
    ImportConverter3 = ifequal "%m", "CR"; { save to E:\conquest\dicom\cr\%o.dcm; openrem_import_cr_or_dx.lua(E:\conquest\dicom\cr\%o.dcm::%V0008,0070::%V0008,1090::%V0008,1010::%V0018,1020::%V0008,0020::%V0010,0010::%V0010,0020); destroy; }

    # Import converter for CT images. Conquest is configured to save images using the NHS number as the folder name, so
    # I think it makes sense to process the images by patient, rather than by study ("process patient after"... rather
    # than "process study after"...). If "process study" was used then the openrem_import_ct.lua script may be run
    # multiple times on the same folder if the folder contains more than one study for that patient.
    ImportConverter4 = ifequal "%V0008,1090","Brilliance 64"; { ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.7"; { save to E:\conquest\dicom\sr\%o.dcm; openrem_import_ctphilips.lua("E:\conquest\dicom\sr\%o.dcm"); }; destroy; }
    ImportConverter5 = ifequal "%V0008,1090","Brilliance 16P"; { ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.7"; { save to E:\conquest\dicom\sr\%o.dcm; openrem_import_ctphilips.lua("E:\conquest\dicom\sr\%o.dcm"); }; destroy; }
    ImportConverter6 = ifnotequal "%V0008,1090", "Brilliance 64"; { ifequal "%m", "CT"; { process patient after 0 by openrem_import_ct.lua %p::%V0008,0070::%V0008,1090::%V0018,1020::%V0008,1010::%V0010,0010::%V0010,0020::%V0008,0020::%V0018,1000; }; }

    # Import converter for Presentation State objects - delete them
    ImportConverter7 = ifequal "%m", "PR"; { destroy; }

    # Import converter for Key Object Selection objects - delete them
    ImportConverter8 = ifequal "%m", "KO"; { destroy; }

    # Import converter for OT modality objects - delete them
    ImportConverter9 = ifequal "%m", "OT"; { destroy; }

    # Import converter for PT modality objects (PET) - delete them
    ImportConverter10 = ifequal "%m", "PT"; { destroy; }

    # Import converter for NM modality objects - delete them
    ImportConverter11 = ifequal "%m", "NM"; { destroy; }

    # Import converter for "Comprehensive SR Storage" type files - delete them
    ImportConverter12 = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.33"; {destroy;}

    # Import converter for "Basic Text SR Storage" type files - delete them
    ImportConverter13 = ifequal "%V0008,0016","=BasicTextSRStorage"; {destroy;}

    # Import converter for US modality objects - delete them
    ImportConverter14 = ifequal "%m", "US"; { destroy; }

    # Import converter for XA modality objects - delete them
    ImportConverter15 = ifequal "%m", "XA"; { destroy; }

    # Import converter for PX modality objects (panoramic x-ray) - delete them
    ImportConverter16 = ifequal "%m", "PX"; { destroy; }

    # Import converter for PX modality objects (panoramic x-ray) - delete them
    ImportConverter17 = ifequal "%m", "PX"; { destroy; }

    # Import converter for XRayAngiographicImageStorage images (graphical dose reports sent by the cath lab) - delete them
    ImportConverter18 = ifequal "%V0008,0016","=XRayAngiographicImageStorage"; { destroy; }

    # Import converter for XRayAngiographicImageStorage images (graphical dose reports sent by the cath lab) - delete them
    ImportConverter19 = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.12.1"; { save to E:\conquest\dicom\cath_lab_protocols\%o.dcm; openrem_zip_angiostorage.lua(E:\conquest\dicom\cath_lab_protocols::E:\conquest\dicom\cath_lab_protocols\%o.dcm::%V0008,0020::%V0008,0030::%V0008,0050); destroy; }

    # Enhanced SR Storage objects
    ImportConverter20 = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.22"; {save to E:\conquest\dicom\sr\%o.dcm; openrem_import_rdsr.lua("E:\conquest\dicom\sr\%o.dcm"); destroy;}

    # Import converter for PX modality objects (panoramic x-ray) - delete them as the systems we have contain no useful
    # dose data information.
    ImportConverter21 = ifequal "%m", "MR"; { destroy; }
