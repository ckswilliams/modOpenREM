Testing GraphViz
================

.. graphviz::

   digraph {
      a -> c;
      b -> c;
      c -> d;
      a [shape=box, label="X-ray imaging modality"];
      b [shape=box, label="PACS via OpenREM query-retrieve"];
      c [label="DICOM StoreSCP (Conquest)"];
   }