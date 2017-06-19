# This Python file uses the following encoding: utf-8
# test_export_rf_xlsx.py

import hashlib
import os
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import rdsr
from remapp.exports.rf_export import rfxlsx
from remapp.models import PatientIDSettings, Exports


class ExportRFxlsx(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        eg = Group(name="exportgroup")
        eg.save()
        eg.user_set.add(self.user)
        eg.save()

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = False
        pid.id_stored = True
        pid.id_hashed = False
        pid.dob_stored = True
        pid.save()

        rf_siemens_zee = os.path.join("test_files", "RF-RDSR-Siemens-Zee.dcm")
        rf_philips_allura = os.path.join("test_files", "RF-RDSR-Philips_Allura.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        rdsr(os.path.join(root_tests, rf_siemens_zee))
        rdsr(os.path.join(root_tests, rf_philips_allura))

    def test_id_as_text(self):  # See https://bitbucket.org/openrem/openrem/issues/443
        filter_set = ""
        pid = True
        name = False
        patient_id = True

        rfxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        import xlrd
        task = Exports.objects.all()[0]

        book = xlrd.open_workbook(task.filename.path)
        all_data_sheet = book.sheet_by_name('All data')
        headers = all_data_sheet.row(0)

        patient_id_col = [i for i, x in enumerate(headers) if x.value == u'Patient ID'][0]
        accession_number_col = [i for i, x in enumerate(headers) if x.value == u'Accession number'][0]
        a_dose_rp_col = [i for i, x in enumerate(headers) if x.value == u'A Dose RP total (Gy)'][0]

        self.assertEqual(all_data_sheet.cell_type(1, patient_id_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(1, accession_number_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(1, a_dose_rp_col), xlrd.XL_CELL_NUMBER)

        self.assertEqual(all_data_sheet.cell_value(1, patient_id_col), '098765')
        self.assertEqual(all_data_sheet.cell_value(1, accession_number_col), '1234.5678')
        self.assertEqual(all_data_sheet.cell_value(1, a_dose_rp_col), 0.00252)

        # cleanup
        task.filename.delete()  # delete file so local testing doesn't get too messy!
        task.delete()  # not necessary, by hey, why not?

    def test_filters(self):
        '''
        Tests that fluoro studies can be exported to XLSX  with single or multiple filters

        TODO: Add test study with no filter
        '''
        filter_set = ""
        pid = True
        name = False
        patient_id = True

        rfxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        import xlrd
        task = Exports.objects.all()[0]

        book = xlrd.open_workbook(task.filename.path)
        philips_sheet = book.sheet_by_name('abdomen_2fps_25%')
        siemens_sheet = book.sheet_by_name(('fl_-_ang'))
        headers = siemens_sheet.row(0)

        filter_material_col = [i for i, x in enumerate(headers) if x.value == u'Filter material'][0]
        filter_thickness_col = [i for i, x in enumerate(headers) if x.value == u'Mean filter thickness (mm)'][0]

        self.assertEqual(philips_sheet.cell_value(1, filter_material_col), 'Cu | Al')
        self.assertEqual(philips_sheet.cell_value(1, filter_thickness_col), '0.1 | 1.0')
        self.assertEqual(siemens_sheet.cell_value(1, filter_material_col), 'Cu')
        self.assertEqual(siemens_sheet.cell_value(1, filter_thickness_col), '0.6')

        # cleanup
        task.filename.delete()  # delete file so local testing doesn't get too messy!
        task.delete()  # not necessary, by hey, why not?
