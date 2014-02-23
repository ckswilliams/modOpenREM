Using the OpenREM interface and export function
***********************************************


Navigating the OpenREM web interface
====================================

Depending on your web server setup, your web interface to OpenREM will
usually be at http://yourserver/openrem or if you are using the test web
server then it might be at http://localhost:8000/openrem.

The home page for OpenREM should look something like this when it is 
populated with studies:

.. image:: img/HomeFull.png
    :width: 730px
    :align: center
    :height: 590px
    :alt: OpenREM homepage screenshot

By selecting the links in the navigation bar at the top, you can view all
of the CT, fluoroscopy or mammography studies. Alternatively, if you click
on the station name link (in blue) you can filter to just that source modality.

Filtering for specific studies
==============================

This image shows the CT studies view, filtered by entering terms in the 
boxes on the right hand side to show just the studies for a particular
date range and for just one source modality (filtering on station name):

.. image:: img/CTFilter.png
    :width: 730px
    :align: center
    :height: 410px
    :alt: Filtering CT studies

The search fields can all be used on their own or together, and they are
all case insensitive 'contains' searches. The exception is the date field,
where both from and to have to be filled in (if either are), and the format
must be ``yyyy-mm-dd``. There currently isn't any more complex filtering
available, but it does exist as `issue 17 <https://bitbucket.org/edmcdonagh/openrem/issue/17/>`_
for a future release.

The last box below the filtering search boxes is the ordering preferance.
The order by date function does not currently take into account the time
of the study - `issue 37 <https://bitbucket.org/edmcdonagh/openrem/issue/37>`_
exists to address this.

Exporting to csv and xlsx sheets
================================

placeholder
