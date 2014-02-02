=======
OpenREM
=======

OpenREM is a Django app to extract, store and export Radiation Exposure
Monitoring related information, primarily from DICOM files.

Detailed documentation can be found on Read the Docs: http://openrem.rtfd.org

Quick start
-----------

#. Install python (might need to be 2.7)
#. Install `setuptools and pip <http://www.pip-installer.org/en/latest/installing.html>`_
#. Install OpenREM
    + ``pip install OpenREM-ver.tar.gz``
#. Configure OpenREM
    + Locate install location, typically ``something/lib/python2.7/site-packages/openrem``
    + There are two files that need renaming:
        + ``openrem/openrem/settings.py.example`` to ``openrem/openrem/settings.py.example``
        + ``openrem/openrem/wsgi.py.example`` to ``openrem/openrem/wsgi.py.example``
    + in the ``settings.py`` file, set the database details.
    + For testing ONLY, use 
        + ``'ENGINE': 'django.db.backends.sqlite3',``
        + ``'NAME': '/ENTER/PATH/WHERE/DB/FILE/CAN/GO'``
#. Create the database
    + ``python path/to/openrem/manage.py syncdb``
    + (optional for a test database) ``python path/to/openrem/manage.py convert_to_south remapp``
#. Start test web server
    + ``python path/to/openrem/manage.py runserver``
#. Open the web addesss given, appending ``/openrem`` (http://localhost:8000/openrem)
#. Add some data!
    + ``openrem_rdsr.py rdsrfile.dcm``
