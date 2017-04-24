Exporting study information
***************************

Exporting to csv and xlsx sheets
================================

If you are logged in as a user in the ``exportgroup`` or the ``admingroup``,
the export links will be available near the top of the modality filter pages
in the OpenREM interface. The following exports are currently available (version 0.5.0)

* CT basic, single sheet csv
* CT advanced, XLSX muliple-sheets
* Fluoroscopy basic, single sheet csv
* Mammography, single sheet csv
* Mammography NHSBSP, single sheet csv designed to satisfy NHSPSB reporting
* Radiographic, single sheet csv
* Radiographic, XLSX multiple sheets

For CT and radiographic, the XLSX export has multiple sheets. The first sheet contains a
summary of all the study descriptions, requested procedures and series
protocol names contained in the export:

.. image:: img/CTExportSummaryPage.png
    :width: 730px
    :align: center
    :height: 339px
    :alt: CT export front sheet
    
This information is useful for seeing what data is in the spreadsheet, and
can also be used to prioritise which studies or protocols to analyse based on
frequency.

The second sheet of the exported file lists all the studies, with each study
taking one line and each series in the study displayed in the columns to the right.

.. image:: img/CTExportAllData.png
    :width: 730px
    :align: center
    :height: 339px
    :alt: CT export all data sheet

The remainder of the file has one sheet per series protocol name. Each series
is listed one per line. If a single study
has more than one series with the same protocol name, then the same study
will appear on more than one line.

Clicking the link for an export redirects you to the Exports page, which
you can also get to using the link at the top right of the navigation bar:

.. image:: img/Exports.png
    :align: center
    :width: 1277px
    :height: 471px
    :alt: Exports list

Whilst an export is being processed, it will be listed in the first table
at the top. The current status is displayed to indicate export progress.
If an export gets stuck for whatever reason, you may be able to abort the
process by clicking the 'Abort' button. However this does not always cause
an active export to terminate - you may find it completes anyway!

Completed exports are then listed in the second table, with a link to
download the csv or xlsx file.

When the export is no longer needed, it can be deleted from the server
by ticking the delete checkbox and clicking the delete button at the bottom:

.. image:: img/ExportsDelete.png
    :align: center
    :width: 450px
    :height: 268px
    :alt: Deleting exports

.. warning::

    Large exports have been killed by the operating system due to running 
    out of memory - a 6500 CT exam xlsx export was killed after 3400 
    studies for example. This issue is being tracked as `#116`_ and will
    hopefully be addressed in the next release. It is possible that if debug 
    mode is turned off then memory will be managed better, but I also need
    to modify the xlsx export to make use of the memory optimisation mode in 
    xlsxwriter.

Specific modality export information
====================================

NHSBSP Mammography exports
--------------------------
This export is specific to the UK NHS Breast Screening Programme and generates the source data in the format required
for the  dose audit database developed by the National Co-ordinating Centre for the Physics of Mammography.

It has been modified to clean up the data to remove exposures hat are unlikely to be wanted in the submitted data, such
as exposures with any of the following in the protocol name::

    scout, postclip, prefire, biopsy, postfire, stereo, specimin, artefact

The view codes have been modified to match the NCCPM convention, ie medio-lateral oblique is recorded as ``OB`` instead
of ``MLO``. The other codes are mapped to the `ACR MQCM 1999 Equivalent code.`_

Each patient is numbered from starting from 1. Each view for any one patient has a unique view code, so if a second
cranio-caudal exposure is made to the left breast the view codes will be LCC and LCC2.

The survey number is left as 1. This needs to be modified as appropriate. The easiest way to do this in Excel is to
change the first two or three rows, select those cells that have been changed, then double click on the botto-right
corner of the selection box to copy-down the value to all the remaining cells below.

The data can then be copied and pasted into the NCCPM database.

If there are a mixture of 2D and tomography exposures, providing you can separate them by virtue of the filter used,
then you should further prepare the data as follows:

1. Copy the sheet to a new sheet
1. In the first sheet, filter for the target and filter combination used for used for the tomographic exposures and
   delete those rows.
1. In the second sheet, filter for the target and filter combinations used for 2D exposures and delete those rows.
1. Change the survey number on the 2D sheet and the the survey number on the tomographic sheet as appropriate, with the
   tomographic survey number bing one more than the 2D survey number.

Where patients have had both 2D and tomographic exposures in the same study, NCCPM will be able to match them up as they
will have the same patient number in both surveys.









































..  _`#116`: https://bitbucket.org/openrem/openrem/issue/116/
..  _ACR MQCM 1999 Equivalent code.: http://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_CID_4014.html