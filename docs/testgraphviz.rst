Testing GraphViz
================

.. graphviz::

   digraph {
      subgraph cluster_rules {
         node [style=filled,color=white];
         style=filled;
         color=lightgrey;
         conquest_script -> populate_database -> delete_object;
         label = "Apply Conquest rules";
         fontsize=10;
         labelloc=t;
         labeljust=l;
      }

      modality -> conquest;
      pacs -> conquest;
      conquest -> storage -> conquest_script;

      modality [shape=box, label="X-ray imaging modality"];
      pacs [shape=box, label="PACS via OpenREM\nquery-retrieve"];
      conquest [label="DICOM StoreSCP (Conquest)"];
      storage [shape=box, label="DICOM objects stored\non server temporarily"];
      conquest_script [label="Apply dicom.ini rules\nto the DICOM object"];
      populate_database [label="Extract information from\nthe DICOM object to the\nOpenREM database"];
      delete_object [label="Delete the DICOM object"];
   }