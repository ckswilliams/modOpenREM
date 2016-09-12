# This Python file uses the following encoding: utf-8
# test_get_values.py

from __future__ import unicode_literals
from django.test import TestCase
from dicom.sequence import Sequence
from dicom.dataset import Dataset
from remapp.extractors.dx import _xray_filters_multiple
from remapp.models import GeneralStudyModuleAttr, ProjectionXRayRadiationDose, IrradEventXRayData, \
    IrradEventXRaySourceData

class DXImportTests(TestCase):
    def test_multiple_filter_kodak_dr7500(self):
        """
        Test the material extraction process when the materials are comma separated
        """
        ds = Dataset()
        FilterMaterial = "niobium,europium"
        ds.FilterThicknessMinimum = "1.0\\0.1"
        ds.FilterThicknessMaximum = "1.0\\0.1"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_multiple(FilterMaterial, ds.FilterThicknessMaximum, ds.FilterThicknessMinimum, source)

        self.assertEqual(source.xrayfilters_set.all().count(), 2)
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
                         "Niobium or Niobium compound")
        self.assertEqual(source.xrayfilters_set.all()[1].xray_filter_material.code_meaning,
                         "Europium or Europium compound")


    def test_multiple_filter_kodak_drxevolution(self):
        """
        Test the material extraction process when the materials are in a MultiValue format
        """
        ds = Dataset()
        ds.FilterMaterial = "aluminum\\copper"
        ds.FilterThicknessMinimum = "1.0\\0.1"
        ds.FilterThicknessMaximum = "1.0\\0.1"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_multiple(ds.FilterMaterial, ds.FilterThicknessMaximum, ds.FilterThicknessMinimum, source)

        self.assertEqual(source.xrayfilters_set.all().count(), 2, 'Wrong number of filters recorded')
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
                         "Aluminum or Aluminum compound")
        self.assertEqual(source.xrayfilters_set.all()[1].xray_filter_material.code_meaning,
                         "Copper or Copper compound")


    def test_single_filter(self):
        """
        Test the material extraction process when there is just one filter
        """
        ds = Dataset()
        FilterMaterial = "lead"
        ds.FilterThicknessMinimum = "1.0"
        ds.FilterThicknessMaximum = "1.0"

        g = GeneralStudyModuleAttr.objects.create()
        g.save()
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
        proj.save()
        event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
        event.save()
        source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
        source.save()

        _xray_filters_multiple(FilterMaterial, ds.FilterThicknessMaximum, ds.FilterThicknessMinimum, source)

        self.assertEqual(source.xrayfilters_set.all().count(), 1)
        self.assertEqual(source.xrayfilters_set.all()[0].xray_filter_material.code_meaning,
                         "Lead or Lead compound")
