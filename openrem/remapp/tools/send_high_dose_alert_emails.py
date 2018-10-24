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


def send_rf_high_dose_alert_email(study_pk=None):
    from remapp.models import GeneralStudyModuleAttr, HighDoseMetricAlertSettings
    from datetime import timedelta

    if study_pk:
        study = GeneralStudyModuleAttr.objects.get(pk=study_pk)
    else:
        return

    alert_values = HighDoseMetricAlertSettings.objects.values('alert_total_dap_rf', 'alert_total_rp_dose_rf')[0]
    week_delta = HighDoseMetricAlertSettings.objects.values('accum_dose_delta_weeks')[0]
    this_study_dap = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
    this_study_rp_dose = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().dose_rp_total
    accum_dap = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().total_dap_delta_gym2_to_cgycm2()
    accum_rp_dose = study.projectionxrayradiationdose_set.get().accumxraydose_set.last().accumintegratedprojradiogdose_set.get().dose_rp_total_over_delta_weeks
    patient_id = study.patientmoduleattr_set.values_list('patient_id', flat=True)[0]

    if patient_id:
        study_date = study.study_date
        oldest_date = (study_date - timedelta(weeks=week_delta))
        included_studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF', patientmoduleattr__patient_id__exact=patient_id, study_date__range=[oldest_date, study_date])
    else:
        included_studies = None

    if this_study_dap >= alert_values['alert_total_dap_rf'] or this_study_rp_dose >= alert_values['alert_total_rp_dose_rf'] or accum_dap >= alert_values['alert_total_dap_rf'] or accum_rp_dose >= alert_values['alert_total_rp_dose_rf']:
        msg_body = 'This is an automatically-generated e-mail from OpenREM. Please do not reply to this message.\r\n'
        msg_body += '\r\n'
        msg_body += 'A fluoroscopy study has triggered a high dose alert. See below for details.\r\n'
        msg_body += '\r\n'
        msg_body += 'This study\r\n'
        #msg_body += '\tStudy date:\t{0}\r\n'.format(g.study_date.strftime('%x'))
        #msg_body += '\tStudy time:\t{0}\r\n'.format(g.study_time.strftime('%X'))
        #msg_body += '\tInstitution:\t{0}\r\n'.format(g.generalequipmentmoduleattr_set.get().institution_name)
        #msg_body += '\tDisplay name:\t{0}\r\n'.format(
        #    g.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name)
        #msg_body += '\tAccession number:\t{0}\r\n'.format(g.accession_number)
        #msg_body += '\tOpenREM link:\t{0}\r\n'.format(reverse('rf_detail_view', args=[g.pk]))
        #msg_body += '\r\n'

        html_msg_body = '<p>This is an automatically-generated e-mail from OpenREM. Please do not reply to this message.</p>'
        html_msg_body += '<p>A fluoroscopy study has triggered a high dose alert. See below for details.</p>'
        html_msg_body += '<p>This study</p>'
        html_msg_body += '<table>'
        #html_msg_body += '<tr><td>Study date:</td><td>{0}</td></tr>'.format(g.study_date.strftime('%x'))
        #html_msg_body += '<tr><td>Study time:</td><td>{0}</td></tr>'.format(g.study_time.strftime('%X'))
        #html_msg_body += '<tr><td>Institution:</td><td>{0}</td></tr>'.format(
        #    g.generalequipmentmoduleattr_set.get().institution_name)
        #html_msg_body += '<tr><td>Display name:</td><td>{0}</td></tr>'.format(
        #    g.generalequipmentmoduleattr_set.get().unique_equipment_name.display_name)
        #html_msg_body += '<tr><td>Accession number:</td><td>{0}</td></tr>'.format(g.accession_number)
        #html_msg_body += '<tr><td>OpenREM link:</td><td>{0}</td></tr>'.format(reverse('rf_detail_view', args=[g.pk]))
        #html_msg_body += '</table>'

        msg_body += '\tTotal DAP (cGy.cm2):\t{0:.1f}'.format(this_study_dap)
        html_msg_body += '<table>'
        html_msg_body += '<tr><td>Total DAP (cGy.cm<sup>2</sup>):</td><td>{0:.1f}</td>'.format(this_study_dap)
        if this_study_dap >= alert_values['alert_total_dap_rf']:
            msg_body += '. This is above the alert level of {0:.1f}\r\n'.format(alert_values['alert_total_dap_rf'])
            html_msg_body += '<td>Above the {0:.1f} alert level</td></tr>'.format(alert_values['alert_total_dap_rf'])
        else:
            msg_body += '\r\n'
            html_msg_body += '</tr>'
        msg_body += '\r\n'
        html_msg_body += '</table>'

        msg_body += '\tTotal dose at RP (Gy):\t{0:.1f}'.format(this_study_rp_dose)
        html_msg_body += '<table>'
        html_msg_body += '<tr><td>Total dose at RP (Gy):</td><td>{0:.1f}</td>'.format(this_study_dap)
        if this_study_rp_dose >= alert_values['alert_total_rp_dose_rf']:
            msg_body += '. This is above the alert level of {0:.1f}\r\n'.format(alert_values['alert_total_rp_dose_rf'])
            html_msg_body += '<td>Above the {0:.1f} alert level</td></tr>'.format(alert_values['alert_total_rp_dose_rf'])
        else:
            msg_body += '\r\n'
            html_msg_body += '</tr>'
        msg_body += '\r\n'
        html_msg_body += '</table>'

        # if calc_accum_dose_over_delta_weeks_on_import:
        #     try:
        #         if accum_int_proj_to_update.total_dap_delta_gym2_to_cgycm2() >= alert_values[
        #             'alert_total_dap_rf'] or accum_int_proj_to_update.dose_rp_total_over_delta_weeks >= alert_values[
        #             'alert_total_rp_dose_rf']:
        #             # Add these items to the message too
        #             msg_body += '\r\n'
        #             msg_body += 'Total DAP and dose and RP for this patient ID from the past {0} weeks\r\n'.format(
        #                 week_delta)
        #             msg_body += '\tNumber of studies from the past {0} weeks:\t{1}\r\n'.format(week_delta,
        #                                                                                        included_studies.count())
        #             msg_body += '\tTotal DAP from the past {0} weeks (cGy.cm2):\t{1:.1f}'.format(week_delta,
        #                                                                                          accum_int_proj_to_update.total_dap_delta_gym2_to_cgycm2())
        #             html_msg_body += '<p>Total DAP and dose and RP for this patient ID from the past {0} weeks</p>'.format(
        #                 week_delta)
        #             html_msg_body += '<table>'
        #             html_msg_body += '<tr><th>Item</th><th>Value</th><th>Comments</th></tr>'
        #             html_msg_body += '<tr><td>Number of studies from the past {0} weeks:</td><td>{1}</td><td></td></tr>'.format(
        #                 week_delta, included_studies.count())
        #             html_msg_body += '<tr><td>Total DAP from the past {0} weeks (cGy.cm2):</td><td>{1:.1f}</td>'.format(
        #                 week_delta, accum_int_proj_to_update.total_dap_delta_gym2_to_cgycm2())
        #             if accum_int_proj_to_update.total_dap_delta_gym2_to_cgycm2() >= alert_values['alert_total_dap_rf']:
        #                 msg_body += '. This is above the alert level of {1:.1f}\r\n'.format(week_delta, alert_values[
        #                     'alert_total_dap_rf'])
        #                 html_msg_body += '<td>Above the {1:.1f} alert level</td></tr>'.format(week_delta, alert_values[
        #                     'alert_total_dap_rf'])
        #             else:
        #                 msg_body += '\r\n'
        #                 html_msg_body += '<td>None</td></tr>'
        #             msg_body += '\r\n'
        #
        #             msg_body += '\tTotal dose at RP from the past {0} weeks (Gy):\t{1:.1f}'.format(week_delta,
        #                                                                                            accum_int_proj_to_update.dose_rp_total_over_delta_weeks)
        #             html_msg_body += '<tr><td>Total dose at RP from the past {0} weeks (Gy)</td><td>{1:.1f}</td>'.format(
        #                 week_delta, accum_int_proj_to_update.dose_rp_total_over_delta_weeks)
        #             if accum_int_proj_to_update.dose_rp_total_over_delta_weeks >= alert_values['alert_total_rp_dose_rf']:
        #                 msg_body += '. This is above the alert level of {1:.1f}\r\n'.format(week_delta, alert_values[
        #                     'alert_total_rp_dose_rf'])
        #                 html_msg_body += '<td>Above the {1:.1f} alert level</td></tr>'.format(week_delta, alert_values[
        #                     'alert_total_rp_dose_rf'])
        #             else:
        #                 msg_body += '\r\n'
        #                 html_msg_body += '<td>None</td></tr>'
        #             msg_body += '\r\n'
        #             html_msg_body += '</table>'
        #
        #             msg_body += 'All studies for this patient ID from the past {0} weeks are:\r\n'.format(week_delta)
        #             msg_body += 'OpenREM link\tStudy date\tStudy time\tAccession number\tDAP (cGy.cm2)\tDose at RP (Gy)\r\n'
        #             html_msg_body += '<p>All studies for this patient ID from the past {0} weeks are:</p>'.format(
        #                 week_delta)
        #             html_msg_body += '<table>'
        #             html_msg_body += '<tr><th>OpenREM link</th><th>Study date</th><th>Study time</th><th>Accession number</th><th>DAP (cGy.cm<sup>2</sup>)</th><th>Dose at RP (Gy)</th></tr>'
        #             linked_studies = GeneralStudyModuleAttr.objects.filter(
        #                 pk__in=included_studies.values_list('pk', flat=True))
        #             for linked_study in linked_studies:
        #                 linked_study_dap = linked_study.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get().convert_gym2_to_cgycm2()
        #                 linked_study_rp_dose = linked_study.projectionxrayradiationdose_set.get().accumxraydose_set.get().accumintegratedprojradiogdose_set.get().dose_rp_total
        #                 msg_body += '{0}\t{1}\t{2}\t{3}\t{4:.1f}\t{5:.1f}\r\n'.format(
        #                     reverse('rf_detail_view', args=[linked_study.pk]), linked_study.study_date.strftime('%x'),
        #                     linked_study.study_time.strftime('%X'), linked_study.accession_number, linked_study_dap,
        #                     linked_study_rp_dose)
        #                 html_msg_body += '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4:.1f}</td><td>{5:.1f}</td></tr>'.format(
        #                     reverse('rf_detail_view', args=[linked_study.pk]), linked_study.study_date.strftime('%x'),
        #                     linked_study.study_time.strftime('%X'), linked_study.accession_number, linked_study_dap,
        #                     linked_study_rp_dose)
        #             html_msg_body += '</table>'
        #
        #     except NameError:  # There's a chance that accum_int_proj_to_update or included_studies won't exist
        #         pass

        from django.contrib.auth.models import User
        from django.core.mail import send_mail, EmailMultiAlternatives
        from openremproject import settings

        msg_subject = 'OpenREM high dose alert'
        recipients = User.objects.filter(
            highdosemetricalertrecipients__receive_high_dose_metric_alerts__exact=True).values_list('email', flat=True)

        msg = EmailMultiAlternatives(msg_subject, msg_body, settings.EMAIL_DOSE_ALERT_SENDER, recipients)
        msg.attach_alternative(html_msg_body, 'text/html')
        msg.send()

        # send_mail(msg_subject,
        #          msg_body,
        #          settings.EMAIL_DOSE_ALERT_SENDER,
        #          recipients,
        #          fail_silently=False)
