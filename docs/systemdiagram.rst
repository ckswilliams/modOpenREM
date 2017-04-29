Diagram showing the OpenREM system components
=============================================

.. graphviz::

   digraph {
      node [fixedsize=true width=2.0 height=0.75 fontsize=10 margin="0.0,0.0"];

      // Define the things on the server
      subgraph cluster_server {

         label="OpenREM server";
         tooltip="The server";
         fontname="Helvetica-bold";
         fontsize=16;
         style=filled;
         color=lightgrey;
         node [style=filled color=white];

         // Define the nodes for the data storage, display and retrieval
         webserver [label="Apache\nweb server&sup1;" fontname="Helvetica" tooltip="Serve web pages to the user" shape="box"];
         python_django [label="OpenREM\nDjango app" fontname="Helvetica" tooltip="Python web framework" shape="box"];
         database [label="PostgreSQL\ndatabase&sup3;" fontname="Helvetica" tooltip="Relational database management system" shape="parallelogram"];
         rabbitmq [label="RabbitMQ\nmessage broker" fontname="Helvetica" tooltip="Message broker" shape="box"];
         celery [label="Celery\ntask queue" fontname="Helvetica" tooltip="Asynchronous task queue" shape="hexagon"];
         skin_dose_map_data [label="Skin dose map\ndata calculation,\nstorage, retrieval" fontname="Helvetica" tooltip="Calculate, store and retrieve skin dose map data" shape="parallelogram"];
         server_media_folder [label="Server file storage\n(Media Home folder)" fontname="Helvetica" tooltip="File storage on the server" shape="parallelogram"];
         data_export [label="Data export to\nlocal file system" fontname="Helvetica" tooltip="Files are made available to the user via a web page URL" shape="box"];

         // Define the links between the data storage, display and retrieval
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

         // Define the nodes for the DICOM store, database population and skin dose map calculation
         conquest [label="DICOM StoreSCP\n(Conquest&sup2;)" fontname="Helvetica" tooltip="Conquest, acting as a DICOM storage SCP" shape="box"];
         conquest_script [shape=diamond label="Does the\nobject contain\nuseful data?" fontname="Helvetica" tooltip="Process the rules in dicom.ini"];
         populate_database [label="Extract information from\nthe DICOM object to the\nOpenREM database" fontname="Helvetica", tooltip="Extract data using OpenREM's python scripts" shape="box"];
         delete_object [label="Delete the DICOM object\nfrom the Conquest store" fontname="Helvetica" tooltip="Delete the DICOM object from the local store SCP" shape="box"];
         calc_skin_dose_map [shape=diamond label="Calculate\nskin dose\nmap?" fontname="Helvetica" tooltip="Calculate the skin dose map?"];
         blank_node_1 [shape=none style=invisible];

         // Define the links between the DICOM store, database population and skin dose map calculation
         conquest_script -> populate_database [label="Yes" fontcolor=darkgreen fontsize=8 fontname="Courier"];
         populate_database -> delete_object;
         conquest_script -> delete_object [label="No" fontcolor=red fontsize=8 fontname="Courier"];
         conquest -> conquest_script;
         populate_database -> calc_skin_dose_map;

         // Define the links between the two groups
         python_django -> populate_database [dir=back]
         calc_skin_dose_map -> celery [style=dotted label="Yes" fontcolor=darkgreen fontsize=8 fontname="Courier"]

         // Force certain nodes to be on the same level so that the diagram looks good (hopefully)
         {rank=same; webserver conquest};
         {rank=same; celery calc_skin_dose_map };
         {rank=same; python_django->blank_node_1->delete_object->populate_database [style=invis]; rankdir=LR;}
      }

      // Define the web browser, modality and pacs nodes
      web_browser [label="Client\nweb browser" fontname="Helvetica" tooltip="The user's web browser" shape="box" style=rounded];
      modality [label="X-ray imaging\nmodality" fontname="Helvetica" tooltip="Data send from an x-ray imaging modality" shape="parallelogram"];
      pacs [label="PACS" fontname="Helvetica" tooltip="A Picture Archiving and Communication System" shape="parallelogram"];
      blank_node_2 [label="" shape=none];

      // Define the links that the browser, modality and pacs have
      web_browser -> webserver [dir=both label="via user-requests\land Ajax\l" fontsize=8 fontname="Courier" tooltip="Ajax used to retrieve chart data"];
      modality -> conquest [label="via modality\lconfiguration\l" fontsize=8 fontname="Courier"];
      pacs -> conquest [label="via OpenREM\lquery-retrieve\l" fontsize=8 fontname="Courier"];

      // Force the web browser, blank node, modality and pacs to be on the same level in a specific order
      {rank=same; web_browser->blank_node_2->modality->pacs [style=invis]; rankdir=LR;};
   }

Alternatives
------------

1: Webservers
^^^^^^^^^^^^^
Apache with mod_wsgi is the recommended method of deploying OpenREM/Django. You can use other web servers, for example
nginx. You can read more about `Apache and mod_wsgi on the Django website
<https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/>`_ and also about other methods on the subsequent
pages on the same site.

Alternatively, a built-in web server is included that will suffice for testing purposes and getting started.

2: DICOM Store node
^^^^^^^^^^^^^^^^^^^
Any DICOM Store can be used, as long as it can be used to call the OpenREM import script. A built-in store is
available, but not recommended for production use. See :doc:`netdicom-nodes` for more details. Conquest is the
recommended DICOM Store service to use.

3: Database
^^^^^^^^^^^
PostgreSQL is the recommended database to use with OpenREM. It is the only database that OpenREM will calculate
median values for charts with. Other databases can be used with varying capabilities; see the `Django documentation
<https://docs.djangoproject.com/en/1.8/ref/databases/>`_ for more details. For testing only, the built-in SQLite3
database can be used, but this is not suitable for later migration to a production database.
