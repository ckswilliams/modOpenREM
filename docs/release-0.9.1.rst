########################
Upgrade to OpenREM 0.9.1
########################

****************
Headline changes
****************





****************************
Upgrading from version 0.8.x
****************************

* Enable RabbitMQ management interface
* Enable Flower
* Fix Celery on Windows at 3.1.25
* E-mail server settings



****************************
Upgrading from version 0.9.0
****************************


Ubuntu installs that followed :doc:`quick_start_linux`
======================================================

Systemd service files have been renamed in these docs to use *openrem-function* rather than *function-openrem*. To
update the service files accordingly, follow the following steps. **This is optional**, but will make finding them
easier (e.g. ``sudo systemctl status openrem[tab][tab]`` will list them!)

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
