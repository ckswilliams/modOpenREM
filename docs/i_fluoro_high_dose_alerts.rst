Fluroscopy high dose alerts
***************************
*New in 0.8.2*

.. contents::

Alert level configuration
=========================

.. figure:: img/ConfigMenu.png
   :figwidth: 30%
   :align: right
   :alt: Config options

   Figure 1: The ``Config`` menu (user and admin)

The system highlights fluoroscopy studies that have exceeded defined levels of
DAP and total dose at reference point. These alert levels can be configured by
an OpenREM administrator via the `Fluoro alert levels` option in the ``Config``
menu (figure 1).

The default alert levels are 20000 cGy.cm\ :sup:`2` DAP and 2 Gy total dose at
reference point (figure 2).

.. figure:: img/fluoroHighDoseAlertSettings.png
   :figwidth: 100%
   :align: center
   :alt: Fluoroscopy high dose alert settings

   Figure 2: Fluoroscopy high dose alert settings

Figures 3 and 4 illustrate how studies that exceed an alert level are
highlighted in the filtered and detailed fluoroscopy views.

.. figure:: img/fluoroHighDoseAlertFilteredView.png
   :figwidth: 100%
   :align: center
   :alt: Filtered view showing the highlighting of some high dose studies

   Figure 3: Filtered view showing the highlighting of some high dose studies


.. figure:: img/fluoroHighDoseAlertDetailedView.png
   :figwidth: 100%
   :align: center
   :alt: Detailed view showing high-dose highlighting

   Figure 4: Detailed view showing high-dose highlighting


Alerts for accumulated dose over a period of time
=================================================

As well as alerting to individual studies that exceed alert levels the system
can be configured to calculate accumulated dose over a defined number of weeks
for studies with matching patient ID.

For this to work the storage of patient ID or encrypted patient ID must be
enabled (see the ``Patient Identifiable data`` :ref:`i_not_patient_indicator`
documentation).

The number of previous weeks over which to sum DAP and dose at RP for studies
with matching patient ID is defined in the options (figure 2).

The display of summed DAP and dose at RP values on the fluoroscopy filtered
view can be enabled or disabled (figure 2).

The calculation of summed DAP and dose at RP for incoming studies can also be
enabled or disabled (figure 2).

An example of a study where there is another study on a matching patient ID is
shown below in figure 5. In this example neither of the two studies were
individually above an alert level, but when summed together the total dose at
RP does exceed the corresponding alert.

.. figure:: img/fluoroHighDoseAlertDetailedViewTwoStudies.png
   :figwidth: 100%
   :align: center
   :alt: Detailed view showing associated studies over a time period

   Figure 5: Detailed view showing associated studies over a time period


Recalculation of summed data
============================

After upgrading from a version of OpenREM prior to 0.8.2, or after changing
the alert levels or number of weeks to look for matching data, the summed
dose values need to be recalculated. The user is prompted to do this via
the display of an orange button, as shown in figure 6 below.

.. figure:: img/fluoroHighDoseAlertSettingsRecalculate.png
   :figwidth: 100%
   :align: center
   :alt: Prompt to recalculate the summed dose values

   Figure 6: Prompt to recalculate the summed dose values

Recalculation of the summed data is likely to take several minutes. During this
time the form buttons are faded out and disabled, and a spinning icon is shown
in the middle of the page (figure 7).

.. figure:: img/fluoroHighDoseAlertSettingsRecalculating.png
   :figwidth: 100%
   :align: center
   :alt: Recalculating the summed dose values

   Figure 7: Prompt to recalculate the summed dose values

Once all summed data has been recalculated the orange recalculate button is
hidden, the other form buttons are reactivated and the user is shown a
success message at the top of the screen (figure 8, below).

.. figure:: img/fluoroHighDoseAlertSettingsRecalculated.png
   :figwidth: 100%
   :align: center
   :alt: Recalculating the summed dose values

   Figure 8: Message on successful recalculation


E-mail notifications of high dose alerts
========================================

E-mail notifications of high dose studies can be enabled or disabled on the
high dose alerts configuration page as shown in figure 2.

Any OpenREM user can be configured to receive these messages; these users can
be chosen by navigating to the `Fluoro alert notifcation` option on the
`Config` menu (figure 2). This takes you to a page where notification
recipients can be configured (figure 9).

It should be noted that any OpenREM user selected to recieve high dose alerts
must have an e-mail address entered in their user configuration. Successful
e-mail sending is also dependent on the correct configuration of the e-mail
section of the OpenREM settings.

Include example e-mail?

.. figure:: img/fluoroHighDoseAlertNotifications.png
   :figwidth: 100%
   :align: center
   :alt: E-mail user-notification of high-dose alerts

   Figure 9: E-mail user-notification of high-dose alerts
