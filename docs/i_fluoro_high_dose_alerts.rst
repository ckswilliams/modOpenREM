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
an OpenREM administrator via the fluoro alert levels option in the ``Config``
menu. The default alert levels are 20000 cGy.cm:sup:`2` DAP and 2 Gy total dose
at reference point.

.. figure:: img/fluoroHighDoseAlertSettings.png
   :figwidth: 100%
   :align: center
   :alt: Fluoroscopy high dose alert settings

   Figure 2: Fluoroscopy high dose alert settings


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

The system can also be configured to calculate accumulated dose over an
OpenREM-admin defined number of weeks for studies with matching patient ID. For
this to work the storage of patient ID, or encrypted patient ID, must be
enabled.

The number of previous weeks over which to sum DAP and dose at RP for studies
with matching patient ID is defined in the options (figure 2).

The display of these summed DAP and dose at RP values on the fluoroscopy
filtered view can be enabled or disabled (figure 2).

The calculation of summed DAP and dose at RP for incoming studies can also be
enabled or disabled (figure 2).

.. figure:: img/fluoroHighDoseAlertDetailedViewTwoStudies.png
   :figwidth: 100%
   :align: center
   :alt: Detailed view showing associated studies over a time period

   Figure 5: Detailed view showing associated studies over a time period


Recalculation of summed data
============================

Something here about having to recalculate summed data after change in
parameters - see figures.

Warning that it will take minutes.

.. figure:: img/fluoroHighDoseAlertSettingsRecalculate.png
   :figwidth: 100%
   :align: center
   :alt: Prompt to recalculate the summed dose values

   Figure 6: Prompt to recalculate the summed dose values

.. figure:: img/fluoroHighDoseAlertSettingsRecalculating.png
   :figwidth: 100%
   :align: center
   :alt: Recalculating the summed dose values

   Figure 7: Prompt to recalculate the summed dose values

.. figure:: img/fluoroHighDoseAlertSettingsRecalculated.png
   :figwidth: 100%
   :align: center
   :alt: Recalculating the summed dose values

   Figure 8: Message on successful recalculation


E-mail notifications of high dose alerts
========================================

Can be enabled or disabled on the configuration page (figure 2).

E-mail alerts only sent if calculation of summed doses is enabled for incoming studies.

Relies on e-mail being configured in the OpenREM settings.

Any OpenREM user can be configured to receive these messages (see a figure) -
must have an e-mail address entered in their user configuration.

Include example e-mail?

.. figure:: img/fluoroHighDoseAlertNotifications.png
   :figwidth: 100%
   :align: center
   :alt: E-mail user-notification of high-dose alerts

   Figure 9: E-mail user-notification of high-dose alerts
