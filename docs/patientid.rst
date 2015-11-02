#########################
Patient identifiable data
#########################

Prior to version 0.7, no data that is generally considered to be patient identifiable was stored in the OpenREM database.

The following patient descriptors have always been recorded if they were available:

* Patient age at the time of the study, but not date of birth (though this could be calculated from age)
* Patient sex
* Patient height
* Patient weight

In addition, a key identifier for the exam that is normally not considered patient identifiable was stored:

* Study accession number

It has become apparent that there are reasons where people need to store patient identifiable data to make the most of
OpenREM, such as
