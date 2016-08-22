# test_get_values.py

from django.test import TestCase
from dicom.sequence import Sequence
from dicom.dataset import Dataset
from remapp.tools.get_values import get_seq_code_value, get_seq_code_meaning


from remapp.extractors import rdsr
from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, DicomDeleteSettings



class ImportCTRDSR(TestCase):
    def test_import_ct_rdsr_siemens(self):
        """
        Imports a known RDSR file derived from a Siemens Definition Flash single source RDSR, and tests all the values
        imported against those expected.
        """
        PatientIDSettings.objects.create()

        import os
        dicom_file = "test_files/CT-RDSR-Siemens_Flash-TAP-SS.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        dicom_path = os.path.join(root_tests, dicom_file)

        rdsr(dicom_path)
        a = GeneralStudyModuleAttr.objects.all()
        b = a[0]

        self.assertEqual(b.accession_number, 'ACC12345601')

