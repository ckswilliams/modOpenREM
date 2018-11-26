# This Python file uses the following encoding: utf-8
#    OpenREM - Radiation Exposure Monitoring tools for the physicist
#    Copyright (C) 2012,2013  The Royal Marsden NHS Foundation Trust
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    Additional permission under section 7 of GPLv3:
#    You shall not make any use of the name of The Royal Marsden NHS
#    Foundation trust in connection with this Program in any press or
#    other public announcement without the prior written consent of
#    The Royal Marsden NHS Foundation Trust.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
..  module:: send_high_dose_alert_emails.
    :synopsis: Module to send high dose alert e-mails.

..  moduleauthor:: David Platten

"""

import os
import sys
import django

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1,projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()


def send_rf_high_dose_alert_email(study_pk=None, test_message=None, test_user=None):
    """
    Function to send users a fluoroscopy high dose alert e-mail
    """
    from remapp.models import GeneralStudyModuleAttr, HighDoseMetricAlertSettings
    from datetime import timedelta
    from django.contrib.auth.models import User
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from openremproject import settings
    from socket import error as socket_error
    from socket import gaierror as gai_error
    from smtplib import SMTPException
    from ssl import SSLError

    # Send a test message to the e-mail address contained in test_user
    if test_message:
        if test_user:
            try:
                text_msg_content = render_to_string('remapp/email_test_template.txt')
                html_msg_content = render_to_string('remapp/email_test_template.html')
                recipients = [test_user]
                msg_subject = 'OpenREM e-mail test message'
                msg = EmailMultiAlternatives(msg_subject, text_msg_content, settings.EMAIL_DOSE_ALERT_SENDER, recipients)
                msg.attach_alternative(html_msg_content, 'text/html')
                msg.send()
            except (SSLError, SMTPException, ValueError, gai_error, socket_error) as the_error:
                # SSLError raised if SSL unsupported by mail server but configured in local_settings.py
                # SMTPException raised if TLS unsupported by mail server but configured in local_settings.py
                # ValueError raised if the user has set both TLS and SSL security options
                # gai_error raised if the user has misconfigured the mail server hostname
                # socket_error catches various things including connection errors
                return the_error
        return

    if study_pk:
        study = GeneralStudyModuleAttr.objects.get(pk=study_pk)
    else:
        return

    this_study_dap = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
    this_study_rp_dose = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().dose_rp_total
    accum_dap = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().total_dap_delta_gym2_to_cgycm2()
    accum_rp_dose = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().dose_rp_total_over_delta_weeks

    alert_levels = HighDoseMetricAlertSettings.objects.values('show_accum_dose_over_delta_weeks', 'alert_total_dap_rf', 'alert_total_rp_dose_rf', 'accum_dose_delta_weeks')[0]

    if alert_levels['show_accum_dose_over_delta_weeks']:
        patient_id = study.patientmoduleattr_set.values_list('patient_id', flat=True)[0]
        if patient_id:
            study_date = study.study_date
            week_delta = HighDoseMetricAlertSettings.objects.values_list('accum_dose_delta_weeks', flat=True)[0]
            oldest_date = (study_date - timedelta(weeks=week_delta))
            included_studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF', patientmoduleattr__patient_id__exact=patient_id, study_date__range=[oldest_date, study_date])
        else:
            included_studies = None
    else:
        included_studies = None

    if this_study_dap >= alert_levels['alert_total_dap_rf'] or this_study_rp_dose >= alert_levels['alert_total_rp_dose_rf'] or accum_dap >= alert_levels['alert_total_dap_rf'] or accum_rp_dose >= alert_levels['alert_total_rp_dose_rf']:

        projection_xray_dose_set = study.projectionxrayradiationdose_set.get()
        accumxraydose_set_all_planes = projection_xray_dose_set.accumxraydose_set.select_related('acquisition_plane').all()

        content_dict = {
            'study': study,
            'accumxraydose_set_all_planes': accumxraydose_set_all_planes,
            'all_studies': included_studies,
            'week_delta': week_delta,
            'alert_levels': alert_levels,
            'studies_in_week_delta': included_studies,
            'server_url': settings.EMAIL_OPENREM_URL
        }

        text_msg_content = render_to_string('remapp/rf_dose_alert_email_template.txt', content_dict)
        html_msg_content = render_to_string('remapp/rf_dose_alert_email_template.html', content_dict)
        recipients = User.objects.filter(highdosemetricalertrecipients__receive_high_dose_metric_alerts__exact=True).values_list('email', flat=True)
        msg_subject = 'OpenREM high dose alert'
        msg = EmailMultiAlternatives(msg_subject, text_msg_content, settings.EMAIL_DOSE_ALERT_SENDER, recipients)
        msg.attach_alternative(html_msg_content, 'text/html')
        msg.send()
