=======================
OpenREM version history
=======================

0.4.0
-----

..  note::

    * `#64`_ includes **changes to the database schema and needs a user response** - see `version 0.4.0 release notes <http://docs.openrem.org/page/release-0.4.0.html>`_
    * `#65`_ includes changes to the settings file which **require settings information to be copied** and files moved/renamed - see `version 0.4.0 release notes <http://docs.openrem.org/page/release-0.4.0.html>`_

* `#68`_   Now checks sequence code meaning and value exists before assigning them. Thanks to JA Cole
* `#67`_   Added 'Contributing authors' section of documentation
* `#66`_   Added 'Release notes' section of documentation, incuding this file
* `#65`_   Added new ``local_settings.py`` file for database settings and other local settings.
* `#64`_   Fixed imports failing due to non-conforming strings that were too long.
* `#63`_   The mammography import code stored the date of birth unnecessarily. Also now gets decimal_age from age field if necessary
* `#60`_   Removed extraneous colon from interface data field
* `#18`_   Studies can now be deleted from the web interface with the correct login
* `#16`_   Added user authentication with different levels of access
* `#9`_    Enable import of ``*.dcm``


0.3.9
-----
..  note:: `#51`_ includes changes to the database schema -- make sure South is in use before upgrading. See http://docs.openrem.org/page/upgrade.html

* `#59`_   CSS stylesheet referenced particular fonts that are not in the distribution -- references removed
* `#58`_   Export to xlsx more robust - limitation of 31 characters for sheet names now enforced
* `#57`_   Modified the docs slightly to include notice to convert to South before upgrading
* `#56`_   Corrected the mammography target and filter options added for issue `#44`_
* `#53`_   Dates can now be selected from a date picker widget for filtering studies
* `#52`_   Split the date field into two so either, both or neither can be specified
* `#51`_   Remove import modifications from issue `#28`_ and `#43`_ now that exports are filtered in a better way after `#48`_ and `#49`_ changes.
* `#50`_   No longer necessary to apply a filter before exporting -- docs changed to reflect this
* `#49`_   CSV exports changed to use the same filtering routine introduced for `#48`_ to better handle missing attributes
* `#48`_   New feature -- can now filter by patient age. Improved export to xlsx to better handle missing attributes
* `#47`_   Install was failing on pydicom -- fixed upstream

0.3.8
-----

* --    File layout modified to conform to norms
* `#46`_   Updated documentation to reflect limited testing of mammo import on additional modalities
* `#45`_   mam.py was missing the licence header - fixed
* `#44`_   Added Tungsten, Silver and Aluminum to mammo target/filter strings to match -- thanks to DJ Platten for strings
* `#43`_   Mammography and Philips CT import and export now more robust for images with missing information such as accession number and collimated field size
* `#42`_   Documentation updated to reflect `#37`_
* `#37`_   Studies now sort by time and date


0.3.7
-----

* `#40`_   Restyled the filter section in the web interface and added a title to that section
* `#38`_   Column titles tidied up in Excel exports
* `#36`_	openrem_ptsizecsv output of log now depends on verbose flag
* `#35`_   Numbers no longer stored as text in Excel exports

0.3.6
-----

* `#34`_   Localised scripts that were on remote web servers in default Bootstrap code
* `#33`_   Documentation now exists for adding data via csv file
* `#24`_   Web interface has been upgraded to Bootstrap v3
* `#5`_    Web interface and export function now have some documentation with screenshots


0.3.5-rc2
---------

* `#32`_   Missing sys import bug prevented new patient size import from working

0.3.5
-----

* --    Prettified this document!
* `#31`_   Promoted patient size import from csv function to the scripts folder so it will install and can be called from the path
* `#30`_   Improved patient size import from csv to allow for arbitary column titles and study instance UID in addition to accession number.
* `#29`_   Corrected the docs URL in the readme

0.3.4-rc2
---------

* `#28`_   XLSX export crashed if any of the filter fields were missing. Now fills on import with 'None'
* `#27`_   Use requested procedure description if requested procedure code description is missing


0.3.4
-----

