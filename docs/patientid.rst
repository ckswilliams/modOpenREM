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
OpenREM, so this is now configurable from version 0.7 onwards.

Configure what is stored
========================

.. figure:: img/ConfigMenu.png
    :align: center
    :alt: Configuration menu

On the Config menu, select ``Patient ID settings``. The initial settings are as follows:

.. figure:: img/ModifyPtIDStorage.png
    :align: center
    :alt: Modify patient identifiable data settings

The default for patient name, ID and date of birth is to not store them. There isn't an option currently to not store
the accession number, though OpenREM continues to work if it is missing.

To start to store patient identifiable data from now on, select the relevant box and press ``Submit``. If you change the
setting again later, then data already stored will remain in the database.

Store hashed data only
======================

If you wish to have the patient name and/or ID available for finding studies relating to a specific patient, but do
not need to identify who that patient is, then it is possible to create a 'hash' of the ID or name before it is stored.

If *exactly* the same name or ID (including spelling, spacing, case etc) occur more than once, then the same hash
will be generated.