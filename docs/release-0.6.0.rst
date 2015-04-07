####################
Release Notes v0.6.0
####################

****************
Headline changes
****************

* Charts

* Modalities with no data are hidden in the user interface

******
Charts
******

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