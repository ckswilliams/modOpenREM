# This Python file uses the following encoding: utf-8
# test_export_ct_xlsx.py

import hashlib
import os
from django.contrib.auth.models import User, Group
from django.test import TestCase, RequestFactory
from remapp.extractors import rdsr
from remapp.exports.ct_export import ctxlsx
from remapp.models import PatientIDSettings, Exports


class ExportCTxlsx(TestCase):
    """Test class for CT exports to XLSX

    """
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

        ct_ge_ct660 = os.path.join("test_files", "CT-ESR-GE_Optima.dcm")
        ct_ge_vct = os.path.join("test_files", "CT-ESR-GE_VCT.dcm")
        ct_siemens_flash_ss = os.path.join("test_files", "CT-RDSR-Siemens_Flash-TAP-SS.dcm")
        ct_toshiba_dosecheck = os.path.join("test_files", "CT-RDSR-Toshiba_DoseCheck.dcm")
        root_tests = os.path.dirname(os.path.abspath(__file__))

        rdsr(os.path.join(root_tests, ct_ge_ct660))
        rdsr(os.path.join(root_tests, ct_ge_vct))
        rdsr(os.path.join(root_tests, ct_siemens_flash_ss))
        rdsr(os.path.join(root_tests, ct_toshiba_dosecheck))

    def test_id_as_text(self):  # See https://bitbucket.org/openrem/openrem/issues/443
        filter_set = ""
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        import xlrd
        task = Exports.objects.all()[0]

        book = xlrd.open_workbook(task.filename.path)
        all_data_sheet = book.sheet_by_name('All data')
        headers = all_data_sheet.row(0)

        patient_id_col = [i for i, x in enumerate(headers) if x.value == 'Patient ID'][0]
        accession_number_col = [i for i, x in enumerate(headers) if x.value == 'Accession number'][0]
        dlp_total_col = [i for i, x in enumerate(headers) if x.value == 'DLP total (mGy.cm)'][0]
        e1_dose_check_col = [i for i, x in enumerate(headers) if x.value == 'E1 Dose check details'][0]
        e2_dose_check_col = [i for i, x in enumerate(headers) if x.value == 'E2 Dose check details'][0]

        self.assertEqual(all_data_sheet.cell_type(2, patient_id_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(3, patient_id_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(2, accession_number_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(3, accession_number_col), xlrd.XL_CELL_TEXT)
        self.assertEqual(all_data_sheet.cell_type(2, dlp_total_col), xlrd.XL_CELL_NUMBER)

        self.assertEqual(all_data_sheet.cell_value(2, patient_id_col), '008F/g234')
        self.assertEqual(all_data_sheet.cell_value(3, patient_id_col), '00001234')
        self.assertEqual(all_data_sheet.cell_value(2, accession_number_col), '001234512345678')
        self.assertEqual(all_data_sheet.cell_value(3, accession_number_col), '0012345.12345678')
        self.assertEqual(all_data_sheet.cell_value(2, dlp_total_col), 2002.39)

        e1_dose_check_string = u"Dose Check Alerts: DLP alert is configured at 100.00 mGy.cm with an accumulated " \
                               u"forward estimate of 251.20 mGy.cm. CTDIvol alert is configured at 10.00 mGy with no " \
                               u"accumulated forward estimate recorded. Person authorizing irradiation: Luuk. "
        e2_dose_check_string = u"Dose Check Alerts: DLP alert is configured at 100.00 mGy.cm with an accumulated " \
                               u"forward estimate of 502.40 mGy.cm. CTDIvol alert is configured at 10.00 mGy with an " \
                               u"accumulated forward estimate of 10.60 mGy. Person authorizing irradiation: Luuk. "
        self.assertEqual(all_data_sheet.cell_value(1, e1_dose_check_col), e1_dose_check_string)
        self.assertEqual(all_data_sheet.cell_value(1, e2_dose_check_col), e2_dose_check_string)

        # cleanup
        task.filename.delete()  # delete file so local testing doesn't get too messy!
        task.delete()  # not necessary, by hey, why not?

    def test_zero_filter(self):
        """Test error handled correctly when empty filter.

        """
        filter_set = {"study_description": "asd"}
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        task = Exports.objects.all()[0]
        self.assertEqual(u"ERROR", task.status)

    def test_acq_type_filter_spiral(self):
        """Test to check that filtering CT by acquisition type works
        as expected.

        """
        filter_set = {"ct_acquisition_type": ["Spiral Acquisition"]}
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        task = Exports.objects.all()[0]
        self.assertEqual(4, task.num_records)

    def test_acq_type_filter_sequenced(self):
        """Test to check that filtering CT by acquisition type works
        as expected.

        """
        filter_set = {"ct_acquisition_type": ["Sequenced Acquisition"]}
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        task = Exports.objects.all()[0]
        self.assertEqual(1, task.num_records)

    def test_acq_type_filter_spiral_and_sequenced(self):
        """Test to check that filtering CT by acquisition type works
        as expected.

        """
        filter_set = {"ct_acquisition_type": ["Spiral Acquisition", "Sequenced Acquisition"]}
        pid = True
        name = False
        patient_id = True

        ctxlsx(filter_set, pid=pid, name=name, patid=patient_id, user=self.user)

        task = Exports.objects.all()[0]
        self.assertEqual(4, task.num_records)
