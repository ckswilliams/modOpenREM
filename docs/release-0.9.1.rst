########################
Upgrade to OpenREM 0.9.1
########################

****************
Headline changes
****************

*******************
Upgrade preparation
*******************

Version 0.9 of OpenREM has a minimum Python 2.7 version and a minimum version of setuptools. If your installation was
originally for OpenREM 0.6 in 2014 or earlier, these may now be too old and need updating.

To check the Python version, activate the virtualenv if you are using one, then:

.. code-block:: console

    python -V

If the version is earlier than ``2.7.9``, then an upgrade is needed.

**Ubuntu Linux**

* Check which version of Ubuntu is installed (``lsb_release -a``)
* If it is 14.04 LTS (Trusty), then an operating system upgrade or transfer to a new server is required (see later)
* 16.04 LTS (Xenial) or later should have 2.7.11 or later available.
* For other Linux distributions check in their archives for which versions are available.

**Windows**

* A newer version of Python 2.7 can be downloaded from `python.org <https://www.python.org/downloads>`_ and installed
  over the current version.

**Linux and Windows**

* With a version of Python 2.7.9 or later (**not Python 3**), setuptools can be updated (activate virtualenv if using
  one:

    .. code-block:: console

        pip install setuptools -U

****************************
Upgrading from version 0.7.4
****************************




****************************
Upgrading from version 0.8.x
****************************

* Enable RabbitMQ management interface
* Enable Flower
* Fix Celery on Windows at 3.1.25
* E-mail server settings
* Update setuptools (




****************************
Upgrading from version 0.9.0
****************************


Ubuntu installs that followed :doc:`quick_start_linux`
======================================================

Systemd service files have been renamed in these docs to use *openrem-function* rather than *function-openrem*. To
update the service files accordingly, follow the following steps. **This is optional**, but will make finding them
easier (e.g. ``sudo systemctl status openrem-[tab][tab]`` will list them!)

.. sourcecode:: console

    sudo systemctl stop gunicorn-openrem.service
    sudo systemctl stop celery-openrem.service
    sudo systemctl stop flower-openrem.service

    sudo systemctl disable gunicorn-openrem.service
    sudo systemctl disable celery-openrem.service
    sudo systemctl disable flower-openrem.service

    sudo mv /etc/systemd/system/{gunicorn-openrem,openrem-gunicorn}.service
    sudo mv /etc/systemd/system/{celery-openrem,openrem-celery}.service
    sudo mv /etc/systemd/system/{flower-openrem,openrem-flower}.service

    sudo systemctl enable openrem-gunicorn.service
    sudo systemctl enable openrem-celery.service
    sudo systemctl enable openrem-flower.service

    sudo systemctl start openrem-gunicorn.service
    sudo systemctl start openrem-celery.service
    sudo systemctl start openrem-flower.service
