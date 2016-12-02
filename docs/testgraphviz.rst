Testing GraphViz
================

Diagram showing the OpenREM components
--------------------------------------

.. graphviz::

   digraph {

      // Define the things on the server
      subgraph cluster_server {
         label="Server";
         tooltip="The server";
         labeljust=l;
         fontname="Helvetica";
         style=filled;
         color=lightgrey;
         node [style=filled, color=white];

         // Define the nodes
         webserver [label="Apache\nweb server", fontname="Helvetica", tooltip="Serve web pages to the user"];
         python_django [label="OpenREM\nDjango app", fontname="Helvetica", tooltip="Python web framework"];
         database [label="PostgreSQL\ndatabase", fontname="Helvetica", tooltip="Relational database management system"];
         rabbitmq [label="RabbitMQ\nmessage broker", fontname="Helvetica", tooltip="Message broker"];
         celery [label="Celery\ntask queue", fontname="Helvetica", tooltip="Asynchronous task queue"];
         skin_dose_map_data [label="Skin dose map data\ncalculation, storage, retrieval", fontname="Helvetica", tooltip="Calculate, store and retrieve skin dose map data"];
         server_media_folder [label="Server file storage\n(Media Home folder)", fontname="Helvetica", tooltip="File storage on the server"];
         data_export [label="Data export to\nlocal file system", fontname="Helvetica", tooltip="Files are made available to the user via a web page URL"];

         // Define the links between the nodes
         webserver -> python_django [dir=both];
         python_django -> database [dir=both, label="via psycopg2\nPython adapter", fontsize=8, fontname="Courier"];
         python_django -> rabbitmq;
         rabbitmq -> celery;
         celery -> skin_dose_map_data;
         celery -> data_export;
         skin_dose_map_data -> server_media_folder [dir=both];
         skin_dose_map_data -> python_django [style=dotted dir=both];
         data_export -> server_media_folder;
         data_export -> python_django [style=dotted dir=both];

         // Force python_django and the database to be on the same level
         {rank=same; python_django database}
         {rank=same; skin_dose_map_data data_export}
      }

      // Define the web browser
      web_browser [label="Client\nweb browser", fontname="Helvetica", tooltip="The user's web browser"];
      web_browser -> webserver [dir=both, label="via user-requests\land Ajax\l", fontsize=8, fontname="Courier", tooltip="Ajax used to retrieve chart data"];
   }

Diagram showing import of data into OpenREM
-------------------------------------------

.. graphviz::

   digraph {
      splines=ortho;
      fontname="Courier";

      subgraph cluster_rules {
         node [style=filled,color=white];
         style=filled;
         color=lightgrey;
         fontsize=10;
         labelloc=t;
         labeljust=l;

         conquest_script -> populate_database [label="Yes", fontcolor=darkgreen, fontsize=10];
         populate_database -> delete_object;
         conquest_script -> delete_object [label="No", fontcolor=red, fontsize=10];
         label = "Apply Conquest rules\nto each DICOM object";

         {rank=same; populate_database, delete_object};
      }

      modality -> conquest [label="Via modality\nconfiguration", fontsize=10];
      pacs -> conquest [label="Via OpenREM\nquery-retrieve", fontsize=10];
      conquest -> conquest_script;

      modality [shape=box, label="X-ray imaging\nmodality"];
      pacs [shape=box, label="PACS"];
      conquest [label="DICOM StoreSCP\n(Conquest)"];
      conquest_script [shape=diamond, label="Does the object contain useful data?"];
      populate_database [label="Extract information from\nthe DICOM object to the\nOpenREM database"];
      delete_object [label="Delete the DICOM object\nfrom the Conquest store"];
   }