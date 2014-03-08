=======================
OpenREM version history
=======================



0.3.9
-----
..  note:: #51 includes changes to the database schema -- make sure South is in use before upgrading. See http://docs.openrem.org/page/upgrade.html

* #59   CSS stylesheet referenced particular fonts that are not in the distribution -- references removed
* #58   Export to xlsx more robust - limitation of 31 characters for sheet names now enforced
* #57   Modified the docs slightly to include notice to convert to South before upgrading
* #56   Corrected the mammography target and filter options added for issue #44
* #53   Dates can now be selected from a date picker widget for filtering studies
* #52   Split the date field into two so either, both or neither can be specified
* #51   Remove import modifications from issue #28 and #43 now that exports are filtered in a better way after #48 and #49 changes.
* #50   No longer necessary to apply a filter before exporting -- docs changed to reflect this
* #49   CSV exports changed to use the same filtering routine introduced for #48 to better handle missing attributes
* #48   New feature -- can now filter by patient age. Improved export to xlsx to better handle missing attributes
* #47   Install was failing on pydicom -- fixed upstream

0.3.8
-----

* --    File layout modified to conform to norms
* #46   Updated documentation to reflect limited testing of mammo import on
  additional modalities
* #45   mam.py was missing the licence header - fixed
* #44   Added Tungsten, Silver and Aluminum to mammo target/filter strings to match -- thanks to DJ Platten for strings
* #43   Mammography and Philips CT import and export now more robust for images with 
  missing information such as accession number and collimated field size
* #42   Documentation updated to reflect #37
* #37	Studies now sort by time and date


0.3.7
-----

* #40   Restyled the filter section in the web interface and added a title to that section
* #38   Column titles tidied up in Excel exports
* #36	openrem_ptsizecsv output of log now depends on verbose flag
* #35   Numbers no longer stored as text in Excel exports

0.3.6
-----

* #34   Localised scripts that were on remote web servers in default Bootstrap code
* #33   Documentation now exists for adding data via csv file
* #24   Web interface has been upgraded to Bootstrap v3
* #5    Web interface and export function now have some documentation with screenshots


0.3.5-rc2
---------

* #32   Missing sys import bug prevented new patient size import from working

0.3.5
-----

* --    Prettified this document!
* #31   Promoted patient size import from csv function to the scripts folder so it will install and can be called from the path
* #30   Improved patient size import from csv to allow for arbitary column titles and study instance UID in addition to accession number.
* #29   Corrected the docs URL in the readme

0.3.4-rc2
---------

* #28   XLSX export crashed if any of the filter fields were missing. Now fills on import with 'None'
* #27   Use requested procedure description if requested procedure code description is missing


0.3.4
-----

* --    General improvements and addition of logo to docs
* #23   Added Windows XP MySQL backup guide to docs
* #22   Added running Conquest as a Windows XP service to docs
* #15   Added version number and copyright information to xlsx exports
* #14   Added version number to the web interface
* #13   Improve the docs with respect to South database migrations


0.3.3-r2
--------

* #12   Added this version history
* #11   Documentation is no longer included in the tar.gz install file -- see http://openrem.trfd.org instead

0.3.3
-----

..      Warning::
        
        Installs of OpenREM earlier than 0.3.3 will break on upgrade if the scripts are called from other programs.
        For example openrem_rdsr is now called openrem_rdsr.py

* --    Added warning of upgrade breaking existing installs to docs
* #10   Added .py suffix to the scripts to allow them to be executed on Windows (thanks to DJ Platten)
* #8    Removed superfluous '/' in base html file, harmless on linux, prevented Windows loading stylesheets (thanks to DJ Platten)
* #7    Added windows and linux path examples for test SQLite database creation
* #6    Corrected renaming of example files installation instruction (thanks to DJ Platten) 
* #4    Added some text to the documentation relating to importing files to OpenREM
* #3    Corrected copyright notice in documentation


0.3.2
-----

*       Initial version uploaded to bitbucket.org
