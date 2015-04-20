######################
Release Notes v0.6.0b1
######################

****************
Headline changes
****************

* Charts
* Preview of DICOM Store SCP functionality
* Exports available to import into `OpenSkin`_
* Modalities with no data are hidden in the user interface

*************************
Preparing for the upgrade
*************************

Convert to South
================

**Make sure you have converted your database to South before attempting an upgrade**

Quick reminder of how, if you haven't done it already

.. sourcecode:: bash

    # Linux: Debian/Ubuntu and derivatives
    python /usr/local/lib/python2.7/dist-packages/openrem/manage.py convert_to_south remapp
    # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
    python /usr/local/lib/python2.7/site-packages/openrem/manage.py convert_to_south remapp

    # Windows, assuming no virtualenv
    python C:\Python27\Lib\site-packages\openrem\manage.py convert_to_south remapp

Additional installs
===================

OpenREM requires two additional programs to be installed to enable the new features: *Numpy* for charts, and
*pynetdicom* for the DICOM Store Service Class Provider. Note that the version of pynetdicom must be later than the
current pypi release!

Install numpy
-------------
**Insert numpy install instructions here**

Install pynetdicom
------------------

.. sourcecode:: bash

    pip install https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2



Upgrading from version 0.5.1
============================

* Back up your database

    * For PostgreSQL you can refer to :doc:`backupRestorePostgreSQL`
    * For a non-production SQLite3 database, simply make a copy of the database file

* The 0.6.0b1 upgrade must be made from a 0.5.1 (or later) database, and a schema migration is required:

    .. sourcecode:: bash

        pip install openrem==0.6.0b1

            # Linux: Debian/Ubuntu and derivatives
            python /usr/local/lib/python2.7/dist-packages/openrem/manage.py schemamigration --auto remapp
            python /usr/local/lib/python2.7/dist-packages/openrem/manage.py migrate remapp
            # Linux: other distros. In a virtualenv replace all up to lib/ as appropriate
            python /usr/local/lib/python2.7/site-packages/openrem/manage.py schemamigration --auto remapp
            python /usr/local/lib/python2.7/site-packages/openrem/manage.py migrate remapp
            # Windows:
            python C:\Python27\Lib\site-packages\openrem\manage.py schemamigration --auto remapp
            python C:\Python27\Lib\site-packages\openrem\manage.py migrate remapp

***********************
Summary of new features
***********************

Charts
======

Release 0.6.0 has a range of charting options available for CT and radiographic data. These charts allow visualisation
of trends and frequencies to inform surveys and monitor performance. For more information, please see :doc:`charts`.


DICOM Store Service Class Provider
==================================

OpenREM can now act as the DICOM Store service, allowing direct sending of DICOM objects from modalities to OpenREM
without needing to use Conquest or any other DICOM Store SCP. This feature is a preview as it hasn't been extensively
tested, but it is expected to work. For more information, please see :doc:`netdicom`.


Exports for OpenSkin
====================

Fluoroscopy studies can now be exported in a format suitable for importing into Jonathan Cole's OpenSkin software. The
export link is on the fluoroscopy study detail page. The software for creating the exposure incidence map can be
downloaded from https://bitbucket.org/jacole/openskin/downloads (choose the zip file), and information about the project
can be found on the `OpenSkin wiki`_. The software allows the user to choose between a 2D phantom that would represent
the dose to a film laying on the couch surface, or a simple 3D phantom made up of a cuboid and two semi-cylinders
(these can be seen on the `Phantom design`_ section of the wiki). For both options the output is an image of the dose
distribution in 2D, along with calculated peak skin dose information.

Automatic hiding of unused modality types
=========================================

A fresh install of OpenREM will no longer show any of the four modality types in the tables or in the navigation bar
at the top. As DICOM objects are ingested, the appropriate tables and navigation links are created.

Therefore a site that has no mammography for example will no longer have that table or navigation link in their
interface.

******
Charts
******

**To be moved to the charts doc**

Charts of the currently filtered data can now be shown for CT and radiographic data.
The user can configure which plots are shown using the ``Chart options`` on the CT
and radiographic pages.

The first option, ``Plot charts?``, determines whether any plots are shown. This also
controls whether the data for the plots is calculated by OpenREM. Some plot data is
slow to calculate when there is a large amount of data: some users may prefer to leave
``Plot charts?`` off for performance reasons. ``Plot charts?`` can be switched on and
activated with a click of the ``submit`` button after the data has been filtered.

A user's chart options can also be changed via OpenREM's user administration page.

The available charts for CT data are as follows:

    * Bar chart of mean DLP for each acquisition protocol. Clicking on a bar takes the
      user to a histogram of DLP for that protocol. Clicking on the tool-tip link of
      a histogram bar takes the user to the list of studies that contain the
      acquisitions in the histogram bar.

    * Pie chart of the frequency of each acquisition protocol. Clicking on a segment
      of the pie chart takes the user to the list of studies that contain the
      acquisitions in that segment.

    * Bar chart of mean DLP for each study name. Clicking on a bar takes the user to
      a histogram of DLP for that study name. Clicking on the tool-tip link of a
      histogram bar takes the user to the list of studies that correspond to the
      data in the histogram bar.

    * Pie chart of the frequency of each study name. Clicking on a segment of the
      pie chart takes the user to the list of studies that correspond to the data
      in that segment.

    * Pie chart showing the number of studies carried out per weekday. Clicking on
      a segment of the pie chart takes the user to a pie chart showing the studies
      for that weekday broken down per hour.

    * Line chart showing how the mean DLP of each study name varies over time. The
      time period per data point can be chosen by the user in the ``Chart options``.
      Note that selecting a short time period may result in long calculation times.
      The user can zoom in to the plot by clicking and dragging the mouse to select
      a date range. The user can also click on items in the legend to show or hide
      individual lines.

The available charts for radiographic data are as follows:

    * Bar chart of mean DAP for each acquisition protocol. Clicking on a bar takes the
      user to a histogram of DAP for that protocol. Clicking on the tool-tip link of
      a histogram bar takes the user to the list of studies that contain the
      acquisitions in the histogram bar.

    * Pie chart of the frequency of each acquisition protocol. Clicking on a segment
      of the pie chart takes the user to the list of studies that contain the
      acquisitions in that segment.

    * Bar chart of mean kVp for each acquisition protocol. Clicking on a bar takes the
      user to a histogram of kVp for that protocol. Clicking on the tool-tip link of
      a histogram bar takes the user to the list of studies that contain the
      acquisitions in the histogram bar.

    * Bar chart of mean mAs for each acquisition protocol. Clicking on a bar takes the
      user to a histogram of mAs for that protocol. Clicking on the tool-tip link of
      a histogram bar takes the user to the list of studies that contain the
      acquisitions in the histogram bar.

    * Pie chart showing the number of studies carried out per weekday. Clicking on
      a segment of the pie chart takes the user to a pie chart showing the studies
      for that weekday broken down per hour.

    * Line chart showing how the mean DAP of each acquisition protocol varies over
      time. The time period per data point can be chosen by the user in the
      ``Chart options``. Note that selecting a short time period may result in long
      calculation times. The user can zoom in to the plot by clicking and dragging
      the mouse to select a date range. The user can also click on items in the
      legend to show or hide individual lines.

.. _`OpenSkin`: https://bitbucket.org/jacole/openskin
.. _`OpenSkin wiki`: https://bitbucket.org/jacole/openskin/wiki/Home
.. _`Phantom design`: https://bitbucket.org/jacole/openskin/wiki/Phantom%20design