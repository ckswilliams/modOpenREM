Importing updated Radiation Dose Structured Reports
***************************************************

Some modalities are configured to send an RDSR after every exposure, with each new RDSR containing a complete record of
the examination up to that point. For example this is what the current version of the Siemens CT scanner software does.

The other circumstance where this might happen is when an initial exam is aborted and then continued, with two RDSRs
being sent as a result.

Pre-0.8.0 OpenREM behaviour
===========================

Prior to release 0.8.0, OpenREM would check the StudyInstanceUID on import and check the value against the existing
studies in the database. If a match was found, then the new RDSR was rejected on the basis that it must be a duplicate.

Therefore, if you have a scanner that creates per-event RDSRs and sends them automatically to the OpenREM server, you
will find that every study in database for that scanner has only one event (e.g. the topogram).

Release 0.8.0 OpenREM behaviour
===============================

New imports
-----------

On import of the first RDSR in a study, the series time and content time are both recorded in the database. Both of
these would normally change with each subsequent RDSR for the same study.

When the second RDSR is imported, the duplicate StudyInstanceUID will trigger OpenREM to check the series time and
content time. If the new study has a later time than the existing study, OpenREM will attempt to check if the first
RDSR has finished importing, and then delete the existing study from the database and replace it with the new one.

If the existing study has not finished importing, OpenREM will pause for 30 seconds before proceeding.

Imports from before upgrading to 0.8.0
--------------------------------------

