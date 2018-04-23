**********************
Running the test suite
**********************

Preparation
===========

Install the dependencies and OpenREM
------------------------------------

OpenREM is a Django application, and therefore we use Django's test-execution framework to test OpenREM.

The first thing to do is to create a local copy of the git repository, then install all of OpenREM's dependencies in a
virtualenv.

You will need ``python``, ``pip``, ``git`` and ``virtualenv`` installed - see the links on the :doc:`install-prep` docs
for the latter, but you might try ``pip install virtualenv``.

.. sourcecode:: console

    mkdir openremrepo
    git clone https://bitbucket.org/openrem/openrem.git openremrepo

Now create the virtualenv:

.. sourcecode:: console

    mkdir veOpenREM
    virtualenv veOpenREM
    . veOpenREM/bin/activate  # Linux
    veOpenREM\Scripts\activate  # Windows

At this stage there should be a ``(veOpenREM)`` prefix to our prompt telling us the virtualenv is activated.

Now install the dependencies:

.. sourcecode:: console

    pip install -e openremrepo/
    pip install https://bitbucket.org/edmcdonagh/pynetdicom/get/default.tar.gz#egg=pynetdicom-0.8.2b2

In the future it might be necessary to install numpy too for testing.

Configure OpenREM
-----------------

Rename and configure ``openremproject/local_settings.py.example`` and ``openremproject/wsgi.py.example`` as per the
:doc:`install` docs.

Create a database following the same :doc:`install` instructions.

Run the tests!
==============

Making sure the virtualenv is activated, move to ``openremrepo/openrem`` and run:

.. sourcecode:: console

    python manage.py test remapp

All the tests that exit in ``openrem/remapp/tests/`` will now be run.


Related tools
=============

Enabling django-debug-toolbar
-----------------------------

Add the following line to ``local_settings.py``:

.. sourcecode:: console

    INTERNAL_IPS= ['127.0.0.1']

If you wish to make use of the debug toolbar on machines other than the one the code is running on, change the
INTERNAL_IPS address list to include your client machine.

Now when ``DEBUG = True`` the toolbar should appear.

Creating test versions of production systems
============================================

If you wish to create a duplicate install to test upgrades etc, refer to :ref:`restore-psql-linux` and the preceding
text regarding making backups.