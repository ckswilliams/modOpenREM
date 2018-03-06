***********************************
Running OpenREM on Windows with IIS
***********************************

These instructions are for running OpenREM under IIS on Windows Server 2012, but should work on Windows 7/8/10 and
later versions of Windows Server with minimal modification.
The instructions are based on http://blog.mattwoodward.com/2016/07/running-django-application-on-windows.html

Why using IIS
=============
The built-in Django webserver is not advised for production environments. There are a few alternatives for serving
a Django application. Apache is probably the best known web server, but  has some requirements under Windows in
combination with Python / Django that are hard to fulfill (see
https://github.com/GrahamDumpleton/mod_wsgi/blob/develop/win32/README.rst). IIS is default available on Windows Server
and doesn't have these requirements.


Prerequisites
=============

+ A working OpenREM installation, that serves web pages using the built-in web server.
    You can test this using the instructions in :doc:`startservices`

Steps to perform
================

Install wfastcgy Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - Open a command prompt and navigate to the python\script directory if that directory is not in your path
    - Type ``pip install wfastcgi``
    - Close the command prompt by entering ``exit``

Install IIS
^^^^^^^^^^^

    - Open Control panel
    - Take care the ``view by`` is on small or large icons (not category view)
    - Select Program and Features
    - Select Turn Windows features on or off
    - **Windows Server 2012**

        - Click ``Next``
        - Leave the ``Role-based or feature-based installation`` radio button selected and click ``Next``
        - Leave the current server highlighted and click ``Next``
        - Scroll to the bottom of the list and check ``Web Server (IIS)``
        - In the dialog that appears, leave the ``Include management tools (if applicable)`` checkbox checked and click
          ``Add Features``
        - On the ``Select server roles`` step, now that ``Web Server (IIS)`` is checked, click ``Next``
        - Leave the defaults and click ``Next``
        - On the ``Web Server Role (IIS)`` step, click ``Next``
        - On the ``Select role services`` step, scroll down to ``Application Development``, expand that section, and check the
          ``CGI`` box. click ``Next``.
        - Click ``Install`` and after installation, click ``Close``

    - **Windows 10**

        - ``Internet information services``
        - Ticked (black square) ``Web Management Tools``, ``World Wide Web Services``
        - In ``World Wide Web Services``, ``Application Development Features``, tick ``CGI``
        - ``OK``
        - ``Close``

    - Close the Server Manager and the Control Panel

    To test the IIS installation browse to http://localhost. You should see the default IIS "Welcome" Page.

Configure IIS
^^^^^^^^^^^^^

    - Open Administrative Tools and double-click the Internet Information Services (IIS) Manager link. You may need to
      right click and ``Run as Adminstrator``.
    - Click on the name of the server within the IIS manager
    - Click No if a pop-up about the Web Platform Components appears
    - Double-click on the ``FastCGI Settings`` icon
    - In the right pane under ``actions`` click ``Add Application...``
    - In the ``Full Path`` box type the path to the Python executable, e.g.: ``c:\python27\python.exe``
    - In the ``Arguments`` box type the path to wfastcgi.py file, e.g.: ``c:\python27\Lib\site-packages\wfastcgi.py``.

    ..  Note::

      If your path contains spaces be sure to have double quotes(``"``) around the argument

    - Under ``FastCGI properties``, click on ``(Collection)`` next to ``Environment Variables`` and click on the grey
      ``...`` box
    - In the EnvironmentVariables Collection Editor dialog, click ``Add``
    - Under ``Name properties`` on the right, click the input box to the right of ``Name,`` and replace the text
      ``Name`` by ``DJANGO_SETTINGS_MODULE`` (capitals is important)
    - As ``Value`` enter ``openremproject.settings``
    - Click Add again and add a variable with name ``PYTHON_PATH`` and value the path to the openrem path,
      e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Click Add for the third time and a variable with name ``WSGI_HANDLER`` and value
      ``django.core.wsgi.get_wsgi_application()``
    - Click twice ``Ok`` to close the ``EnviromentVariables Collection Editor`` and the ``Add FastCGI Application dialog``
    - Start Windows Explorer and browse to the openrem directory, e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Right click on the folder and choose properties. In the security tab, make sure ``SYSTEM`` (local system) has
      ``Full control`` for this directory and the subdirectories.
    - The same applies for the ``MEDIA_ROOT`` (as configured in ``local_settings.py``; default ``c:/Temp/OpenREM/media``)


Create a new website
^^^^^^^^^^^^^^^^^^^^

    - In the IIS manager under connections expand the three under server name
    - Right-click on sites and click ``Add Website...``
    - Enter as sitename ``OpenREM``
    - As physical path enter the same path as the ``PYTHON_PATH`` in the ``FastCGI`` settings above,
      e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Set the port to the port you desire. If you wish to use the default port 80, you need to stop and/or remove  the
      default website or change the port of the default website
    - Click ``OK`` (Windows 10 only?)

Configure the new website
^^^^^^^^^^^^^^^^^^^^^^^^^

    - In IIS manager **double** click on the OpenREM website under Sites
    - Double click on the ``Handler Mappings`` icon in the middle pane
    - In the right pane, under ``Actions``, click ``Add Module Mappings`` or ``Add Module Mapping..``
    - In the ``Request Path`` box enter an asterix (``*``)
    - In the ``Module`` box select ``FastCgiModule`` (not the CgiModule)
    - In the ``Executable`` box enter ``path\to\python.exe|path\to\wfastcgi.py``,
      e.g.: ``c:\python27\python.exe|c:\python27\Lib\site-packages\wfastcgi.py``. The ``|`` character between the two
      paths is usually to be found with ``Shift`` ``\``.
    - In ``Name`` type ``OpenREM cgi handler`` (value of name is not important)

    ..  Note::

      If one of your paths contains a space use quotations marks around that path.
      Don't use quotations marks around the full statement.

    - Click the ``Request Restrictions`` button and uncheck the ``Invoke handler only if request is mapped to:`` checkbox
    - Click ``Ok`` twice to close the Request Restrictions dialog and the Add Module Mapping dialog
    - When prompted ``Do you want to create a FastCGI application for this executable?`` click ``No``

    The website should work now: browse to http://localhost:port (port is the number you configured the website on.
    If the port is 80, you can omit the colon and port number).

    ..  Note::
      The website will look "ugly" as the static files (like the css-files) are not yet configured

Configure Django and IIS to serve static files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - Create a directory called ``static`` in your openrem directory,
      e.g. ``C:\Python27\Lib\site-packages\openrem\static``
    - In the Openrem local settingsfile, located in the openremproject directory
      (e.g. ``C:\Python27\Lib\site-packages\openrem\oprenremproject\local_settings.py``) find the ``STATIC_ROOT`` variable
      and set the value to match the directory you just created. The backslashes should be replaced by forward slashed.
      e.g. ``STATIC_ROOT = 'C:/Python27/Lib/site-packages/openrem/static'``
    - Open a command prompt and navigate to the openrem directory, e.g. ``C:\Python27\Lib\site-packages\openrem``
    - Type ``python manage.py collectstatic``
    - Type ``Yes`` to confirm if the static root directory mentioned is correct
    - Close the command prompt by typing ``exit``
    - In IIS right-click on the OpenREM website (under Sites)
    - Click ``Add Virtual Directory``
    - Type ``static`` as alias and the path to the static directoy as ``Physical Path``,
      e.g. ``C:\Python27\Lib\site-packages\openrem\static``
    - Click ``Ok`` to close the dialog box
    - Click on the ``static`` directory in IIS within the OpenREM site (unfold the OpenREM site)
    - Double click on the ``Handler Mappings`` icon in the middle pane
    - On the right pane click ``View Ordered Lists...`` under Actions
    - Click on the ``StaticFile Handler`` in the middle pane and on ``Move Up`` in the right pane until the
      ``StaticFile Handler`` is on the top

    ..  Note::

        You may get a warning that you are detaching the virtual directory. Click ``Yes`` on this warning.

    Check the website by browsing to http://localhost:port, everything should be fine now.