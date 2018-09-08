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
    sudo apt install python python-pip virtualenv rabbitmq-server postgresql nginx orthanc dcmtk default-jre

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
    pip install numpy psycopg2-binary gunicorn
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

First navigate to the Python openrem folder and copy the example local_settings and wsgi files to remove the
``.example`` suffixes:

.. code-block:: console

    cd /var/dose/veopenrem/lib/python2.7/site-packages/openrem/
    cp openremproject/local_settings.py{.example,}
    cp openremproject/wsgi.py{.example,}

Edit the new local_settings file (``nano openremproject/local_settings.py``):

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'openremdb',
            'USER': 'openremuser',
            'PASSWORD': 'mysecretpassword',     # This needs changing, hopefully!
            'HOST': '',
            'PORT': '',
        }
    }

    MEDIA_ROOT = '/var/dose/media/'

    STATIC_ROOT = '/var/dose/static/'

    # Change secret key

    # Leave the hash in place for now, but remove it and the space so DEBUG starts at the start of the line as soon as
    # something doesn't work. Put it back when you get it working again.
    # DEBUG = True

    ALLOWED_HOSTS = [
        # Add the names and IP address of your host, for example:
        'openrem-server',
        'openrem-server.ad.abc.nhs.uk',
        '10.123.213.22',
    ]

    LOG_ROOT = "/var/dose/log"
    logfilename = os.path.join(LOG_ROOT, "openrem.log")
    qrfilename = os.path.join(LOG_ROOT, "openrem_qr.log")
    storefilename = os.path.join(LOG_ROOT, "openrem_store.log")
    extractorfilename = os.path.join(LOG_ROOT, "openrem_extractor.log")

    # Removed comment hashes to enable log file rotation:
    LOGGING['handlers']['file']['class'] = 'logging.handlers.RotatingFileHandler'
    LOGGING['handlers']['file']['maxBytes'] = 10 * 1024 * 1024  # 10*1024*1024 = 10 MB
    LOGGING['handlers']['file']['backupCount'] = 5  # number of log files to keep before deleting the oldest one
    LOGGING['handlers']['qr_file']['class'] = 'logging.handlers.RotatingFileHandler'
    LOGGING['handlers']['qr_file']['maxBytes'] = 10 * 1024 * 1024  # 10*1024*1024 = 10 MB
    LOGGING['handlers']['qr_file']['backupCount'] = 5  # number of log files to keep before deleting the oldest one
    LOGGING['handlers']['store_file']['class'] = 'logging.handlers.RotatingFileHandler'
    LOGGING['handlers']['store_file']['maxBytes'] = 10 * 1024 * 1024  # 10*1024*1024 = 10 MB
    LOGGING['handlers']['store_file']['backupCount'] = 5  # number of log files to keep before deleting the oldest one
    LOGGING['handlers']['extractor_file']['class'] = 'logging.handlers.RotatingFileHandler'
    LOGGING['handlers']['extractor_file']['maxBytes'] = 10 * 1024 * 1024  # 10*1024*1024 = 10 MB
    LOGGING['handlers']['extractor_file']['backupCount'] = 5  # number of log files to keep before deleting the oldest one

    DCMTK_PATH = '/usr/bin'
    DCMCONV = os.path.join(DCMTK_PATH, 'dcmconv')
    DCMMKDIR = os.path.join(DCMTK_PATH, 'dcmmkdir')
    JAVA_EXE = '/usr/bin/java'
    JAVA_OPTIONS = '-Xms256m -Xmx512m -Xss1m -cp'
    PIXELMED_JAR = '/var/dose/pixelmed/pixelmed.jar'
    PIXELMED_JAR_OPTIONS = '-Djava.awt.headless=true com.pixelmed.doseocr.OCR -'

Now create the database = assuming you are still in ``/var/dose/veopenrem/lib/python2.7/site-packages/openrem/``:

.. code-block:: console

    python manage.py makemigrations remapp
    python manage.py migrate
    python manage.py createsuperuser
    mv remapp/migrations/0002_0_7_fresh_install_add_median.py{.inactive,}
    python manage.py migrate

Configure NGINX and gunicorn
----------------------------

Start NGINX:

.. code-block:: console

    sudo systemctl start nginx

Create the OpenREM site config file ``sudo nano /etc/nginx/sites-available/openrem-server``:

.. code-block:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location /static {
            alias /var/dose/static;
        }

        location / {
            proxy_pass http://unix:/tmp/openrem-server.socket;
            proxy_set_header Host $host;
            proxy_read_timeout 300s;
        }
    }














