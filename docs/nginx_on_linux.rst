************************************************
Running OpenREM on Linux with Gunicorn and NGINX
************************************************

These instructions are for running OpenREM with Gunicorn and NGINX on Ubuntu Server, but should work on other Linux
distributions with minimal modification.
These instructions are based on https://www.obeythetestinggoat.com/book/chapter_making_deployment_production_ready.html

Prerequisites
=============

    + A working OpenREM installation, that serves web pages using the built-in web server. You can test this using the
      instructions in :doc:`startservices`

Steps to perform
================

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

Save (``Ctrl-o``) and exit (``Ctrl-x``).

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
``media`` folder. For example, if you created your media folder in ``/var/openrem/media``. We will need to make user the
permissions will be suitable. For example:

.. sourcecode:: bash

    sudo mkdir /var/openrem/static
    sudo chown $USER:www-data /var/openrem/static
    sudo chmod 755 /var/openrem/static

Now edit your ``openrem/openremproject/local_settings.py`` config file to put the same path in the ``STATIC_ROOT``:

.. sourcecode:: bash

    nano local_settings.py

    # Find the static files section
    STATIC_ROOT = '/var/openrem/static'  # replacing path as appropriate

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