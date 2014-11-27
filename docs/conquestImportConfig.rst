Configuring Conquest DICOM server to automatically forward data to OpenREM
**************************************************************************

The Conquest DICOM server can be configured to automatically run tasks when it receives specific types of DICOM object. For example, a script can be run when a DX image is received that will extract dose information into OpenREM; Conquest will then delete the original image.

These actions are set up in the ``dicom.ini`` file, located in the root of the Conquest installation folder.

For example::
    ImportModality1   = MG
    
    ImportConverter1  = save to C:\\conquest\\dosedata\\mammo\\%o.dcm; system C:\\conquest\\openrem-mam-launch.bat C:\\conquest\\dosedata\\mammo\\%o.dcm; destroy

``ImportModality1 = MG`` tells Conquest that modality 1 is MG. The commands listed in the ``ImportConverter1`` line are then run on all incoming MG images.

The ``ImportConverter`` instructions are separated by semicolons; the above example has three commands:

+ ``save to C:\conquest\dosedata\mammo\%o.dcm`` saves the incoming MG image to the specified folder with a file name set to the SOP instance UID contained in the image
+ ``system C:\conquest\openrem-mam-launch.bat C:\conquest\dosedata\mammo\%o.dcm`` runs a DOS batch file, using the newly saved file as the argument. On my system this batch file runs the OpenREM ``openrem_mg.py`` import script
+ ``destroy`` tells Conquest to delete the image that it has just received.

My system has three further import sections for DX, CR, and structured dose report DICOM objects::

    # Import of DX images
    ImportModality2   = DX
    ImportConverter2  = save to C:\conquest\dosedata\dx\%o.dcm; system C:\conquest\openrem-dx-launch.bat C:\conquest\dosedata\dx\%o.dcm; destroy

    # Import of CR images
    ImportModality3   = CR
    ImportConverter3  = save to C:\conquest\dosedata\dx\%o.dcm; system C:\conquest\openrem-dx-launch.bat C:\conquest\dosedata\dx\%o.dcm; destroy

    # Import of structured dose reports (this checks the DICOM tag 0008,0016 to see if it matches the value for a dose report)
    ImportConverter4  = ifequal "%V0008,0016","1.2.840.10008.5.1.4.1.1.88.67"; {save to C:\conquest\dosedata\sr\%o.dcm; system C:\conquest\openrem-sr-launch.bat "C:\conquest\dosedata\sr\%o.dcm"; destroy}