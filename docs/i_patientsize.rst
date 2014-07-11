Adding patient size information from csv using the web interface
****************************************************************
*New in 0.4.3*

Uploading patient size data
===========================

If you log in as a user that is in the ``admingroup``, then a menu is
available at the right hand end of the navigation bar:

.. image:: img/AdminImportMenu.png
    :width: 314px
    :align: right
    :height: 110px
    :alt: Admin import patient size data menu

The first option takes you to a page where you can upload a csv file
containing details of the patient height and weight, plus either the
accession number or the Study Instance UID.

.. image:: img/AdminUploadPtSzCSV.png
    :width: 730px
    :align: center
    :height: 497px
    :alt: Uploading CSV files containing patient size information

.. image:: img/AdminUploadButton.png
    :width: 252px
    :align: right
    :height: 114px
    :alt: Upload patient size csv file button

The csv file needs to have at least the required columns. Additional columns
will be ignored. If your source of patient size data does not have either the
height or the weight column, simply add a new empty column with just the title
in the first row.

When you have selected the csv file, press the button to upload it.

Importing the size data to the database
=======================================

On the next page select the column header that corresponds to each of the 
head, weight and ID fields. Also select whether the ID field is an Accession number
or a Study UID:

When the column headers are selected, click the 'Process the data' button.

.. image:: img/AdminSizeHeaders.png
    :width: 730px
    :align: center
    :height: 357px
    :alt: Selecting header information

The progress of the import is then reported on the patient size imports page:

.. image:: img/AdminSizeImporting.png
    :width: 730px
    :align: center
    :height: 86px
    :alt: Patient size importing

As soon as the import is complete, the source csv file is deleted from the
server.
