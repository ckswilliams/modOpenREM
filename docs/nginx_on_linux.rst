************************************************
Running OpenREM on Linux with Gunicorn and NGINX
************************************************

These instructions are for running OpenREM with Gunicorn and NGINX on Ubuntu Server, but should work on other Linux
distributions with minimal modification.
These instructions are based on a guide at
`obeythetestingoat.com <https://www.obeythetestinggoat.com/book/chapter_making_deployment_production_ready.html>`_



Prerequisites
=============

    + A working OpenREM installation, that serves web pages using the built-in web server. You can test this using the
      instructions in :doc:`startservices`

.. contents:: :local:

Steps to perform
================

.. note::

    If you get stuck somewhere in these instructions, please check the :ref:`troubleshooting` section at the end of this
    page.

Install NGINX
^^^^^^^^^^^^^

.. sourcecode:: bash

    sudo apt install nginx
    sudo systemctl start nginx

You should now be able to see the 'Welcome to nginx' page if you go to your server address in a web browser.

Create initial nginx configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new config file - you can name the file as you like, but it is usually has the server name.

.. sourcecode:: bash

    sudo nano /etc/nginx/sites-available/openrem-server

Start with the following settings - replace the server name with the hostname of your server. For this example, I will
use ``openrem-server``

.. sourcecode:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location / {
            proxy_pass http://localhost:8000;
        }
    }

Save and exit (see :ref:`nano` below for tips).

Now delete the default nginx configuration from ``sites-enabled`` and make a link to our new one:

.. sourcecode:: bash

    sudo rm /etc/nginx/sites-enabled/default
    sudo ln -s /etc/nginx/sites-available/openrem-server /etc/nginx/sites-enabled/openrem-server

Now we reload nginx and start our server as before to test this step. At this stage, nginx is simply passing requests to
the default port (80) on to port 8000 to be dealt with (which is why we need to start the test server again).

.. sourcecode:: bash

    sudo systemctl reload nginx
    # activate your virtual environment if you are using one
    # navigate to the openrem folder with manage.py in
    python manage.py runserver

Now use your web browser to look at your server again - the 'Welcome to nginx' page should be replaced by an ugly
version of the OpenREM website - this is because the 'static' files are not yet being served - we'll fix this later.

Replace runserver with Gunicorn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Activate your virtualenv if you are using one (add sudo if your aren't), and:

.. sourcecode:: bash

    pip install gunicorn

Make sure you have stopped the test webserver (``Ctrl-c`` in the shell ``runserver`` is running in), then from the same
openrem folder:

.. sourcecode:: bash

    gunicorn openremproject.wsgi:application

The Gunicorn server should start, and you should be able to see the same broken version of the web interface again.

Serve static files using nginx
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a folder called ``static`` somewhere that your webserver user will be able to get to - for example alongside the
``media`` folder, and set the permissions. So if you created your media folder in ``/var/openrem/media``, you might
do this:

.. sourcecode:: bash

    sudo mkdir /var/openrem/static
    sudo chown $USER:www-data /var/openrem/static
    sudo chmod 755 /var/openrem/static

Now edit your ``openremproject/local_settings.py`` config file to put the same path in the ``STATIC_ROOT``:

.. sourcecode:: bash

    nano local_settings.py

    # Find the static files section
    STATIC_ROOT = '/var/openrem/static/'  # replacing path as appropriate

Now use the Django ``manage.py`` application to pull all the static files into the new folder:

.. sourcecode:: bash

    python manage.py collectstatic

Now we need to tell nginx to serve them:

.. sourcecode:: bash

    sudo nano /etc/nginx/sites-available/openrem-server

And modify the file to add the ``static`` section - remember to put the path you have used instead of
``/var/openrem/static``

.. sourcecode:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location /static {
            alias /var/openrem/static;
        }

        location / {
            proxy_pass http://localhost:8000;
        }
    }

Now reload nginx and gunicorn to see if it is all working...

.. sourcecode:: bash

    sudo systemctl reload nginx
    # activate your virtual environment if you are using one
    # navigate to the openrem folder with manage.py in
    gunicorn openremproject.wsgi:application

Take another look, and it should all be looking nice now!

Switch to using Unix Sockets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step is optional, but does allow you more flexibility if you need to do anything else on this server using port
8000 as this installation of OpenREM will no longer be using that port. Instead we'll use 'sockets', which are like
files on the disk. We put these in ``/tmp/``.

