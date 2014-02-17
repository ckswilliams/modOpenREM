=======================
OpenREM version history
=======================

0.3.4-rc2
---------

* #28     XLSX export crashed if any of the filter fields were missing. Now fills on import with 'None'
* #27     Use requested procedure description if requested procedure code description is missing


0.3.4
-----

* --      General improvements and addition of logo to docs
* #23     Added Windows XP MySQL backup guide to docs
* #22     Added running Conquest as a Windows XP service to docs
* #15     Added version number and copyright information to xlsx exports
* #14     Added version number to the web interface
* #13     Improve the docs with respect to South database migrations


0.3.3-r2
--------

* #12     Added this version history
* #11     Documentation is no longer included in the tar.gz install file -- see http://openrem.trfd.org instead

0.3.3
-----

..      Warning::
        
        Installs of OpenREM earlier than 0.3.3 will break on upgrade if the scripts are called from other programs.
        For example openrem_rdsr is now called openrem_rdsr.py

* --      Added warning of upgrade breaking existing installs to docs
* #10     Added .py suffix to the scripts to allow them to be executed on Windows (thanks to DJ Platten)
* #8      Removed superfluous '/' in base html file, harmless on linux, prevented Windows loading stylesheets (thanks to DJ Platten)
* #7      Added windows and linux path examples for test SQLite database creation
* #6      Corrected renaming of example files installation instruction (thanks to DJ Platten) 
* #4      Added some text to the documentation relating to importing files to OpenREM
* #3      Corrected copyright notice in documentation


0.3.2
-----

* Initial version uploaded to bitbucket.org
