*******************************
Offline Installation on Windows
*******************************

In order to carry out an offline installation you will need to download the OpenREM package and dependencies.
Most of the python libraries will be in tar.gz or whl formats. Ensure you have the version that matches your version of python and is 64 bit or 32 bit as appropriate. They can be installed with `pip install` filename.

We will need to update pip for compatibility even though it is included in the main python package you download.

On a computer with internet access
==================================

Download independent binaries
-----------------------------

Python from https://www.python.org/downloads/windows/

* Follow the link to the **Latest Python 2 release**
* Download either the **Windows x86 MSI installer** for 32-bit Windows or
* Download **Windows x86-64 MSI installer** for 64-bit Windows

Erlang from https://www.erlang.org/downloads

* Download the latest version of Erlang/OTP. Again, choose between
* **Windows 32-bit Binary File** or
* **Windows 64-bit Binary File**

RabbitMQ from http://www.rabbitmq.com/install-windows.html

* Download **rabbitmq-server-x.x.x.exe** from either option

Download NumPy from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

* Find the right version - look for **numpy-x.xx.x+mkl-cp27-cp27m-win32.whl** for 32-bit Windows or
* **numpy-x.xx.x+mkl-cp27-cp27m-win_amd64.whl** for 64-bit Windows.
* At the time of writing, ``x.xx.x`` was ``1.11.0`` - choose the latest version

Download pynetdicom from https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2

* The downloaded file will be named something like ``edmcdonagh-pynetdicom-2da8a57b53b3.tar.gz``

To add
^^^^^^

* Database
* Web server

Download python packages from PyPI
----------------------------------

In a console, navigate to a suitable place and create a directory to collect all the packages in, then use pip to
download them all:

.. sourcecode:: console

    mkdir openremfiles
    pip install -d openremfiles openrem==0.7.0b15

Copy everything to the Windows machine
--------------------------------------

* Add the ``pynetdicom`` file and the ``numpy`` file to the directory with the other python packages
* Copy this directory plus all the binaries to the Windows server that you are using


On the Windows server without internet access
=============================================

Installation of binaries
------------------------

Install the binaries in the following order:

1. Python
1. Erlang
1. RabbitMQ

Installation of the python packages
-----------------------------------

In a console, navigate to the directory that your openremfiles directory is in, and

.. sourcecode:: console

    pip install openremfiles\numpy‑1.11.0+mkl‑cp27-cp27m‑win32.whl
    # or if you have the 64 bit version
    pip install openremfiles\numpy‑1.11.0+mkl‑cp27-cp27m‑win_amd64.whl
    # adjusting the version number appropriately

    pip install --no-index --find-links=openremfiles openrem==0.7.0b15

    pip install openremfiles\edmcdonagh-pynetdicom-2da8a57b53b3.tar.gz

To add
^^^^^^

* Database
* Web server

Configure OpenREM ready for use
===============================

OpenREM is now installed, so go straight to the :ref:`localsettingsconfig` section of the standard installation docs