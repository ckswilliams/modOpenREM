##############################
Not-patient indicator settings
##############################

The standard configuration for OpenREM is to not store any patient identifiable information.  Therefore it can be
difficult to distinguish between real patients and test or quality assurance exposures.

*Changed in 0.8.0*

To aid identification of non-patient exposures, the patient name and the patient ID are checked against a set of
patterns, and if a match is found then the pattern is recorded in the database before the patient name and ID are
deleted or converted to a hash (see :doc:`patientid`)

