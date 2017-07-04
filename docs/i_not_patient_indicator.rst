##############################
Not-patient indicator settings
##############################

The standard configuration for OpenREM is to not store any patient identifiable information.  Therefore it can be
difficult to distinguish between real patients and test or quality assurance exposures.

*Changed in 0.8.0*

To aid identification of non-patient exposures, the patient name and the patient ID are checked against a set of
patterns, and if a match is found then the pattern is recorded in the database before the patient name and ID are
deleted or converted to a hash (see :doc:`patientid` for details).

****************************************************
Setting the patterns to identify non-patient studies
****************************************************

The patient name and the ID are matched against the patterns you configure. The patterns make use of wildcards as per
the following table:

+---------+----------------------------------+
| Pattern |	Meaning                          |
+=========+==================================+
| *	      | matches everything               |
+---------+----------------------------------+
| ?	      | matches any single character     |
+---------+----------------------------------+
| [seq]	  | matches any character in seq     |
+---------+----------------------------------+
| [!seq]  | matches any character not in seq |
+---------+----------------------------------+

To match all studies where the patient name begins with  ``physics``, the pattern should be set to ``physics*``. This
would match ``Physics^RoutIQ`` but not match ``Testing^Physics``.

