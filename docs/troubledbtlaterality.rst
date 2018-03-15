*****************************************************
Fixing accumulated AGD and laterality for Hologic DBT
*****************************************************

The code for extracting dose related information from Hologic digital breast tomosynthesis proprietary projection
images object used an incorrect tag to extract the laterality of the image. As a result the accumulated AGD code didn't
work, so the accumulated AGD cell on the mammography summary sheets remained blank.

The code below allows the laterality to be derived automatically from the acquisition protocol name, if the protocol
name has ``R`` or ``L`` as the first letter. When this information is derived, the accumulated AGD is also calculated
per breast.

How to use the code
===================

Create a new file in your Python OpenREM folder which we will add the code to. For example it could be called
``fix_dbt_laterality.py``:

* Ubuntu linux: ``/usr/local/lib/python2.7/dist-packages/openrem/fix_dbt_laterality.py``
* Other linux: ``/usr/lib/python2.7/site-packages/openrem/fix_dbt_laterality.py``
* Linux virtualenv: ``lib/python2.7/site-packages/openrem/fix_dbt_laterality.py``
* Windows: ``C:\Python27\Lib\site-packages\openrem\fix_dbt_laterality.py``
* Windows virtualenv: ``Lib\site-packages\openrem\fix_dbt_laterality.py``

Copy and paste the code from below. You will need to edit the ``DISPLAY_NAME`` tp match the Display name you have
configured for the Hologic DBT system that needs to be modified.

If you are working on Linux, you may like to look at the brief tips on using ``nano`` on the NGINX
:ref:`troubleshooting` section.

