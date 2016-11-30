Testing GraphViz
================

.. graphviz::

   digraph {
      subgraph cluster_rules {
         node [style=filled,color=white];
         style=filled;
         color=lightgrey;
         conquest_script -> populate_database -> delete_object;
         label = "Apply Conquest rules"
      }

      modality -> conquest;
      pacs -> conquest;
      conquest -> storage -> conquest_script;

      modality [shape=box, label="X-ray imaging modality"];
      pacs [shape=box, label="PACS via OpenREM query-retrieve"];
      conquest [label="DICOM StoreSCP (Conquest)"];
      storage [shape=box, label="DICOM objects stored on server temporarily"];
      conquest_script [label="Process Conquest script"];
      populate_database [label="Extract information to database"];
      delete_object [label="Delete DICOM object"];
   }