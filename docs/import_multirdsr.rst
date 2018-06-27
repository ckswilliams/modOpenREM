Cumulative and continued study RDSRs
************************************

Background
==========

Cumulative RDSRs
----------------
Some modalities are configured to send an RDSR after every exposure, with each new RDSR containing a complete record of
the examination up to that point. For example, this is what the current version of the Siemens CT scanner software does.

Continued study RDSRs
---------------------
On most systems the RDSR is sent when the study is completed. If the study is then restarted, the system must create a
new RDSR. On a Siemens CT system, this new RDSR will have the same Study Instance UID and the same accession number,
but the content will only refer to the continued study, not the original study.

Pre-0.8.0 OpenREM behaviour
---------------------------

Prior to release 0.8.0, OpenREM would check the Study Instance UID on import and check the value against the existing
studies in the database. If a match was found, then the new RDSR was rejected on the basis that it must be a duplicate.

This would therefore ignore both cumulative and continued study RDSRs which means your database might be filled with
single event studies, and you won't have details of any continued studies.

Current OpenREM behaviour
=========================

New imports
-----------

On import of the first RDSR in a study, the SOP Instance UID of the RDSR is recorded with the study. This is an ID
that is unique to that RDSR object - any further RDSRs might have the same Study Instance UID, but will always have a
different SOP Instance UID.

When the second RDSR is imported, the duplicate StudyInstanceUID will trigger OpenREM to check the SOP Instance UID of
the new RDSR against the one(s) stored with that study. If there is a match, the new RDSR is ignored as it has already
been processed. If it does not match, then the Irradiation Event UID of each exposure in the new RDSR is compared to the
Irradiation Event UIDs already in the database for that study, to establish if the new RDSR carries new information that
should be imported.

In the case of a cumulative RDSR that is sent after each event, the original study is deleted from
the database and is replaced by the newer one if it has additional events.

In the case of a continued study RDSR which has
a completely different set of events, the new RDSR is imported alongside the existing one.

Existing studies imported before 0.8.0
--------------------------------------

RDSRs imported before upgrading to 0.8.0 will not have the SOP Instance UID recorded in the database and so the new
RDSR will be compared at event level with the existing study before making an import decision, as with new studies.

Fixing existing studies
=======================

Importing from file
-------------------

If you are have a store of the RDSRs that were previously rejected, import them all again and this time they should be
processed properly.

For example on my system, using linux, each scanner started sending per-exposure RDSRs from the date they were upgraded.
I found the RDSRs from that date to the date I upgraded OpenREM and imported them:

..  sourcecode:: bash

    touch --date "2018-01-06" tmpdate20180106
    touch --date "2018-02-07" tmpdate20180207
    find RDSRs/ -newer tmpdate20180106 ! -newer tmpdate20180207 -name *.dcm -exec openrem_rdsr.py {} \;

Importing via query-retrieve
----------------------------

The query-retrieve duplicates processing has been updated to compare SOP Instance UIDs returned by the remote node (the
PACS) with the SOP Instance UIDs stored with each study in OpenREM. Therefore, after an initial import of each RDSR
in your search, any subsequent query should drop any RDSRs that have previously been processed and not move them a
second time.
