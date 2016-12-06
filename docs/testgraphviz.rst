OpenREM diagrams
================

Diagram showing the OpenREM system components
---------------------------------------------

.. graphviz::

   digraph {
      node [fixedsize=true width=1.5];

      // Define the things on the server
      subgraph cluster_server {
         label="Server";
         tooltip="The server";
         labeljust=l;
         fontname="Helvetica";
         style=filled;
         color=lightgrey;
         node [style=filled color=white];

         // Define the nodes
         webserver [label="Apache\nweb server" fontname="Helvetica" tooltip="Serve web pages to the user" shape="box" style="rounded filled" color=white];
         python_django [label="OpenREM\nDjango app" fontname="Helvetica" tooltip="Python web framework" shape="box"];
         database [label="PostgreSQL\ndatabase" fontname="Helvetica" tooltip="Relational database management system" shape="cylinder"];
         rabbitmq [label="RabbitMQ\nmessage broker" fontname="Helvetica" tooltip="Message broker" shape="box"];
         celery [label="Celery\ntask queue" fontname="Helvetica" tooltip="Asynchronous task queue" shape="polygon sides=6"];
         skin_dose_map_data [label="Skin dose map\ndata calculation,\nstorage, retrieval" fontname="Helvetica" tooltip="Calculate, store and retrieve skin dose map data" shape="parallelogram" width="2.5"];
         server_media_folder [label="Server file storage\n(Media Home folder)" fontname="Helvetica" tooltip="File storage on the server" shape="folder" width="2.5"];
         data_export [label="Data export to\nlocal file system" fontname="Helvetica" tooltip="Files are made available to the user via a web page URL" shape="box"];

         // Define the links between the nodes
         webserver -> python_django [dir=both];
         python_django -> database [dir=both label="via psycopg2\nPython adapter" fontsize=8 fontname="Courier"];
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
      web_browser [label="Client\nweb browser" fontname="Helvetica" tooltip="The user's web browser" shape="box" style=rounded];
      web_browser -> webserver [dir=both label="via user-requests\land Ajax\l" fontsize=8 fontname="Courier" tooltip="Ajax used to retrieve chart data"];
   }

Diagram showing import of data into OpenREM
-------------------------------------------

.. graphviz::

   digraph {

      subgraph cluster_rules {
         label = "Apply Conquest rules\nto each DICOM object";
         node [style=filled color=white];
         style=filled;
         color=lightgrey;
         labelloc=t;
         labeljust=l;
         fontname="Helvetica"

         conquest_script -> populate_database [label="Yes" fontcolor=darkgreen fontsize=8 fontname="Courier"];
         populate_database -> delete_object;
         conquest_script -> delete_object [label="No" fontcolor=red fontsize=8 fontname="Courier"];

         {rank=same; populate_database delete_object};
      }

      modality -> conquest [label="via modality\lconfiguration\l" fontsize=8 fontname="Courier"];
      pacs -> conquest [label="via OpenREM\lquery-retrieve\l" fontsize=8 fontname="Courier"];
      conquest -> conquest_script;

      modality [label="X-ray imaging\nmodality" fontname="Helvetica" tooltip="Data send from an x-ray imaging modality" shape="box" style="rounded"];
      pacs [label="PACS" fontname="Helvetica" tooltip="A Picture Archiving and Communication System" shape="parallelogram"];
      conquest [label="DICOM StoreSCP\n(Conquest)" fontname="Helvetica" tooltip="Conquest, acting as a DICOM storage SCP" shape="box"];
      conquest_script [shape=diamond label="Does the object contain useful data?" fontname="Helvetica" tooltip="Process the rules in dicom.ini"];
      populate_database [label="Extract information from\nthe DICOM object to the\nOpenREM database" fontname="Helvetica", tooltip="Extract data using OpenREM's python scripts" shape="box"];
      delete_object [label="Delete the DICOM object\nfrom the Conquest store" fontname="Helvetica" tooltip="Delete the DICOM object from the local store SCP" shape="box"];
   }