* --    General improvements and addition of logo to docs
* `#23`_   Added Windows XP MySQL backup guide to docs
* `#22`_   Added running Conquest as a Windows XP service to docs
* `#15`_   Added version number and copyright information to xlsx exports
* `#14`_   Added version number to the web interface
* `#13`_   Improve the docs with respect to South database migrations


0.3.3-r2
--------

* `#12`_   Added this version history
* `#11`_   Documentation is no longer included in the tar.gz install file -- see http://openrem.trfd.org instead

0.3.3
-----

..      Note::
        
        Installs of OpenREM earlier than 0.3.3 will break on upgrade if the scripts are called from other programs.
        For example openrem_rdsr is now called openrem_rdsr.py

* --    Added warning of upgrade breaking existing installs to docs
* `#10`_   Added .py suffix to the scripts to allow them to be executed on Windows (thanks to DJ Platten)
* `#8`_    Removed superfluous '/' in base html file, harmless on linux, prevented Windows loading stylesheets (thanks to DJ Platten)
* `#7`_    Added windows and linux path examples for test SQLite database creation
* `#6`_    Corrected renaming of example files installation instruction (thanks to DJ Platten) 
* `#4`_    Added some text to the documentation relating to importing files to OpenREM
* `#3`_    Corrected copyright notice in documentation


0.3.2
-----

*       Initial version uploaded to bitbucket.org

