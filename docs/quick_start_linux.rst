Quick start: Ubuntu install
===========================

A one page install based on Ubuntu 18.04 using:

* Python 2.7 running in a virtualenv
* Database: PostgreSQL
* DICOM Store SCP: Orthanc running on port 104
* Webserver: NGINX with Gunicorn
* Daemonisation: systemd scripts for Celery and Gunicorn
* All OpenREM files in ``/var/dose/`` with group owner of ``openrem``

Pre-install prep
----------------
First edit ``/etc/hosts`` to add the local server name – else ``rabbitmq-server`` will not start when installed::

    sudo nano /etc/hosts

Modify the content to ensure the following two lines are present - **substitute the correct server hostname on the
second line**::

    127.0.0.1 localhost
    127.0.1.1 ubuntu1804

``Ctrl-o Ctrl-x`` to write out and exit

Now create new group ``openrem`` and add your user to it (``$USER`` will automatically substitute for the user you are
running as) :

.. code-block:: console

    sudo groupadd openrem
    sudo adduser $USER openrem

At a later stage, to add a second administrator just add them to the ``openrem`` group in the same way.

Create the folders we need, and set the permissions. In due course, the ``orthanc`` user and the ``www-data`` user will
be added to the ``openrem`` group, and the 'sticky' group setting below will enable both users to write to the logs etc:

.. code-block:: console

    sudo mkdir /var/dose
    sudo chown $USER:openrem /var/dose
    sudo chmod 775 /var/dose
    cd /var/dose
    mkdir celery
    mkdir log
    mkdir media
    mkdir -p orthanc/dicom
    mkdir pixelmed
    mkdir static
    mkdir veopenrem
    sudo chown -R $USER:openrem /var/dose/*
    sudo chmod -R g+s /var/dose/*


Install apt packages and direct downloads
-----------------------------------------

.. code-block:: console

    sudo apt update
    sudo apt install python python-pip virtualenv rabbitmq-server postgresql orthanc dcmtk default-jre

    cd /var/dose/pixelmed
    wget http://www.dclunie.com/pixelmed/software/webstart/pixelmed.jar


Install Python packages
-----------------------

Create a virtualenv (Python local environment) in the folder we created:

.. code-block:: console

    virtualenv /var/dose/veopenrem

Activate the virtualenv and install the python packages (note the ``.`` – you can also use the word ``source``):

.. code-block:: console

    . /var/dose/veopenrem/bin/activate
    pip install numpy psycopg2-binary
    pip install openrem
    pip install https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2


Setup PostgreSQL database
-------------------------

*Need to establish if it really is necessary to change security configuration - I am thinking it might not be*

Create a postgres user, and create the database. You will be asked to enter a new password (twice). This will be needed
when configuring OpenREM:

.. code-block:: console

    sudo -u postgres createuser -P openremuser
    sudo -u postgres createdb -T template1 -O openremuser -E 'UTF8' openremdb

If you are migrating from another server, you could at this point create a template0 database to restore into. See
:ref:`restore-psql-linux` for details.


Configure OpenREM
-----------------

First navigate to the Python openrem folder and copy the example local_settings and wsgi files:

.. code-block:: console

    cd /var/dose/veopenrem/lib/python2.7/site-packages/openrem/
    cp openremproject/local_settings.py{.example,}
    cp openremproject/wsgi.py{.example,}

