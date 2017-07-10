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

.. figure:: img/ConfigMenu.png
    :figwidth: 30 %
    :align: right
    :alt: Config menu

    The ``Config`` menu

Use the ``Config`` menu and select ``Not-patient indicators``:

The patient name and the ID are matched against the patterns you configure. The patterns make use of wildcards as per
the following table, and are case insensitive:

========= ===================================
Pattern   Meaning
========= ===================================
 \*	       matches everything
 ?	       matches any single character
 [seq]	   matches any character in seq
 [!seq]    matches any character not in seq
========= ===================================

To match all studies where the patient name begins with  ``physics``, the pattern should be set to ``physics*``. This
would match ``Physics^RoutIQ`` but not match ``Testing^Physics``. The patient name in DICOM is normally formatted
``Family name^Given name^Middle name^Prefix^Suffix``. Therefore to match any studies where the first name is ``Test``,
you would set the pattern to be ``*^test*``.

If your test patient name always starts with ``PHY`` and then a number, you might use this pattern: ``phy[0-9]*``.
Here we have used a range for the sequence to match any number, but it will only match one character per sequence, so a
``*`` is required to match all the characters after the first number. This pattern will match ``Phy12345`` and
``PHY6test`` but not ``Phyliss``.

The pattern list for patient name and the list for patient ID are separate, so both need to be populated to meet your
requirements.

Creating new patterns
=====================

Click on ``Add ID patterns`` or ``Add name patterns`` in the panel title bar and follow the instructions.

Modifying patterns
==================

Click the ``Modify`` link in the row of the pattern you wish to modify.

Deleting patterns
=================

Click the ``Delete`` link in the row of the pattern you wish to delete. You will be asked to confirm the deletion.

**************************************************
Replicating behaviour of release 0.7.4 and earlier
**************************************************


OpenREM releases before 0.8 had the not-patient identification patterns hard-coded. From release 0.8.0 the patterns are
(admin) user configurable, but will start with no patterns in place. To add the patterns that would maintain the
behaviour of previous releases, use the link at the bottom of the config page, or the link in the add/modify pages.

