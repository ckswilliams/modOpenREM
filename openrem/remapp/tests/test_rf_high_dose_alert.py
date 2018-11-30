# This Python file uses the following encoding: utf-8
# test_rf_high_dose_alert.py

import os
from django.contrib.auth.models import User, Group
from django.test import RequestFactory, TestCase
from remapp.extractors import rdsr
from remapp.models import PatientIDSettings, GeneralStudyModuleAttr, HighDoseMetricAlertSettings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from remapp.interface.mod_filters import RFSummaryListFilter
from decimal import Decimal


class RFHighDoseAlert(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='temporary', email='temporary@…', password='temporary')
        vg = Group(name="admingroup")
        vg.save()
        vg.user_set.add(self.user)
        vg.save()

        pid = PatientIDSettings.objects.create()
        pid.name_stored = True
        pid.name_hashed = True
        pid.id_stored = True
        pid.id_hashed = True
        pid.dob_stored = True
        pid.save()

        try:
            HighDoseMetricAlertSettings.objects.get()
        except ObjectDoesNotExist:
            HighDoseMetricAlertSettings.objects.create()

        alert_settings = HighDoseMetricAlertSettings.objects.all()[0]
        alert_settings.accum_dose_delta_weeks = 2
        alert_settings.calc_accum_dose_over_delta_weeks_on_import = True
        alert_settings.save()

        rf_siemens_zee_20160512 = os.path.join("test_files", "RF-RDSR-Siemens-Zee.dcm")
        rf_siemens_zee_20160510 = os.path.join("test_files", "RF-RDSR-Siemens-Zee_adjusted.dcm")
        # The second file has had the study date adjusted by two days, and the Study UID adjusted by a single digit

        root_tests = os.path.dirname(os.path.abspath(__file__))
        # Important to read in the earlist study date RDSR first because
        # the cumulated DAP and RP dose looks for matching studies that have
        # previously taken place.
        rdsr(os.path.join(root_tests, rf_siemens_zee_20160510))
        rdsr(os.path.join(root_tests, rf_siemens_zee_20160512))

        self.dap_16_text = u'<strong style="color: red;">16.0</strong>'
        self.dap_32_text = u'<strong style="color: red;">32.0</strong>'
        self.rp_252_text = u'<strong style="color: red;">0.00252 </strong>'
        self.rp_504_text = u'<strong style="color: red;">0.00504 </strong>'
        self.rp_000_text = u'<strong style="color: red;">0.0</strong>'
        self.one_exam_text = u'(1 exam)'
        self.two_exams_text = u'(2 exams)'

    def test_cumulative_dap(self):
        """ Test that the calculated cumulative DAP over delta weeks is correct for the two studies
        """
        self.client.login(username='temporary', password='temporary')
        filter_set = ''
        f = RFSummaryListFilter(filter_set, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').order_by().distinct())

        # Test that cumulative DAP matches what I expect below
        # Using AlmostEqual as comparing floating point numbers
        total_dap_over_week_delta = f.qs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total_over_delta_weeks', flat=True)[0]
        expected_value = Decimal(0.0000320)
        self.assertAlmostEqual(total_dap_over_week_delta, expected_value, places=7, msg=None)

        total_dap_over_week_delta = f.qs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total_over_delta_weeks', flat=True)[1]
        expected_value = Decimal(0.0000160)
        self.assertAlmostEqual(total_dap_over_week_delta, expected_value, places=7, msg=None)

    def test_cumulative_rp_dose(self):
        """ Test that calculated cumulative total dose at RP over delta weeks is correct
        """
        self.client.login(username='temporary', password='temporary')
        filter_set = ''
        f = RFSummaryListFilter(filter_set, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').order_by().distinct())

        # Test that cumulative DAP matches what I expect below
        # Using AlmostEqual as comparing floating point numbers
        total_rp_dose_over_week_delta = f.qs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total_over_delta_weeks', flat=True)[0]
        expected_value = Decimal(0.0050400)
        self.assertAlmostEqual(total_rp_dose_over_week_delta, expected_value, places=7, msg=None)

        total_rp_dose_over_week_delta = f.qs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total_over_delta_weeks', flat=True)[1]
        expected_value = Decimal(0.0025200)
        self.assertAlmostEqual(total_rp_dose_over_week_delta, expected_value, places=7, msg=None)

    def test_dap_alert(self):
        """Test that DAP alert highlights the value in red appropriately in the RF summary view
        The test uses two different alert levels
        """
        self.client.login(username='temporary', password='temporary')

        # First DAP alert level tests
        # Second study should alert on cumulative DAP
        alert_settings = HighDoseMetricAlertSettings.objects.all()[0]
        alert_settings.alert_total_dap_rf = 30.0
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_summary_list_filter'), follow=True)

        # One study should be highlighted
        self.assertContains(response, self.dap_32_text, count=1)

        # The other should not
        self.assertNotContains(response, self.dap_16_text)

        # The string (2 exams) should appear twice for the more recent study (once in the DAP field, once in the RP field)
        self.assertContains(response, self.two_exams_text, count=2)

        # The string (1 exam) should appear twice for the earlier study (once in the DAP field, once in the RP field)
        self.assertContains(response, self.one_exam_text, count=2)

        # Second DAP alert level tests
        # Both studies should alert on total DAP; second should alert on cumulated DAP
        alert_settings.alert_total_dap_rf = 15.0
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_summary_list_filter'), follow=True)

        # The latest study should have cumulative DAP highlighted
        self.assertContains(response, self.dap_32_text, count=1)

        # The latest study should have 16.0 cGy.cm^2 total DAP highlighted, and the earlier study should have
        # 16.0 cGy.cm^2 total DAP and cumulative DAP highlighted
        self.assertContains(response, self.dap_16_text, count=3)

    def test_rp_dose_alert(self):
        """Test that dose at RP alert highlights the value in red appropriately in the RF summary view
        The test uses two different alert levels
        """
        self.client.login(username='temporary', password='temporary')

        # First dose at RP test
        # Second study should alert on RP dose
        alert_settings = HighDoseMetricAlertSettings.objects.all()[0]
        alert_settings.alert_total_rp_dose_rf = 0.0050
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_summary_list_filter'), follow=True)

        # Cumulative RP dose should be highlighted for the latest study
        self.assertContains(response, self.rp_504_text, count=1)

        # Cumulative RP dose should not be highlighted for the earlier study, and nor should the total dose at RP
        self.assertNotContains(response, self.rp_252_text)

        # Second dose at RP test
        # Both studies should alert on RP dose ; second should alert on cumulated RP dose
        alert_settings.alert_total_rp_dose_rf = 0.0025
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_summary_list_filter'), follow=True)

        # Cumulative RP dose should be highlighted for the latest study
        self.assertContains(response, self.rp_504_text, count=1)

        # The latest study should have total RP dose highlighted, and the earlier study should have
        # total RP dose and cumulative RP dose highlighted
        self.assertContains(response, self.rp_252_text, count=3)

    def test_detail_view_alerts(self):
        """Test that DAP and RP dose alert highlights the value in red appropriately in the RF detail view
        The test uses two different alert levels
        """
        self.client.login(username='temporary', password='temporary')

        # First DAP and RP dose alert level tests
        # Second study should alert on cumulative DAP
        alert_settings = HighDoseMetricAlertSettings.objects.all()[0]
        alert_settings.alert_total_dap_rf = 30.0
        alert_settings.alert_total_rp_dose_rf = 0.0050
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter for the newest study - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_detail_view', kwargs={'pk': 2}), follow=True)

        # Cumulative DAP should be highlighted for the most recent study
        self.assertContains(response, self.dap_32_text, count=1)

        # Cumulative RP dose should be highlighted for the latest study
        self.assertContains(response, self.rp_504_text, count=1)

        # Obtain the response from the RF summary list filter for the older study - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_detail_view', kwargs={'pk': 1}), follow=True)

        # Cumulative DAP should not be highlighted for the older study
        self.assertNotContains(response, self.dap_16_text)

        # Cumulative RP dose should not be highlighted for the earlier study
        self.assertNotContains(response, self.rp_252_text)

        # Second DAP and RP dose alert level tests
        # Second study should alert on cumulative DAP
        alert_settings = HighDoseMetricAlertSettings.objects.all()[0]
        alert_settings.alert_total_dap_rf = 15.0
        alert_settings.alert_total_rp_dose_rf = 0.0025
        alert_settings.show_accum_dose_over_delta_weeks = True
        alert_settings.save()

        # Recalculate the cumulative dose data because DAP alert changed
        self.client.get(reverse_lazy('rf_recalculate_accum_doses'), follow=True)

        # Obtain the response from the RF summary list filter for the newest study - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_detail_view', kwargs={'pk': 2}), follow=True)

        # Cumulative DAP should be highlighted for the most recent study
        self.assertContains(response, self.dap_32_text, count=1)

        # Cumulative RP dose should be highlighted for the latest study
        self.assertContains(response, self.rp_504_text, count=1)

        # Total DAP should be highlighted for the most recent study, and twice in the summary of studies in past two weeks
        self.assertContains(response, self.dap_16_text, count=3)

        # Total dose at RP dose should be highlighted for the latest study, and twice in the summary of studies in past two weeks
        # The two entries in the summary table are rounded
        self.assertContains(response, self.rp_252_text, count=1)
        self.assertContains(response, self.rp_000_text, count=2)

        # Obtain the response from the RF summary list filter for the older study - this includes the html of the page
        response = self.client.get(reverse_lazy('rf_detail_view', kwargs={'pk': 1}), follow=True)

        # Cumulative DAP should be highlighted for the older study, together with total DAP and total DAP in summary over past two weeks
        self.assertContains(response, self.dap_16_text, count=3)

        # Cumulative RP dose should be highlighted for the older study, together with total dose at RP and total dose at RP in summary of past two weeks
        # The two entries in the summary table are rounded
        self.assertContains(response, self.rp_252_text, count=2)
        self.assertContains(response, self.rp_000_text, count=1)
