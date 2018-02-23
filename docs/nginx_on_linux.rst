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

.. sourcecode:: console

    sudo apt install nginx
    sudo systemctl start nginx

You should now be able to see the 'Welcome to nginx' page if you go to your server address in a web browser.

Create initial nginx configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new config file - you can name the file as you like, but it is usually has the server name.

.. sourcecode:: bash

    sudo nano /etc/nginx/sites-available/openrem

Start with the following settings - replace the server name with the hostname of your server

.. sourcecode:: nginx

    server {
        listen 80;
        server_name superlists-staging.ottg.eu;

        location / {
            proxy_pass http://localhost:8000;
        }
    }