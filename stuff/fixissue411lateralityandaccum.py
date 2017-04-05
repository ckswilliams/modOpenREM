# -*- coding: utf-8 -*-
import os
import sys
import django
import logging

logger = logging.getLogger(__name__)

# setup django/OpenREM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openremproject.settings')
django.setup()

from remapp.models import IrradEventXRayData
from remapp.tools.get_values import get_or_create_cid


def _accumulatedmammo_update(event):  # TID 10005
    from remapp.tools.get_values import get_or_create_cid
    from remapp.models import AccumMammographyXRayDose
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
             projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name__display_name__exact = "RMH Sutton RDAC 3")

events_r = events.filter(laterality__code_meaning__exact=u"Right")
events_l = events.filter(laterality__code_meaning__exact=u"Left")
events_n = events.filter(laterality__isnull=True)
print u"Total events is {0}, of which {1} are Right, {2} are Left and {3} are null (remainder {4})".format(
    events.count(), events_r.count(), events_l.count(), events_n.count(),
    events.count() - events_r.count() - events_l.count() - events_n.count())

for event in events_n:
    if event.acquisition_protocol[0] == u'R':
        event.laterality = get_or_create_cid('G-A100', 'Right')
        event.save()
        _accumulatedmammo_update(event)
    elif event.acquisition_protocol[0] == u'L':
        event.laterality = get_or_create_cid('G-A101', 'Left')
        event.save()
        _accumulatedmammo_update(event)

events_r = events.filter(laterality__code_meaning__exact =u"Right")
events_l = events.filter(laterality__code_meaning__exact =u"Left")
events_n = events.filter(laterality__isnull=True)
print u"Post update, total events is {0}, of which {1} are Right, {2} are Left and {3} are null (remainder {4})".format(
    events.count(), events_r.count(), events_l.count(), events_n.count(),
    events.count() - events_r.count() - events_l.count() - events_n.count())
