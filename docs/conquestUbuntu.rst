$ sudo apt-get install conquest-sqlite 
[sudo] password for mcdonaghe: 
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  linux-headers-4.2.0-16 linux-headers-4.2.0-16-generic linux-image-4.2.0-16-generic
  linux-image-extra-4.2.0-16-generic
Use 'apt-get autoremove' to remove them.
The following extra packages will be installed:
  conquest-common liblua5.1-0
Suggested packages:
  conquest-dicom-server
The following NEW packages will be installed
  conquest-common conquest-sqlite liblua5.1-0
0 to upgrade, 3 to newly install, 0 to remove and 0 not to upgrade.
Need to get 2,615 kB of archives.
After this operation, 4,670 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
Get:1 http://gb.archive.ubuntu.com/ubuntu/ wily/universe conquest-common amd64 1.4.17d-1 [2,012 kB]
Get:2 http://gb.archive.ubuntu.com/ubuntu/ wily/main liblua5.1-0 amd64 5.1.5-8 [102 kB]
Get:3 http://gb.archive.ubuntu.com/ubuntu/ wily/universe conquest-sqlite amd64 1.4.17d-1 [501 kB]
Fetched 2,615 kB in 4s (534 kB/s)        
Selecting previously unselected package conquest-common.
(Reading database ... 254467 files and directories currently installed.)
Preparing to unpack .../conquest-common_1.4.17d-1_amd64.deb ...
Unpacking conquest-common (1.4.17d-1) ...
Selecting previously unselected package liblua5.1-0:amd64.
Preparing to unpack .../liblua5.1-0_5.1.5-8_amd64.deb ...
Unpacking liblua5.1-0:amd64 (5.1.5-8) ...
Selecting previously unselected package conquest-sqlite.
Preparing to unpack .../conquest-sqlite_1.4.17d-1_amd64.deb ...
Unpacking conquest-sqlite (1.4.17d-1) ...
Processing triggers for doc-base (0.10.6) ...
Processing 3 added doc-base files...
Processing triggers for man-db (2.7.4-1) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...
Setting up conquest-common (1.4.17d-1) ...
Setting up liblua5.1-0:amd64 (5.1.5-8) ...
Setting up conquest-sqlite (1.4.17d-1) ...
Adding `_conquest' group to system ...
Adding `_conquest' user to system ...
adduser: Warning: The home directory `/etc/conquest-dicom-server' does not belong to the user you are currently creating.
We'll regenerate the database...
Starting /usr/bin/dgate...
Regen Database
Mon Feb 15 09:12:54 2016 Started zip and cleanup thread
Mon Feb 15 09:12:54 2016 Step 1: Re-intialize SQL Tables
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMWorkList
Dropping Existing tables (if-any)
Worklist is empty
Dropping worklist
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMWorkList
***Failed SQLITEExec : DROP TABLE DICOMWorkList
Dropping other tables
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMPatients
***Failed SQLITEExec : DROP TABLE DICOMPatients
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMStudies
***Failed SQLITEExec : DROP TABLE DICOMStudies
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMSeries
***Failed SQLITEExec : DROP TABLE DICOMSeries
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: DICOMImages
***Failed SQLITEExec : DROP TABLE DICOMImages
Mon Feb 15 09:12:54 2016 ***SQLITEExec error: no such table: UIDMODS
***Failed SQLITEExec : DROP TABLE UIDMODS
WorkList Database
Patient Database
Study Database
Series Database
Image Database
Mon Feb 15 09:12:54 2016 Step 2: Load / Add DICOM Object files
Regen Device 'MAG0'
Mon Feb 15 09:12:54 2016 Regeneration Complete


If it's the first time you install conquest-dicom-server, disregard any error messages about absent database tables.
Processing triggers for libc-bin (2.21-0ubuntu4) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for systemd (225-1ubuntu9) ...

