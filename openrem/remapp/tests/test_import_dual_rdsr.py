# This Python file uses the following encoding: utf-8
# test_import_dual_rdsr.py

import os
from django.test import TestCase
from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, UniqueEquipmentNames, SkinDoseMapCalcSettings


class ImportDualRDSRs(TestCase):
    """Tests for importing DX and RF RDSR for a system set as 'Dual'

    """

    def test_dual_imports_after_dual_setting(self):
        """Test for following scenario:

        #. DX imported from new modality
        #. Administrator sets modality type to Dual
        #. RF imported from same modality
        #. Test to see if RF is imported as RF
        #. Modality is reprocessed as Dual again
        #. Check modality types still correct

        :return: None
        """

        PatientIDSettings.objects.create()
        SkinDoseMapCalcSettings.objects.create()  # Bitbucket pipeline requires in order to import reset_dual


        rf_file = "test_files/Dual-RDSR-RF.dcm"
        dx_file = "test_files/Dual-RDSR-DX.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        rf_path = os.path.join(root_tests, rf_file)
        dx_path = os.path.join(root_tests, dx_file)

        rdsr(dx_path)
        dx_study = GeneralStudyModuleAttr.objects.order_by('id')[0]
        unique_equip = UniqueEquipmentNames.objects.order_by('id')[0]

        self.assertEqual(dx_study.modality_type, u"DX")

        unique_equip.user_defined_modality = 'dual'
        unique_equip.save()

        from remapp.views import reset_dual
        reset_dual(unique_equip.pk)

        rdsr(rf_path)
        rf_study = GeneralStudyModuleAttr.objects.order_by('id')[1]
        # Make sure second study has fallen into same equipment entry
        self.assertEqual(UniqueEquipmentNames.objects.count(), 1)
        # Should have the correct modality type
        self.assertEqual(rf_study.modality_type, u"RF")
        self.assertEqual(dx_study.modality_type, u"DX")

        reset_dual(unique_equip.pk)

        # After reset, all existing studies are correct.
        dx_study = GeneralStudyModuleAttr.objects.order_by('id')[0]
        rf_study = GeneralStudyModuleAttr.objects.order_by('id')[1]
        self.assertEqual(rf_study.modality_type, u"RF")
        self.assertEqual(dx_study.modality_type, u"DX")

    def test_dual_imports_before_dual_setting(self):
        """Test for following scenario:

        #. DX imported from new modality
        #. RF imported from same modality
        #. Test to see if modality types are both correct
        #. Administrator sets modality type to Dual
        #. Check modality types still correct

        :return: None
        """

        PatientIDSettings.objects.create()
        SkinDoseMapCalcSettings.objects.create()  # Bitbucket pipeline requires in order to import reset_dual

        rf_file = "test_files/Dual-RDSR-RF.dcm"
        dx_file = "test_files/Dual-RDSR-DX.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        rf_path = os.path.join(root_tests, rf_file)
        dx_path = os.path.join(root_tests, dx_file)

        rdsr(dx_path)
        rdsr(rf_path)
        dx_study = GeneralStudyModuleAttr.objects.order_by('id')[0]
        rf_study = GeneralStudyModuleAttr.objects.order_by('id')[1]
        # Make sure second study has fallen into same equipment entry
        self.assertEqual(UniqueEquipmentNames.objects.count(), 1)
        unique_equip = UniqueEquipmentNames.objects.order_by('id')[0]

        self.assertEqual(rf_study.modality_type, u"RF")
        self.assertEqual(dx_study.modality_type, u"DX")

        unique_equip.user_defined_modality = 'dual'
        unique_equip.save()

        from remapp.views import reset_dual
        reset_dual(unique_equip.pk)
        reset_dual(unique_equip.pk)

        # After reset, all existing studies are correct.
        dx_study = GeneralStudyModuleAttr.objects.order_by('id')[0]
        rf_study = GeneralStudyModuleAttr.objects.order_by('id')[1]
        self.assertEqual(rf_study.modality_type, u"RF")
        self.assertEqual(dx_study.modality_type, u"DX")


