# This Python file uses the following encoding: utf-8
# test_filters_mammo.py

import os
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from remapp.extractors import mam, rdsr
from remapp.models import PatientIDSettings


class FilterViewTests(TestCase):
    """
    Class to test the filter views for mammography
    """
    def setUp(self):
        """
        Load in all the mammo objects so that there is something to filter!
        """
        PatientIDSettings.objects.create()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        mam1 = "test_files/MG-Im-Hologic-PropProj.dcm"
        mam2 = "test_files/MG-Im-GE-SenDS-scaled.dcm"
        mam3 = "test_files/MG-RDSR-Hologic_2D.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        path_mam1 = os.path.join(root_tests, mam1)
        path_mam2 = os.path.join(root_tests, mam2)
        path_mam3 = os.path.join(root_tests, mam3)

        mam(path_mam1)
        mam(path_mam2)
        rdsr(path_mam3)

    def test_list_all_mammo(self):
        """
        Initial test to ensure three studies are listed with no filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('mg_summary_list_filter'), follow=True)
        self.assertEqual(response.status_code, 200)
        three_responses_text = u'There are 3 studies in this list.'
        self.assertContains(response, three_responses_text)

    def test_filter_study_desc(self):
        """
        Apply study description filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('mg_summary_list_filter') + '?study_description=bilateral', follow=True)
        self.assertEqual(response.status_code, 200)
        one_responses_text = u'There are 1 studies in this list.'
        self.assertContains(response, one_responses_text)
        accession_number = u'AJSKDL1234'  # Accession number of study with matching study description
        self.assertContains(response, accession_number)

    def test_filter_procedure(self):
        """
        Apply procedure filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('mg_summary_list_filter') + '?procedure_code_meaning=Flat+field+tomo', follow=True)
        self.assertEqual(response.status_code, 200)
        one_responses_text = u'There are 1 studies in this list.'
        self.assertContains(response, one_responses_text)
        accession_number = u'90002314523'  # Accession number of study with matching procedure code
        self.assertContains(response, accession_number)

    def test_filter_acquisition_protocol(self):
        """
        Apply acquisition protocol filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('http://test/openrem/mg/?acquisition_protocol=routine', follow=True)
        self.assertEqual(response.status_code, 200)
        one_responses_text = u'There are 1 studies in this list.'
        self.assertContains(response, one_responses_text)
        accession_number = u'AAAA9876'  # Accession number of study with matching acquisition protocol
        self.assertContains(response, accession_number)
