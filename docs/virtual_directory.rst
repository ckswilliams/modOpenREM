**************************************************
Running the OpenREM website in a virtual directory
**************************************************

If you want to run the OpenREM in a virtual directory (like http://server/dms/) you need to configure this in your
web server application that you are using (IIS or nginx). Next to that you also need to configure this in OpenREM.
The following steps are necessary:


    - Configure virtual directory in ``local_settings.py``
    - Update the ``reverse.js`` file

Configure virtual directory in local_settings.py
================================================

Django should know in what virtual directory you are running OpenREM. Perform the following steps to do this.


    - In the OpenREM ``local_settings.py`` file, located in the openremproject directory
      (e.g. ``C:\Python27\Lib\site-packages\openrem\oprenremproject\local_settings.py``) find the ``VIRTUAL_DIRECTORY``
      variable - if there isn't one, somewhere in the ``local_settings.py`` file add ``VIRTUAL_DIRECTORY=''`` at the
      start of a line.
    - Set this variable to the desired virtual directory
    - Add under this line the following code to set the ``STATIC_URL`` variable

        .. code-block:: python

            STATIC_URL = '/' + os.path.join(VIRTUAL_DIRECTORY, STATIC_URL.lstrip('/'))

    - In order to make this command work ``os`` has to be imported, add in ``local_settings.py`` as third line

        .. code-block:: python

            import os

    - Instead of the above two changes, you can also put a hard-coded STATIC_URL as follows

        .. code-block:: python

            STATIC_URL = '/VIRTUAL_DIRECTORY/static/'

     (replace ``VIRTUAL_DIRECTORY`` by the actual value):


    ..  note::

        - Take care the virtual directory name ends with a slash (``/``)
        - Take care the virtual directory name is exactly the same as configured in the web server (this is
          case-sensitive)

Update reverse.js
=================

The static reverse.js file should be updated in order to change the URLs in the static javascript files also.

    - Open a command prompt and navigate to the openrem directory, e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Type ``python manage.py collectstatic_js_reverse``

    ..  note::

        Take care the resulting ``reverse.js`` is written to the correct static directory.
        If that is not the case copy the file manually to the correct location.
