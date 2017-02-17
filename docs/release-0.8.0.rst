########################
Upgrade to OpenREM 0.8.0
########################

****************
Headline changes
****************

* Imports: No longer tries to import non-dose report Enhanced Structured Reports
* Charts: Added mammography scatter plot, thanks to `@rijkhorst`_
* Exports: DX and RF exports work with multiple filters, and will be displayed to max 4 sf

***************************************************
Upgrading an OpenREM server with no internet access
***************************************************


****************************
Upgrading from version 0.7.4
****************************

* Set the date format for xlsx exports (need to check csv situation). Copy the following code into your
  ``local_settings.py`` file if you want to change it from ``dd/mm/yyy``:

.. sourcecode:: python

    # Date format for exporting data to Excel xlsx files.
    # Default in OpenREM is dd/mm/yyyy. Override it by uncommenting and customising below; a full list of codes is available
    # at https://msdn.microsoft.com/en-us/library/ee634398.aspx.
    # XLSX_DATE = 'mm/dd/yyyy'

* Consider setting the timezone and language in ``local_settings.py``. See ``local_settings.py.example``.



..  _@rijkhorst: https://bitbucket.org/rijkhorst/