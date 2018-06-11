Creating bash scripts on linux
******************************

Create a bash script for each of RDSR, mammo, DX and Philips CT dose images, as required. They should have
content something like the following. The examples that follow assume the files have been saved in the folder
``/etc/conquest-dicom-server`` but you can save them where you like and change the ``dicom.ini`` commands accordingly.

These scripts have a line in them to activate the virtual environment; this is done in the line
``. /var/dose/venv/bin/activate`` – you should change the path to your virtualenv or remove it if you have installed
without using a virtualenv.

Eash script also has a line to delete the object after it has been imported – OpenREM can also do this by
configuration, but the file will be written by the ``_conquest`` user, and OpenREM will not be running as that
user. Therefore it is easier to have conquest delete the file. If you don't want them to be deleted, remove
or comment out that line (add a ``#`` character to the start of the line).

* Radiation Dose Structured Reports
* Use which ever editor you are comfortable with – a good choice might be nano. For example:

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/openrem-rdsr.sh

.. sourcecode:: bash

    #!/bin/sh
    #
    # usage: ./openrem-rdsr.sh rdsrfilepath
    #

    # Get the name of the RDSR as variable 'rdsr'
    rdsr="$1"

    # Setup the python virtual environment - change to suit your path or remove if
    # you are not using virtualenv
    . /var/dose/venv/bin/activate

    # Import RDSR into OpenREM
    openrem_rdsr.py ${rdsr}

    # Delete RDSR file - remove or comment (#) this line if you want the file to remain
    rm ${rdsr}

Save and exit, then set the script to be executable:

.. sourcecode:: console

    sudo chmod +x /etc/conquest-dicom-server/openrem-rdsr.sh

And repeat for the other modality scripts below:

* Mammography images

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/openrem-mg.sh

.. sourcecode:: bash

    #!/bin/sh
    #
    # usage: ./openrem-mg.sh mammofilepath
    #

    mamim="$1"

    . /var/dose/venv/bin/activate

    openrem_mg.py ${mamim}

    rm ${mamim}

.. sourcecode:: console

    sudo chmod +x /etc/conquest-dicom-server/openrem-mg.sh

* Radiography images (DX, and CR that might be DX)

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/openrem-dx.sh

.. sourcecode:: bash

    #!/bin/sh
    #
    # usage: ./openrem-dx.sh dxfilepath
    #

    dxim="$1"

    . /var/dose/venv/bin/activate

    openrem_dx.py ${dxim}

    rm ${dxim}

.. sourcecode:: console

    sudo chmod +x /etc/conquest-dicom-server/openrem-dx.sh

* Philips CT dose info images for Philips CT systems with no RDSR

.. sourcecode:: console

    sudo nano /etc/conquest-dicom-server/openrem-ctphilips.sh

.. sourcecode:: bash

    #!/bin/sh
    #
    # usage: ./openrem-ctphilips.sh philipsctpath
    #

    philipsim="$1"

    . /var/dose/venv/bin/activate

    openrem_ctphilips.py ${philipsim}

    rm ${philipsim}

.. sourcecode:: console

    sudo chmod +x /etc/conquest-dicom-server/openrem-ctphilips.sh
