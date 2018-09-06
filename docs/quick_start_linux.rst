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

    dose@ubuntu1804:~$ sudo nano /etc/hosts

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
    mkdir static
    mkdir veopenrem
    sudo chown -R $USER:openrem /var/dose/*
    sudo chmod -R g+s /var/dose/*




Install apt packages
--------------------

.. code-block:: console

    sudo apt update
    sudo apt install python python-pip virtualenv rabbitmq-server postgresql orthanc dcmtk default-jre

Now create a virtualenv (Python local environment) in the folder we created:

.. code-block:: console

    virtualenv /var/dose/veopenrem

Install Python packages
-----------------------

Activate the virtualenv and install the python packages (note the ``.`` – you can also use the word ``source``):

.. code-block:: console

    . /var/dose/veopenrem/bin/activate
    pip install numpy psycopg2-binary





*From pre-install quick-start docs*

You will then need to setup the :doc:`postgresql` and download the latest version of the pixelmed.jar application
e.g.::

    (veopenrem) dose@ubuntu1804:~$ wget http://www.dclunie.com/pixelmed/software/webstart/pixelmed.jar


We can now install OpenREM and the customised version of pynetdicom::

    (veopenrem) dose@ubuntu1804:~$ pip install openrem==0.8.1b1
    (veopenrem) dose@ubuntu1804:~$ pip install https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2


You can now go straight to the :ref:`localsettingsconfig`.
