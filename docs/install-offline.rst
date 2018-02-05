*******************************
Offline Installation on Windows
*******************************

In order to carry out an offline installation you will need to download the OpenREM package and dependencies.
The instructions below should work for downloading on any operating system, as long as you have Python 2.7 and a
reasonably up to date version of pip installed.

If you have trouble when installing the Python packages due to incorrect architecture, you may need to either download
on a Windows system similar to the server (matching 32-bit/64-bit), or to download the files from
http://www.lfd.uci.edu/~gohlke/pythonlibs/ instead.

On a computer with internet access
==================================

Download independent binaries
-----------------------------

**Python** from https://www.python.org/downloads/windows/

* Follow the link to the 'Latest Python 2 release'
* Download either the ``Windows x86 MSI installer`` for 32-bit Windows or
* Download ``Windows x86-64 MSI installer`` for 64-bit Windows

**Erlang** from https://www.erlang.org/downloads

* Download the latest version of Erlang/OTP. Again, choose between
* ``Windows 32-bit Binary File`` or
* ``Windows 64-bit Binary File``

**RabbitMQ** from http://www.rabbitmq.com/install-windows.html

* Download ``rabbitmq-server-x.x.x.exe`` from either option

**PostgreSQL** from http://www.enterprisedb.com/products-services-training/pgdownload#windows

*Note: Other databases such as MySQL are also suitable, though the median function for charts will not be available. For
testing purposes only, you could skip this step and use SQLite3 which comes with OpenREM*

* Download by clicking on the icon for ``Win x86-32`` or ``Win x86-64``

**PostgreSQL Python connector** from http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg

* Find the right version - look for ``psycopg2-X-cp27-cp27m-win32.whl`` for 32-bit Windows or
* ``psycopg2-X-cp27-cp27m-win_amd64.whl`` for 64-it Windows.
* At the time of writing, ``X`` was ``2.7.3.2`` - choose the latest ``cp27`` version

**NumPy** from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

* Find the right version - look for ``numpy-X+mkl-cp27-cp27m-win32.whl`` for 32-bit Windows or
* ``numpy-X+mkl-cp27-cp27m-win_amd64.whl`` for 64-bit Windows.
* At the time of writing, ``X`` was ``1.14.0`` - choose the latest ``cp27`` version

**Pynetdicom** from https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2

* The downloaded file will be named something like ``edmcdonagh-pynetdicom-2da8a57b53b3.tar.gz``
* Note: this version is modified in comparison to the version in PyPI, and will malfunction if you use the official
  version

**A webserver** such as Apache, although this can be left till later - you can get started with the built-in web
server

Download python packages from PyPI
----------------------------------

In a console, navigate to a suitable place and create a directory to collect all the packages in, then use pip to
download them all:

.. sourcecode:: console

    mkdir openremfiles
    pip install -d openremfiles openrem==0.8.0b1

Copy everything to the Windows machine
--------------------------------------

* Add the ``pynetdicom`` file, the ``psycopg2`` file and the ``numpy`` file to the directory with the other python
  packages
* Copy this directory plus all the binaries to the Windows server that you are using


On the Windows server without internet access
=============================================

Installation of binaries
------------------------

Install the binaries in the following order:

1. Python
2. Erlang
3. RabbitMQ

Installation of the python packages
-----------------------------------

In a console, navigate to the directory that your ``openremfiles`` directory is in, and

.. sourcecode:: console

    pip install openremfiles\numpy‑1.14.0+mkl‑cp27-cp27m‑win32.whl  # update the version number
    # or if you have the 64 bit version
    pip install openremfiles\numpy‑1.14.0+mkl‑cp27-cp27m‑win_amd64.whl  # update the version number

    pip install --no-index --find-links=openremfiles openrem==0.8.0b1  # where openremfiles is the directory you created

    pip install openremfiles\edmcdonagh-pynetdicom-2da8a57b53b3.tar.gz

Install PostgreSQL
------------------

See the instructions to :ref:`windowspsqlinstall` on Windows.

Install webserver
-----------------

If you are doing so at this stage.

Configure OpenREM ready for use
===============================

OpenREM is now installed, so go straight to the :ref:`localsettingsconfig` section of the standard installation docs