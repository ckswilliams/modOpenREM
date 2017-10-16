# This Python file uses the following encoding: utf-8
# test_filters_mammo.py

import os
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from remapp.extractors import mam, rdsr
from remapp.models import PatientIDSettings



class FilterViewTests(TestCase):
    """
    Class to test the filter views for mammography
    """
    def setUp(self):
        """
        Load in all the mammo objects so there is something to filter!
        """
        PatientIDSettings.objects.create()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

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
        response = self.client.get(reverse('mg_summary_list_filter'), follow=True)
        self.assertEqual(response.status_code, 200)
        three_responses_text = 'There are 3 studies in this list.'
        self.assertContains(response, three_responses_text)
