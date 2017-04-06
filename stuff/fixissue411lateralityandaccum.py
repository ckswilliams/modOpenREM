# -*- coding: utf-8 -*-
# Routine to fix missing laterality details for exposures extracted from Hologic DBT proprietary projection data objects
# Also retrospectively updates the accumulated average glandular dose fields that were previously missing due to lack
# of laterality.
#
# Contains hard coded DISPLAY_NAME that must be changed appropriately to identify the Hologic DBT system in your
# database.
# See https://bitbucket.org/openrem/openrem/issues/411

import os
import django
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

# setup django/OpenREM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openremproject.settings')
django.setup()

from remapp.models import IrradEventXRayData
from remapp.tools.get_values import get_or_create_cid

DISPLAY_NAME = "RMH Sutton RDAC 3"


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
