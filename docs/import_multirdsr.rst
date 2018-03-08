Importing updated Radiation Dose Structured Reports
***************************************************

Some modalities are configured to send an RDSR after every exposure, with each new RDSR containing a complete record of
the examination up to that point. For example this has what current versions of the Siemens CT scanner software does.

The other circumstance where this might happen is when an initial exam is aborted and then continued, with two RDSRs
being sent as a result.

Pre-0.8.0 OpenREM behaviour
===========================

Prior to release 0.8.0, OpenREM would check the StudyInstanceUID on import and check the value against the existing
studies in the database. If a match was found, then the new RDSR was rejected on the basis that it must be a duplicate.

Therefore, if you have a scanner that creates per-event RDSRs and sends them automatically to the OpenREM server, you
will find that every study in database for that scanner has only one event (e.g. the topogram).