..  _`#79`: https://bitbucket.org/edmcdonagh/openrem/issue/79/
..  _`#78`: https://bitbucket.org/edmcdonagh/openrem/issue/78/
..  _`#77`: https://bitbucket.org/edmcdonagh/openrem/issue/77/
..  _`#76`: https://bitbucket.org/edmcdonagh/openrem/issue/76/
..  _`#75`: https://bitbucket.org/edmcdonagh/openrem/issue/75/
..  _`#74`: https://bitbucket.org/edmcdonagh/openrem/issue/74/
..  _`#73`: https://bitbucket.org/edmcdonagh/openrem/issue/73/
..  _`#72`: https://bitbucket.org/edmcdonagh/openrem/issue/72/
..  _`#71`: https://bitbucket.org/edmcdonagh/openrem/issue/71/
..  _`#70`: https://bitbucket.org/edmcdonagh/openrem/issue/70/
..  _`#69`: https://bitbucket.org/edmcdonagh/openrem/issue/69/
..  _`#68`: https://bitbucket.org/edmcdonagh/openrem/issue/68/
..  _`#67`: https://bitbucket.org/edmcdonagh/openrem/issue/67/
..  _`#66`: https://bitbucket.org/edmcdonagh/openrem/issue/66/
..  _`#65`: https://bitbucket.org/edmcdonagh/openrem/issue/65/
..  _`#64`: https://bitbucket.org/edmcdonagh/openrem/issue/64/
..  _`#63`: https://bitbucket.org/edmcdonagh/openrem/issue/63/
..  _`#62`: https://bitbucket.org/edmcdonagh/openrem/issue/62/
..  _`#61`: https://bitbucket.org/edmcdonagh/openrem/issue/61/
..  _`#60`: https://bitbucket.org/edmcdonagh/openrem/issue/60/
..  _`#59`: https://bitbucket.org/edmcdonagh/openrem/issue/59/
..  _`#58`: https://bitbucket.org/edmcdonagh/openrem/issue/58/
..  _`#57`: https://bitbucket.org/edmcdonagh/openrem/issue/57/
..  _`#56`: https://bitbucket.org/edmcdonagh/openrem/issue/56/
..  _`#55`: https://bitbucket.org/edmcdonagh/openrem/issue/55/
..  _`#54`: https://bitbucket.org/edmcdonagh/openrem/issue/54/
..  _`#53`: https://bitbucket.org/edmcdonagh/openrem/issue/53/
..  _`#52`: https://bitbucket.org/edmcdonagh/openrem/issue/52/
..  _`#51`: https://bitbucket.org/edmcdonagh/openrem/issue/51/
..  _`#50`: https://bitbucket.org/edmcdonagh/openrem/issue/50/
..  _`#49`: https://bitbucket.org/edmcdonagh/openrem/issue/49/
..  _`#48`: https://bitbucket.org/edmcdonagh/openrem/issue/48/
..  _`#47`: https://bitbucket.org/edmcdonagh/openrem/issue/47/
..  _`#46`: https://bitbucket.org/edmcdonagh/openrem/issue/46/
..  _`#45`: https://bitbucket.org/edmcdonagh/openrem/issue/45/
..  _`#44`: https://bitbucket.org/edmcdonagh/openrem/issue/44/
..  _`#43`: https://bitbucket.org/edmcdonagh/openrem/issue/43/
..  _`#42`: https://bitbucket.org/edmcdonagh/openrem/issue/42/
..  _`#41`: https://bitbucket.org/edmcdonagh/openrem/issue/41/
..  _`#40`: https://bitbucket.org/edmcdonagh/openrem/issue/40/
..  _`#39`: https://bitbucket.org/edmcdonagh/openrem/issue/39/
..  _`#38`: https://bitbucket.org/edmcdonagh/openrem/issue/38/
..  _`#37`: https://bitbucket.org/edmcdonagh/openrem/issue/37/
..  _`#36`: https://bitbucket.org/edmcdonagh/openrem/issue/36/
..  _`#35`: https://bitbucket.org/edmcdonagh/openrem/issue/35/
..  _`#34`: https://bitbucket.org/edmcdonagh/openrem/issue/34/
..  _`#33`: https://bitbucket.org/edmcdonagh/openrem/issue/33/
..  _`#32`: https://bitbucket.org/edmcdonagh/openrem/issue/32/
..  _`#31`: https://bitbucket.org/edmcdonagh/openrem/issue/31/
..  _`#30`: https://bitbucket.org/edmcdonagh/openrem/issue/30/
..  _`#29`: https://bitbucket.org/edmcdonagh/openrem/issue/29/
..  _`#28`: https://bitbucket.org/edmcdonagh/openrem/issue/28/
..  _`#27`: https://bitbucket.org/edmcdonagh/openrem/issue/27/
..  _`#26`: https://bitbucket.org/edmcdonagh/openrem/issue/26/
..  _`#25`: https://bitbucket.org/edmcdonagh/openrem/issue/25/
..  _`#24`: https://bitbucket.org/edmcdonagh/openrem/issue/24/
..  _`#23`: https://bitbucket.org/edmcdonagh/openrem/issue/23/
..  _`#22`: https://bitbucket.org/edmcdonagh/openrem/issue/22/
..  _`#21`: https://bitbucket.org/edmcdonagh/openrem/issue/21/
..  _`#20`: https://bitbucket.org/edmcdonagh/openrem/issue/20/
..  _`#19`: https://bitbucket.org/edmcdonagh/openrem/issue/19/
..  _`#18`: https://bitbucket.org/edmcdonagh/openrem/issue/18/
..  _`#17`: https://bitbucket.org/edmcdonagh/openrem/issue/17/
..  _`#16`: https://bitbucket.org/edmcdonagh/openrem/issue/16/
..  _`#15`: https://bitbucket.org/edmcdonagh/openrem/issue/15/
..  _`#14`: https://bitbucket.org/edmcdonagh/openrem/issue/14/
..  _`#13`: https://bitbucket.org/edmcdonagh/openrem/issue/13/
..  _`#12`: https://bitbucket.org/edmcdonagh/openrem/issue/12/
..  _`#11`: https://bitbucket.org/edmcdonagh/openrem/issue/11/
..  _`#10`: https://bitbucket.org/edmcdonagh/openrem/issue/10/
..  _`#9`: https://bitbucket.org/edmcdonagh/openrem/issue/9/
..  _`#8`: https://bitbucket.org/edmcdonagh/openrem/issue/8/
..  _`#7`: https://bitbucket.org/edmcdonagh/openrem/issue/7/
..  _`#6`: https://bitbucket.org/edmcdonagh/openrem/issue/6/
..  _`#5`: https://bitbucket.org/edmcdonagh/openrem/issue/5/
..  _`#4`: https://bitbucket.org/edmcdonagh/openrem/issue/4/
..  _`#3`: https://bitbucket.org/edmcdonagh/openrem/issue/3/
..  _`#2`: https://bitbucket.org/edmcdonagh/openrem/issue/2/
..  _`#1`: https://bitbucket.org/edmcdonagh/openrem/issue/1/
