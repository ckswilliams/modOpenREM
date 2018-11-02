**************************************************
Running the OpenREM website in a virtual directory
**************************************************

If you want to run the OpenREM in a virtual directory (like http://server/dms/) you need to configure this in your
web server application that you are using (IIS or nginx). Next to that you also need to configure this in OpenREM.
The following steps are necessary:


    - Configure virtual directory in local_settings.py
    - Update the reverse.py

Configure virtual directory in local_settings.py
================================================

Django should know in what virtual directory you are running OpenREM. Perform the following steps to do this.


    - In the Openrem ``local_settings.py`` file, located in the openremproject directory
      (e.g. ``C:\Python27\Lib\site-packages\openrem\oprenremproject\local_settings.py``) find the ``VIRTUAL_DIRECTORY`` variable
    - Set this variable to the desired virtual directory

   ..  Note::
     - Take care the virtual directory name ends with a slash (/)
     - Take care the virtual directory name is exactly the same as configured in the web server (this is case-sensitive)

Update the reverse.py
=====================

The static reverse.py file should be updated in order to change the URLs in the static javascript files also.

    ..  Warning::

      The current version of django-js-reverse (v0.8.2) has an ommission.
      To prevent a wrong update, you have to edit the collectstatic_js_reverse.py file of this package.

      - Browse to the ``collectstatic_js_reverse.py`` file, e.g.
        ``C:\Python27\Lib\site-packages\django_js_reverse\management\commands``
      - Open the file in an editor
      - line 40 ("``default_urlresolver = get_resolver(None)``") should be replaced with the following lines
        (correct indentation is important in Python; the "``try:``" should start with 8 leading spaces)

        .. code:: python

          try:
              urlconf = settings.ROOT_URLCONF
          except AttributeError:
              urlconf = None
          default_urlresolver = get_resolver(urlconf)

      - Save the file

After updating the ``collectstatic_js_reverse.py`` file, perform the following 2 steps:
    - Open a command prompt and navigate to the openrem directory, e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Type ``python manage.py collectstatic_js_reverse``

    ..  Note::
      Take care the resulting reverse.py is written to the correct static directory.
      If that is not the case copy the file manually to the correct location.
