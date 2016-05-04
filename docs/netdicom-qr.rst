############################
DICOM Query Retrieve Service
############################


To query retrieve dose related objects from a remote server, you need to review the :doc:`netdicom-nodes` first.

**************************************
Query-retrieve using the web interface
**************************************
.. image:: img/QRmenu.png
    :align: right
    :alt: Import QR menu


* On the Imports menu, select ``Query remote server``. If the menu isn't there, you need to check your user permissions
  - see :ref:`user-settings` for details.
* Each configured query-retrieve node and each local store node is automatically tested to make sure they respond to a
  DICOM echo - the results are presented at the top of the page.

.. image:: img/QRstatuses.png
    :align: center
    :alt: local and remote QR statuses

* Select the desired **remote host**, ie the PACS or modality you wish to query.
* Select the local **store node** you want to retrieve to.
* Select **which modalities** you want to query for - at least one must be ticked.
* Select a **date range** - the wider this is, the more stress the query will place on the remote server, and the higher
  the likelyhood of the query being returned with zero results (a common configuration on the remote host to prevent
  large database queries affecting other services).
* If you wish to **exclude studies** based on their study description, enter the text here. Add several terms by separating
  them with a comma. One example would be to exclude any studies with ``imported`` in the study description, if
  your institution modifies this field on import. The matching is case-insensitive.
* Alternatively, you might want to only **keep studies** with particular terms in the study description. If so, enter them
  in the next box, comma separated.

Advanced query options
======================

* **Include SR only studies** *default not ticked*: If you have a DICOM store with only the radiation dose structured
  reports (RDSR) in, or a mix of whole studies and RDSRs without the corresponding study, then tick this box.
* **Ignore studies already in the database** *default ticked*: The RDSR import routine checks for the existance of the
  study UID in the database, and if it is found they it doesn't go any further. This might change in the future as there
  are instances where two RDSRs might legitimately have the same study UID, but different event UIDs. For image based
  imports, the individual events are checked, so if you think there is a reasonable chance that the database is missing
  individual images from a study, then you might like to deselect this setting. If the same dates are selected multiple
  times (to update during a day for example), activating this setting will result in the same exams all being
  transferred each time.

When you have finished the query parameters, click ``Submit``

Review and retrieve
===================

The progress of the query is reported on the right hand side. If nothing happens, ask the adminsitrator to check if the
celery queue is running.

Once all the responses have been purged of unwanted modalities, study descriptions or study UIDs, the number of studies
of each type will be displayed and a button appears. Click ``Retreive`` to request the remote server send the selected
objects to your selected Store node. This will be based on your original selection - changing the node on the left hand
side at this stage will have no effect.

The progress of the retrieve is displayed in the same place until the retrieve is complete.

***********************************************
Query-retrieve using the command line interface
***********************************************

In a command window/shell, ``qrscu.py -h`` should present you with the following output:

.. sourcecode:: console

    usage: qrscu.py [-h] [-ct] [-mg] [-fl] [-dx] [-f yyyy-mm-dd] [-t yyyy-mm-dd]
                    [-e string] [-i string] [-sr] [-dup] qrid storeid

    Query remote server and retrieve to OpenREM

    positional arguments:
      qrid                  Database ID of the remote QR node
      storeid               Database ID of the local store node

    optional arguments:
      -h, --help            show this help message and exit
      -ct                   Query for CT studies
      -mg                   Query for mammography studies
      -fl                   Query for fluoroscopy studies
      -dx                   Query for planar X-ray studies
      -f yyyy-mm-dd, --dfrom yyyy-mm-dd
                            Date from, format yyyy-mm-dd
      -t yyyy-mm-dd, --duntil yyyy-mm-dd
                            Date until, format yyyy-mm-dd
      -e string, --desc_exclude string
                            Terms to exclude in study description, comma separated, quote whole
                            string
      -i string, --desc_include string
                            Terms that must be included in study description, comma separated,
                            quote whole string
      -sr                   Advanced: Query for structured report only studies
      -dup                  Advanced: Retrieve studies that are already in database

As an example, if you wanted to query the PACS for DX images on the 5th April 2010 with any study descriptions including
``imported`` excluded, first you need to know the database IDs of the remote node and the local node you want the images
sent to. To find these, go to the :doc:`netdicom-nodes` page where the database ID is listed among the other details for
each node.

Assuming the PACS database ID is 2, and the store node ID is 1, the command would look something like:

..sourcecode:: console

    qrscu.py 2 1 -dx -f 2010-04-05 -t 2010-04-05 -e "imported"

If you want to do this regularly to catch new studies, you might like to use a script something like this on linux:

.. sourcecode:: bash

    #!/bin/bash

    . /var/openrem/bin/activate  # activate virtualenv if you are using one, modify or delete this line

    ONEHOURAGO=$(date -d "1 hour ago" "+%Y-%m-%d")

    openrem_qr.py 2 1 -dx -f $ONEHOURAGO -t $ONEHOURAGO  -e "Imported"


This script could be run once an hour using a cron job. By asking for the date an hour ago, you shouldn't miss exams
taking place in the last hour of the day.

A similar script could be created as a batch file on Windows and run using the scheduler.