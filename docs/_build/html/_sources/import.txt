Importing data to OpenREM
*************************


Importing dose related data from DICOM files
============================================

If you are using linux or have put ```"C:\Python27\Lib\site-packages\openrem\scripts"`` and
``"C:\Python27\Lib\site-packages\openrem"`` onto your path, you should be able to import from the command line:

Radiation Dose Structured Reports
---------------------------------

* ``openrem_rdsr.py filename.dcm``

For mammography DICOM images (see restrictions on testing)
----------------------------------------------------------

* ``openrem_mg.py filename.dcm``

For CT dose summary files from Philips CT scanners
--------------------------------------------------

* ``openrem_ctphilips.py filename.dcm``


Importing dose related data from csv files
==========================================

Patient height and weight information
-------------------------------------

If height and weight data is not available in the DICOM data, but is available
from another source, then it can be imported into the database using the 
``openrem_ptsizecsv.py`` function. Normally the key to match the size information
with the studies in the database will be the accession number; however in some
situations this isn't available and the Study Instance UID can be used instead.

usage: ``openrem_ptsizecsv.py [-h] [-u] csvfile id height weight``

``-h, --help``
  Print the help text.

``-u, --si-uid``
  Use Study Instance UID instead of Accession Number.

``csvfile``
  csv file containing the height and/or weight information and study identifier. 
  Other columns will be ignored. Use quotes if the filepath has spaces.

``id``
  Column title for the accession number or study instance UID. Use quotes
  if the title has spaces.

``height``
  Column title for the patient height (DICOM size) - if this information 
  is missing simply add a blank column with a suitable title. Use quotes
  if the title has spaces.

``weight``
  Column title for the patient weight - if this information is missing 
  simply add a blank column with a suitable title. Use quotes if the title
  has spaces.

..  Note::
    
    ``openrem_ptsizecsv.py`` currently prints out the success or otherwise
    of each line to the standard output. `Issue 36 <https://bitbucket.org/edmcdonagh/openrem/issue/36/>`_
    has been raised to suppress this output unless the verbose flag is set.