Change the nginx configuration again (``sudo nano /etc/nginx/sites-available/openrem-server``):

.. sourcecode:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location /static {
            alias /var/openrem/static;
        }

        location / {
            proxy_pass http://unix:/tmp/openrem-server.socket;
        }
    }

Now restart Gunicorn, this time telling it to use the socket, after reloading nginx:

.. sourcecode:: bash

    sudo systemctl reload nginx
    gunicorn --bind unix:/tmp/openrem-server.socket \
    openremproject.wsgi:application

The ``\`` just allows the command to spread to two lines - feel free to put it all on one line.

Check the web interface again, hopefully it should still be working!

Start Gunicorn automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can use systemd on Ubuntu to ensure Gunicorn starts on boot and restarts if it crashes. As before, change each
instance of ``openrem-server`` for the name of your server. You will need to change the ``WorkingDirectory`` to match
the path to your openrem folder.

For the gunicorn command, you will need to provide the full path to gunicorn, whether that is in
``/usr/local/bin/gunicorn`` or the bin folder of your virtualenv.

.. sourcecode:: bash

    # Customise the name of the file as you please - it must end in .service
     sudo nano /etc/systemd/system/gunicorn-openrem-server.service

.. sourcecode:: systemd

    [Unit]
    Description=Gunicorn server for openrem-server

    [Service]
    Restart=on-failure
    User=www-data
    WorkingDirectory=/usr/local/lib/python2.7/dist-packages/openrem

    ExecStart=/usr/local/bin/gunicorn \
        --bind unix:/tmp/openrem-server.socket \
        openremproject.wsgi:application

    [Install]
    WantedBy=multi-user.target

Make sure you have customised the ``User``, the  ``WorkingDirectory`` path, the path to gunicorn, and the name of the
socket file.

.. warning::

    If the user you have configured can't write to the ``STATIC_ROOT`` folder, the ``MEDIA_ROOT`` folder and
    the location the logs are configured to be written (usually in ``MEDIA_ROOT``), the systemd gunicorn service is
    likely to fail when started.

    If you have installed everything in your user folder, you are likely to need to set ``User`` to your own username.

Now enable the new configuration:

.. sourcecode:: bash

    # Load to config
    sudo systemctl daemon-reload
    # Enable start on boot - change the name as per how you created it
    sudo systemctl enable gunicorn-openrem-server.service
    # Now start the service
    sudo systemctl start gunicorn-openrem-server.service

You might like to see if it worked...

.. sourcecode:: bash

    sudo systemctl status gunicorn-openrem-server.service

Look for ``Active: active (running)``


Making use of ALLOWED_HOSTS in local_settings.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default setting of ``ALLOWED_HOSTS`` is ``*`` which isn't secure, but is convenient! We should really change this
to match the hostname of the server.

If your hostname is ``openrem-server``, and the fully qualified domain name is ``openrem-server.ad.hospital.org`` and
IP address is ``10.212.18.209``, then you might configure ``ALLOWED_HOSTS`` in ``openremproject/local_settings.py`` to:

.. sourcecode:: python

    ALLOWED_HOSTS = [
        'openrem-server',
        'openrem-server.ad.hospital.org',
        '10.212.18.209',
    ]

.. note::

    Which hostnames do I need to put in ``ALLOWED_HOSTS``? You need to put in any hostnames you want people to be able
    to access your OpenREM web interface at. So if in your hospital you only type in the address bar the hostname
    (``http://openrem-server`` in this example), then that is all you need to add. If you only use the IP address, then add
    that. If you can use any of them, add them all :-)

Next we need to edit the nginx configuration again to make sure Django can see the hostname by adding the
``proxy_set_header`` configuration (else it gets lost before Django can check it):

.. sourcecode:: bash

    sudo nano /etc/nginx/sites-available/openrem-server

.. sourcecode:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location /static {
            alias /var/openrem/static;
        }

        location / {
            proxy_pass http://unix:/tmp/openrem-server.socket;
            proxy_set_header Host $host;
        }
    }

Now reload the nginx configuration and reload Gunicorn:

.. sourcecode:: bash

    sudo systemctl reload nginx
    sudo systemctl restart gunicorn-openrem-server.service

And check the web interface again. If it doesn't work due to the ``ALLOWED_HOSTS`` setting, you will get a 'Bad request
400' error.

