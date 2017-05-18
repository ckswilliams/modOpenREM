# This Python file uses the following encoding: utf-8
# test_import_mam.py

import os
from decimal import Decimal
from django.test import TestCase
from remapp.extractors import mam
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings



class ImportMGImgHologicPropProjection(TestCase):
    def test_import_mg_img_hol_proj(self):
        """
        Imports a known DICOM object derived from a Hologic DBT proprietary projection data object, and tests the values
        imported against those expected. Initial testing is just for issue
        https://bitbucket.org/openrem/openrem/issues/411
        """
        PatientIDSettings.objects.create()

        dicom_file = "test_files/MG-Im-Hologic-PropProj.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        mam(dicom_path)
        study = GeneralStudyModuleAttr.objects.all()[0]

        # Test that laterality is recorded (see https://bitbucket.org/openrem/openrem/issues/411)
        self.assertEqual(study.projectionxrayradiationdose_set.get().irradeventxraydata_set.get(
            ).laterality.code_meaning, u'Right')

        # Test that accumulated AGD is recorded (see issue 411 again)
        self.assertAlmostEqual(study.projectionxrayradiationdose_set.get().accumxraydose_set.get(
            ).accummammographyxraydose_set.all()[0].accumulated_average_glandular_dose, Decimal(0.26))

