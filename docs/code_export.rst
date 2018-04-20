Export from database
====================
    
Multi-sheet Microsoft Excel XLSX exports
++++++++++++++++++++++++++++++++++++++++
This export has a summary sheet of all the requested and performed 
protocols and the series protocols. The next sheet has all studies on,
one study per line, with the series stretching off to the right. The
remaining sheets are specific to each series protocol, in alphabetical
order, with one series per line. If one study has three series with the
same protocol name, each one has a line of its own.

.. autotask:: remapp.exports.rf_export.rfxlsx
.. autotask:: remapp.exports.ct_export.ctxlsx(filterdict, pid=False, name=False, patid=False, user=False)
.. autotask:: remapp.exports.dx_export.dxxlsx
.. autotask:: remapp.exports.mg_export.exportMG2excel(filterdict, pid=False, name=False, patid=False, user=False, xlsx=True)


Single sheet CSV exports
++++++++++++++++++++++++
   
.. autotask:: remapp.exports.rf_export.exportFL2excel
.. autotask:: remapp.exports.ct_export.ct_csv(filterdict, pid=False, name=False, patid=False, user=False)
.. autotask:: remapp.exports.mg_export.exportMG2excel
.. autotask:: remapp.exports.dx_export.exportDX2excel

Specialised csv exports - NHSBSP formatted mammography export
-------------------------------------------------------------

.. autotask:: remapp.exports.mg_csv_nhsbsp.mg_csv_nhsbsp
