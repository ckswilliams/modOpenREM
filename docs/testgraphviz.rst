Testing GraphViz
================

.. graphviz::

   digraph {
      subgraph cluster_rules {
         node [style=filled,color=white];
         style=filled;
         color=lightgrey;
         conquest_script -> populate_database -> delete_object;
         label = "Apply Conquest rules\nto each DICOM object";
         fontname="Courier";
         fontsize=10;
         labelloc=t;
         labeljust=l;
      }

      modality -> conquest;
      pacs -> conquest;
      conquest -> conquest_script;

      modality [shape=box, label="X-ray imaging\nmodality", fontname="Courier"];
      pacs [shape=box, label="PACS via OpenREM\nquery-retrieve", fontname="Courier"];
      conquest [label="DICOM StoreSCP\n(Conquest)", fontname="Courier"];
      conquest_script [label="Apply dicom.ini rules\nto the DICOM object", fontname="Courier"];
      populate_database [label="Extract information from\nthe DICOM object to the\nOpenREM database", fontname="Courier"];
      delete_object [label="Delete the DICOM object\nfrom the Conquest store", fontname="Courier"];
   }