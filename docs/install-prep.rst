**************************
Before you install OpenREM
**************************

Install Python 2.7.x
====================

* Linux – likely to be installed already
* Windows – instructions and downloads are available at `python.org <https://www.python.org/downloads>`_

Add Python and the scripts folder to the path
---------------------------------------------
*Windows only – this is usually automatic in linux*

During the Windows Python 2.7 installation, you can choose to add Python.exe to Path – choose this option:

.. figure:: img/PythonWindowsPath.png
    :alt: Add Python to Path image

    Add Python to Path – install this option

If Python is already installed, you can add Python to Path yourself:

    Add the following to the end of the ``path`` environment variable (to see
    how to edit the environment variables, see http://www.computerhope.com/issues/ch000549.htm)::

        ;C:\Python27\;C:\Python27\Scripts\

Setuptools and pip
------------------

Install setuptools and pip – for details go to
http://www.pip-installer.org/en/latest/installing.html. The quick version
is as follows:

Linux

    Download the latest version using the same method as for Windows, or
    get the version in your package manager, for example::

        sudo apt-get install python-pip

Windows

    Download the installer script `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_
    and save it locally – right click and *Save link as...* or equivalent.

    Open a command window (Start menu, cmd.exe) and navigate to the place
    you saved the get‑pip.py file::

        python get-pip.py



Quick check of python and pip
`````````````````````````````

To check everything is installed correctly so far, type the following in a 
command window/shell. You should have the version number of pip returned to 
you::

    pip -V

Install RabbitMQ
----------------

* Linux - Follow the guide at http://www.rabbitmq.com/install-debian.html
* Windows - Follow the guide at http://www.rabbitmq.com/install-windows.html

For either install, just follow the defaults – no special configurations required.

..  Note::

    Before continuing, `consider virtualenv`_

Install NumPy
-------------
*(New for version 0.6.0)*

Numpy is required for charts. OpenREM will work without NumPy, but charts will not be displayed.

For linux::

    sudo apt-get install python-numpy
    # If using a virtualenv, you might need to also do:
    pip install numpy

For Windows, there are various options:

1. Download executable install file from SourceForge:

    * Download a pre-compiled Win32 .exe NumPy file from http://sourceforge.net/projects/numpy/files/NumPy/. You need to
      download the file that matches the Python version, which should be 2.7. At the time of writing the latest version was
      1.9.2, and the filename to download was ``numpy-1.9.2-win32-superpack-python2.7.exe``. The filename is truncated on
      SourceForge, so you may need to click on the *i* icon to see which is which. It's usually the third *superpack*.
    * Run the downloaded binary file to install NumPy.

2. Or download a ``pip`` installable wheel file:

    * Download NumPy from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy - ``numpy‑1.9.2+mkl‑cp27‑none‑win32.whl`` is
      likely to be the right version, unless you have 64bit Python installed, in which case use the
      ``numpy‑1.9.2+mkl‑cp27‑none‑win_amd64.whl`` version instead.
    * Install using pip::

        pip install numpy‑1.9.2+mkl‑cp27‑none‑win32.whl

Install pynetdicom
------------------
*(New for version 0.6.0)*

Pynetdicom is used for the new DICOM store SCP function that is available as a preview in this release. See
:doc:`netdicom` for details.

.. sourcecode:: bash

    pip install https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _(What is south?): `Database migrations`_
.. _consider virtualenv: `Virtualenv and virtualenvwrapper`_