Increasing the timeout
^^^^^^^^^^^^^^^^^^^^^^

You may wish to do this to allow for :doc:`skindosemap` that can take more than 30 seconds for complex studies. Both
Gunicorn and nginx configurations need to be modified:

.. sourcecode:: bash

     sudo nano /etc/systemd/system/gunicorn-openrem-server.service

Add the ``--timeout`` setting to the end of the ``ExecStart`` command, time is in seconds (300 = 5 minutes,
1200 = 20 minutes)

.. sourcecode:: systemd

    [Unit]
    Description=Gunicorn server for openrem-server

    [Service]
    Restart=on-failure
    User=www-data
    WorkingDirectory=/usr/local/lib/python2.7/dist-packages/openrem

    ExecStart=/usr/local/bin/gunicorn \
        --bind unix:/tmp/openrem-server.socket \
        openremproject.wsgi:application --timeout 300

    [Install]
    WantedBy=multi-user.target


.. sourcecode:: bash

    sudo nano /etc/nginx/sites-available/openrem-server

Add the ``proxy_read_timeout`` setting in seconds (note the trailing ``s`` this time).

.. sourcecode:: nginx

    server {
        listen 80;
        server_name openrem-server;

        location /static {
            alias /var/openrem/static;
        }

        location / {
            proxy_pass http://unix:/tmp/openrem-server.socket;
            proxy_set_header Host $host;
            proxy_read_timeout 300s;
        }
    }

Reload everything:

.. sourcecode:: bash

    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn-openrem-server.service
    sudo systemctl reload nginx

.. Note::

    If you have jumped straight to here to get the final config, then make sure you substitute all the following values
    to suit your install:

    * ``gunicorn-openrem-server.service`` - name not important (except the ``.service``, but you need to use it in the
      reload commands etc
    * ``User=www-data`` as appropriate. This should either be your user or ``www-data``. You will need to ensure folder
      permissions correspond
    * ``WorkingDirectory`` needs to match the path to your ``openrem`` folder (the one with ``manage.py`` in)
    * ``ExecStart=/usr/local/bin/gunicorn \`` needs to match the path to your ``gunicorn`` executable - either in your
      virtualenv bin folder or system wide as per the example
    * ``--bind unix:/tmp/openrem-server.socket \`` name in ``tmp`` doesn't matter, needs to match in gunicorn and nginx
      configs
    * ``/etc/nginx/sites-available/openrem-server`` ie name of config file in nginx, doesn't matter, usually matches
      hostname
    * ``server_name openrem-server`` - should match hostname
    * ``/var/openrem/static`` folder must exist, with the right permissions. Location not important, must match setting
      in ``local_settings``
    * ``proxy_pass http://unix:/tmp/openrem-server.socket;`` must match setting in gunicorn config, prefixed with
      ``http://``

    You will also need to ``collectstatic``, symlink the nginx configuration into enabled, enable the gunicorn systemd
    config to start on reboot, and you should configure the ``ALLOWED_HOST`` setting. And you will need to have
    installed nginx and gunicorn!


..  _troubleshooting:

Troubleshooting and tips
========================

less
^^^^
Use ``less`` to review files without editing them

* Navigate using arrow keys, page up and down,
* ``Shift-G`` to go to the end
* ``Shift-F`` to automatically update as new logs are added. ``Ctrl-C`` to stop.
* ``/`` to search

.. _nano:

nano
^^^^
Use ``nano`` to edit the files.

* ``Ctrl-o`` to save ('out')
* ``Ctrl-x`` to exit

Nginx
^^^^^

* Logs are located in ``/var/log/nginx/``
* You need root privileges to view the files:

    * To view latest error log: ``sudo less /var/log/nginx/error.log``

* Reload: ``sudo systemctl reload nginx``
* Check nginx config: ``sudo nginx -t``

Systemd and Gunicorn
^^^^^^^^^^^^^^^^^^^^

* Review the logs with ``sudo journalctl -u gunicorn-openrem-server`` (change as appropriate for the the name you have
  used)
* Check the systemd configuration with ``systemd-analyze verify /etc/systemd/system/gunicorn-openrem-server.service`` -
  again changing the name as appropriate.
* If you make changes, you need to use ``sudo systemctl daemon-reload`` before the changes will take effect.
* Restart: ``sudo systemctl restart gunicorn-openrem-server.service``


