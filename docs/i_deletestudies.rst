****************
Deleting studies
****************

Individual studies
==================

If you log in as a user that is in the ``admingroup``, then an extra column is appended in
the filtered view tables to allow studies to be deleted:

.. image:: img/Delete.png
    :width: 730px
    :align: center
    :height: 196px
    :alt: Deleting studies

Clicking on delete takes you to a confirmation page before the delete takes place.

All studies from one source
===========================

.. figure:: img/ConfigMenu.png
   :figwidth: 30%
   :align: right
   :alt: Admin menu

   The ``Config`` menu (admin)


If you log in as a user that is in the ``admingroup``, on the ``Config`` menu select ``Display names & modality`` to
get to a list of all the X-ray systems with data in OpenREM. More information about :doc:`i_displaynames`.

Each row is a unique combination of all the column headers, so if a modality has a software update for example this will
usually mean a new row is started.

In the last column is a link to ``Review`` the studies from that source. This can be useful for troubleshooting a
particular source, or you can use it to delete all the studies from one source in one go.

.. figure:: img/ReviewUniqueEquipmentStudies.png
   :align: center
   :alt: Source study review
   :width: 1036px

   Source equipment review page with study delete options

The details for that source are displayed, along with a table showing which sort of data is contained in each study.
Above the 'Study deletion options' panel the following two numbers are indicated:

#. The number of studies associated with this equipment
#. The number of studies associated with this equipment after being filtered by the indicated modality type

If the second number is smaller than the first, this will indicate that some of the studies from the equipment have
been labelled with a different modality type. There will therefore be an entry in one of the other tables on the
equipment display name page.

Delete studies and table entry
------------------------------

Use this button if you want to delete all the studies and remove the entry that has been made in the Unique Equipment
Names table. Otherwise, the entry would remain but with zero studies associated with it. The deletion takes a second
confirmation step.

If there are studies associated with this equipment that are listed with a modality type different to the one shown,
those studies will not be deleted and the table entry will not be removed.

Delete studies
--------------

If you have associated this table entry with a ``Display name`` and you want any future studies to fall under the same
name, you can leave the entry in the Unique Equipment Names table. You might want to do this for example if you have
a Display name of 'CR' or 'Imported'. Again, there is a confirmation step.

Again, only the studies associated with this equipment that have the same modality type as shown will be deleted.

.. _failed_import_studies:

Failed import studies
=====================

At the bottom of the ``Display names & modality`` page is a table listing the number of studies that are in the
database, but do not have an entry in the ``unique_equipment_name`` table. This usually indicates a study that has
failed early in the import process.

Users in the ``admingroup`` are able to click on the links to review the studies on a per-modality basis. This will list
the information that is available, which might indicate which system they came from, what times, dates and accession
numbers.

The user is then able to delete all the failed import studies in the list.

Before release 0.8.2, these studies would appear in the homepage listing as
*Error has occurred - import probably unsuccessful*. This has now changed to a link to the review page for that modality
with the text *Failed import - review here* for users in the ``admingroup`` and
*Failed import - ask an administrator to review* for other users.
