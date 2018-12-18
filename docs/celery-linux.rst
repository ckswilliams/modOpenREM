######################################
Daemonising Celery and Flower on Linux
######################################

Guides to daemonising Celery can be found in the Celery documentation at
http://docs.celeryproject.org/en/latest/userguide/daemonizing.html.

Alternatively, if you are running Ubuntu 18.04 or another systemd based Linux operating system, the instructions below
are taken from the Celery docs but customised for OpenREM.

In this example, the following folders have been created:

* :file:`/var/dose/celery/`
* :file:`/var/dose/log/`
* :file:`/var/dose/veopenrem/`

OpenREM is installed in a virtualenv in ``/var/dose/veopenrem/``.

Adjust all the paths as appropriate. If you change the default port from 5555 then you need to make the same change in
``openremproject\local_settings.py`` to add/modify the line ``FLOWER_PORT = 5555``

First, create a Celery configuration file:

``nano /var/dose/celery/celery.conf``:

.. code-block:: bash

    # Name of nodes to start
    CELERYD_NODES="default"

    # Absolute or relative path to the 'celery' command:
    CELERY_BIN="/var/dose/veopenrem/bin/celery"

    # App instance to use
    CELERY_APP="openremproject"

    # How to call manage.py
    CELERYD_MULTI="multi"

    # Extra command-line arguments to the worker
    # Adjust the concurrency as appropriate
    CELERYD_OPTS="-O=fair --concurrency=4 --queues=default"

    # - %n will be replaced with the first part of the nodename.
    # - %I will be replaced with the current child process index
    #   and is important when using the prefork pool to avoid race conditions.
    CELERYD_PID_FILE="/var/dose/celery/%n.pid"
    CELERYD_LOG_FILE="/var/dose/log/%n%I.log"
    CELERYD_LOG_LEVEL="INFO"

    # Flower configuration options
    FLOWER_PORT=5555
    FLOWER_LOG_PREFIX="/var/dose/log/flower.log"
    FLOWER_LOG_LEVEL="INFO"

Now create the systemd service files:

``sudo nano /etc/systemd/system/celery-openrem.service``:

.. code-block:: bash

    [Unit]
    Description=Celery Service
    After=network.target

    [Service]
    Type=forking
    Restart=on-failure
    User=www-data
    Group=www-data
    EnvironmentFile=/var/dose/celery/celery.conf
    WorkingDirectory=/var/dose/veopenrem/lib/python2.7/site-packages/openrem
    ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
      --pidfile=${CELERYD_PID_FILE}'
    ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

    [Install]
    WantedBy=multi-user.target

``sudo nano /etc/systemd/system/flower-openrem.service``:

.. code-block:: bash

    [Unit]
    Description=Flower Celery Service
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    EnvironmentFile=/var/dose/celery/celery.conf
    WorkingDirectory=/var/dose/veopenrem/lib/python2.7/site-packages/openrem
    ExecStart=/bin/sh -c '${CELERY_BIN} flower -A ${CELERY_APP} --port=${FLOWER_PORT} \
      --address=127.0.0.1 --log-file-prefix=${FLOWER_LOG_PREFIX} --loglevel=${FLOWER_LOG_LEVEL}'
    Restart=on-failure
    Type=simple

    [Install]
    WantedBy=multi-user.target

Now register, set to start on boot, and start the services:

.. code-block:: console

    sudo systemctl daemon-reload
    sudo systemctl enable celery-openrem.service
    sudo systemctl start celery-openrem.service
    sudo systemctl enable flower-openrem.service
    sudo systemctl start flower-openrem.service
