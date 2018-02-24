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
the default port (80) on to port 8000 to be dealt with (which is why we need to start the test server again.

.. sourcecode:: bash

    sudo systemctl reload nginx
    # activate your virtual environment if you are using one
    # navigate to the openrem folder with manage.py in
    python manage.py runserver

Now use your web browser to look at your server again - the 'Welcome to nginx' page should be replaced by an ugly
version of the OpenREM website - this is because the 'static' files are not yet being served - we'll fix this later.