.. sourcecode:: python

    # -*- coding: utf-8 -*-
    # Routine to fix missing laterality details for exposures extracted from Hologic DBT proprietary projection data objects
    # Also retrospectively updates the accumulated average glandular dose fields that were previously missing due to lack
    # of laterality.
    #
    # Contains hard coded DISPLAY_NAME that must be changed appropriately to identify the Hologic DBT system in your
    # database.
    # See https://bitbucket.org/openrem/openrem/issues/411

    import os
    import sys
    import django
    import logging
    from django.core.exceptions import ObjectDoesNotExist

    logger = logging.getLogger(__name__)

    # setup django/OpenREM
    basepath = os.path.dirname(__file__)
    projectpath = os.path.abspath(os.path.join(basepath, ))
    if projectpath not in sys.path:
        sys.path.insert(1, projectpath)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openremproject.settings')
    django.setup()

    from remapp.models import IrradEventXRayData
    from remapp.tools.get_values import get_or_create_cid

    DISPLAY_NAME = "Display name of my Hologic"


    def _accumulatedxraydose(proj):
        """
        Borrowed from mam.py
        Creates an AccumXRayDose table entry
        :param proj: Projection x-ray radiation dose database entry
        :return: Nothing
        """
        from remapp.models import AccumXRayDose, AccumMammographyXRayDose
        from remapp.tools.get_values import get_or_create_cid
        accum = AccumXRayDose.objects.create(projection_xray_radiation_dose=proj)
        accum.acquisition_plane = get_or_create_cid('113622', 'Single Plane')
        accum.save()
        accummam = AccumMammographyXRayDose.objects.create(accumulated_xray_dose=accum)
        accummam.accumulated_average_glandular_dose = 0.0
        accummam.save()


    def _accumulatedmammo_update(event):  # TID 10005
        """
        Borrowed from mam.py
        Updates the accumulated average glandular dose tables on a per-breast basis
        :param event: Irradiation event database entry
        :return: Nothing
        """
        from remapp.tools.get_values import get_or_create_cid
        from remapp.models import AccumMammographyXRayDose
        try:
            accum = event.projection_xray_radiation_dose.accumxraydose_set.get()
        except ObjectDoesNotExist:
            print("No accumxraydose for event occurring at {0} in study no {1}".format(event.date_time_started,
                event.projection_xray_radiation_dose.general_study_module_attributes.id))
            _accumulatedxraydose(event.projection_xray_radiation_dose)
            accum = event.projection_xray_radiation_dose.accumxraydose_set.get()
        accummams = accum.accummammographyxraydose_set.all()
        event_added = False
        for accummam in accummams:
            if not accummam.laterality:
                if event.laterality.code_meaning == 'Right':
                    accummam.laterality = get_or_create_cid('T-04020', 'Right breast')
                elif event.laterality.code_meaning == 'Left':
                    accummam.laterality = get_or_create_cid('T-04030', 'Left breast')
                accummam.accumulated_average_glandular_dose += event.irradeventxraysourcedata_set.get(
                    ).average_glandular_dose
                accummam.save()
                event_added = True
            elif event.laterality.code_meaning in accummam.laterality.code_meaning:
                accummam.accumulated_average_glandular_dose += event.irradeventxraysourcedata_set.get(
                    ).average_glandular_dose
                accummam.save()
                event_added = True
        if not event_added:
            accummam = AccumMammographyXRayDose.objects.create(accumulated_xray_dose=accum)
            if event.laterality.code_meaning == 'Right':
                accummam.laterality = get_or_create_cid('T-04020', 'Right breast')
            elif event.laterality.code_meaning == 'Left':
                accummam.laterality = get_or_create_cid('T-04030', 'Left breast')
            accummam.accumulated_average_glandular_dose = event.irradeventxraysourcedata_set.get().average_glandular_dose
            accummam.save()
        accummam.save()


    events = IrradEventXRayData.objects.filter(
        projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name__display_name__exact=DISPLAY_NAME)

    events_r = events.filter(laterality__code_meaning__exact=u"Right")
    events_l = events.filter(laterality__code_meaning__exact=u"Left")
    events_n = events.filter(laterality__isnull=True)
    print(u"Total events is {0}, of which {1} are Right, {2} are Left and {3} are null (remainder {4})".format(
        events.count(), events_r.count(), events_l.count(), events_n.count(),
        events.count() - events_r.count() - events_l.count() - events_n.count()))

    for event in events_n:
        if event.acquisition_protocol[0] == u'R':
            event.laterality = get_or_create_cid('G-A100', 'Right')
            event.save()
            _accumulatedmammo_update(event)
        elif event.acquisition_protocol[0] == u'L':
            event.laterality = get_or_create_cid('G-A101', 'Left')
            event.save()
            _accumulatedmammo_update(event)
        else:
            print("Event acquisition protocol is {0} so we couldn't assign it left or right. Exam ID is {1}".format(
                event.acquisition_protocol, event.projection_xray_radiation_dose.general_study_module_attributes.id))

    events_r = events.filter(laterality__code_meaning__exact=u"Right")
    events_l = events.filter(laterality__code_meaning__exact=u"Left")
    events_n = events.filter(laterality__isnull=True)
    print(u"Post update, total events is {0}, of which {1} are Right, {2} are Left and {3} are null (remainder {4})".format(
        events.count(), events_r.count(), events_l.count(), events_n.count(),
        events.count() - events_r.count() - events_l.count() - events_n.count()))

Run the fix
===========

In a shell/command window, activate your virtualenv if you are using one, and change directory to the openrem folder:

* Ubuntu linux: ``cd /usr/local/lib/python2.7/dist-packages/openrem/``
* Other linux: ``cd /usr/lib/python2.7/site-packages/openrem/``
* Linux virtualenv: ``cd lib/python2.7/site-packages/openrem/``
* Windows: ``cd C:\Python27\Lib\site-packages\openrem\``
* Windows virtualenv: ``cd Lib\site-packages\openrem\``

Then:

.. sourcecode:: bash

    python fix_dbt_laterality.py

This should generate the following response, with one message for each event that can't be assigned laterality due to
the acquisition protocol name not starting with ``L`` or ``R``:

.. sourcecode:: bash

    Total events is 1, of which 0 are Right, 0 are Left and 1 are null (remainder 0)
    Event acquisition protocol is Flat Field Tomo so we couldn't assign it left or right. Exam ID is 261384
    Post update, total events is 1, of which 0 are Right, 0 are Left and 1 are null (remainder 0)

The Exam ID referred to is the database ID, so if you look at a mammography exam in the web interface, you can change
the Exam ID in the URL if you want to review that study.