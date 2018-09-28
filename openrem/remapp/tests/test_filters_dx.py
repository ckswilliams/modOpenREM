# This Python file uses the following encoding: utf-8
# test_filters_dx.py

import os
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from remapp.extractors import rdsr, dx
from remapp.models import PatientIDSettings


class FilterViewTests(TestCase):
    """
    Class to test the filter views for radiography
    """
    def setUp(self):
        """
        Load in all the dx objects so that there is something to filter!
        """
        PatientIDSettings.objects.create()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        dx1 = "test_files/DX-Im-Carestream_DR7500-1.dcm"
        dx2 = "test_files/DX-Im-Carestream_DR7500-2.dcm"
        dx3 = "test_files/DX-Im-Carestream_DRX.dcm"
        dx4 = "test_files/DX-Im-GE_XR220-1.dcm"
        dx5 = "test_files/DX-Im-GE_XR220-2.dcm"
        dx6 = "test_files/DX-Im-GE_XR220-3.dcm"
        dx7 = "test_files/DX-RDSR-Canon_CXDI.dcm"
        dx8 = "test_files/DX-RDSR-Carestream_DRXEvolution.dcm"
        root_tests = os.path.dirname(os.path.abspath(__file__))
        path_dx1 = os.path.join(root_tests, dx1)
        path_dx2 = os.path.join(root_tests, dx2)
        path_dx3 = os.path.join(root_tests, dx3)
        path_dx4 = os.path.join(root_tests, dx4)
        path_dx5 = os.path.join(root_tests, dx5)
        path_dx6 = os.path.join(root_tests, dx6)
        path_dx7 = os.path.join(root_tests, dx7)
        path_dx8 = os.path.join(root_tests, dx8)

        dx(path_dx1)
        dx(path_dx2)
        dx(path_dx3)
        dx(path_dx4)
        dx(path_dx5)
        dx(path_dx6)
        rdsr(path_dx7)
        rdsr(path_dx8)

    def test_list_all_dx(self):
        """
        Initial test to ensure five studies are listed with no filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('dx_summary_list_filter'), follow=True)
        self.assertEqual(response.status_code, 200)
        responses_text = u'There are 5 studies in this list.'
        self.assertContains(response, responses_text)

    def test_filter_study_desc(self):
        """
        Apply study description filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('dx_summary_list_filter') + '?study_description=CR', follow=True)
        self.assertEqual(response.status_code, 200)
        one_responses_text = u'There are 2 studies in this list.'
        self.assertContains(response, one_responses_text)
        accession_number1 = u'3599305798462538'  # Accession number of study with matching study description
        accession_number2 = u'7698466579781854'  # Accession number of study with matching study description
        self.assertContains(response, accession_number1)
        self.assertContains(response, accession_number2)

    def test_filter_acquisition_protocol(self):
        """
        Apply acquisition protocol filter
        """
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse_lazy('dx_summary_list_filter') + '?acquisition_protocol=thigh', follow=True)
        self.assertEqual(response.status_code, 200)
        one_responses_text = u'There are 1 studies in this list.'
        self.assertContains(response, one_responses_text)
        accession_number = u'7698466579781854'  # Accession number of study with matching acquisition protocol
        self.assertContains(response, accession_number)
