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
..  module:: urls.
    :synopsis: Module to match URLs and pass over to views or export modules.

..  moduleauthor:: Ed McDonagh

"""

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from remapp.views import DicomStoreCreate, DicomStoreUpdate, DicomStoreDelete
from remapp.views import DicomQRCreate, DicomQRUpdate, DicomQRDelete
from remapp.views import PatientIDSettingsUpdate, DicomDeleteSettingsUpdate, SkinDoseMapCalcSettingsUpdate, \
                         RFHighDoseAlertSettings
from remapp.views import NotPatientNameCreate, NotPatientNameUpdate, NotPatientNameDelete
from remapp.views import NotPatientIDCreate, NotPatientIDUpdate, NotPatientIDDelete

urlpatterns = patterns('remapp.views',

                       url(r'^$', 'openrem_home', name='home'),
                       url(r'^hometotals/$', 'update_modality_totals', name='update_modality_totals'),
                       url(r'^homestudies/$', 'update_latest_studies', name='update_latest_studies'),
                       url(r'^homeworkload/$', 'update_study_workload', name='update_study_workload'),

                       url(r'^rf/$', 'rf_summary_list_filter', name='rf_summary_list_filter'),
                       url(r'^rf/chart/$', 'rf_summary_chart_data', name='rf_summary_chart_data'),
                       url(r'^rf/(?P<pk>\d+)/$', 'rf_detail_view', name='rf_detail_view'),
                       url(r'^rf/(?P<pk>\d+)/skin_map/$', 'rf_detail_view_skin_map', name='rf_detail_view_skin_map'),

                       url(r'^ct/$', 'ct_summary_list_filter', name='ct_summary_list_filter'),
                       url(r'^ct/chart/$', 'ct_summary_chart_data', name='ct_summary_chart_data'),
                       url(r'^ct/(?P<pk>\d+)/$', 'ct_detail_view', name='ct_detail_view'),

                       url(r'^dx/$', 'dx_summary_list_filter', name='dx_summary_list_filter'),
                       url(r'^dx/chart/$', 'dx_summary_chart_data', name='dx_summary_chart_data'),
                       url(r'^dx/(?P<pk>\d+)/$', 'dx_detail_view', name='dx_detail_view'),

                       url(r'^mg/$', 'mg_summary_list_filter', name='mg_summary_list_filter'),
                       url(r'^mg/chart/$', 'mg_summary_chart_data', name='mg_summary_chart_data'),
                       url(r'^mg/(?P<pk>\d+)/$', 'mg_detail_view', name='mg_detail_view'),

                       url(r'^viewdisplaynames/$', 'display_names_view', name='display_names_view'),

                       url(r'^delete/(?P<pk>\d+)$', 'study_delete', name='study_delete'),
                       url(r'^admin/sizeupload$', 'size_upload', name='size_upload'),
                       url(r'^admin/sizeprocess/(?P<pk>\d+)/$', 'size_process', name='size_process'),
                       url(r'^admin/sizeimports', 'size_imports', name='size_imports'),
                       url(r'^admin/sizedelete', 'size_delete', name='size_delete'),
                       url(r'^admin/sizeimport/abort/(?P<pk>\d+)$', 'size_abort', name='size_abort'),
                       url(r'^admin/sizelogs/(?P<task_id>[a-f0-9-]{36})$', 'size_download', name='size_download'),
                       url(r'^updatedisplaynames/$', 'display_name_update', name='display_name_update'),
                       url(r'^populatedisplaynames$', 'display_name_populate', name='display_name_populate'),
                       url(r'^populatefailedimportlist', 'failed_list_populate', name='failed_list_populate'),
                       url(r'^admin/reprocessdual/(?P<pk>\d+)/$', 'reprocess_dual', name='reprocess_dual'),
                       url(r'^admin/review/(?P<equip_name_pk>\d+)/(?P<modality>\w+)/$', 'review_summary_list',
                           name='review_summary_list'),
                       url(r'^admin/review/study$', 'review_study_details', name='review_study_details'),
                       url(r'^admin/review/studiesdelete$', 'review_studies_delete', name='review_studies_delete'),
                       url(r'^admin/equipmentlastdateandcount$', 'display_name_last_date_and_count',
                           name='display_name_last_date_and_count'),
                       url(r'^admin/review/studiesequipdelete$', 'review_studies_equip_delete',
                           name='review_studies_equip_delete'),
                       url(r'^admin/review/failed/(?P<modality>\w+)/$', 'review_failed_imports',
                           name='review_failed_imports'),
                       url(r'^admin/review/failed/study$', 'review_failed_study_details',
                           name='review_failed_study_details'),
                       url(r'^admin/review/studiesdeletefailed$', 'review_failed_studies_delete',
                           name='review_failed_studies_delete'),
                       url(r'^chartoptions/$', 'chart_options_view', name='chart_options_view'),
                       url(r'^homepageoptions/$', 'homepage_options_view', name='homepage_options_view'),
                       url(r'^admin/dicomsummary', 'dicom_summary', name='dicom_summary'),
                       url(r'^admin/dicomstore/add/$', DicomStoreCreate.as_view(), name='dicomstore_add'),
                       url(r'^admin/dicomstore/(?P<pk>\d+)/$', DicomStoreUpdate.as_view(), name='dicomstore_update'),
                       url(r'^admin/dicomstore/(?P<pk>\d+)/delete/$', DicomStoreDelete.as_view(),
                           name='dicomstore_delete'),
                       url(r'^admin/dicomqr/add/$', DicomQRCreate.as_view(), name='dicomqr_add'),
                       url(r'^admin/dicomqr/(?P<pk>\d+)/$', DicomQRUpdate.as_view(), name='dicomqr_update'),
                       url(r'^admin/dicomqr/(?P<pk>\d+)/delete/$', DicomQRDelete.as_view(), name='dicomqr_delete'),
                       url(r'^admin/patientidsettings/(?P<pk>\d+)/$', PatientIDSettingsUpdate.as_view(),
                           name='patient_id_settings_update'),
                       url(r'^admin/dicomdelsettings/(?P<pk>\d+)/$', DicomDeleteSettingsUpdate.as_view(),
                           name='dicom_delete_settings_update'),
                       url(r'^admin/skindosemapsettings/(?P<pk>\d+)/$', SkinDoseMapCalcSettingsUpdate.as_view(),
                           name='skin_dose_map_settings_update'),
                       url(r'^admin/notpatientindicators/$', 'not_patient_indicators', name='not_patient_indicators'),
                       url(r'^admin/notpatientindicators/restore074/$', 'not_patient_indicators_as_074',
                           name='not_patient_indicators_as_074'),
                       url(r'^admin/notpatientindicators/names/add/$', NotPatientNameCreate.as_view(),
                           name='notpatientname_add'),
                       url(r'^admin/notpatientindicators/names/(?P<pk>\d+)/$', NotPatientNameUpdate.as_view(),
                           name='notpatientname_update'),
                       url(r'^admin/notpatientindicators/names/(?P<pk>\d+)/delete/$', NotPatientNameDelete.as_view(),
                           name='notpatientname_delete'),
                       url(r'^admin/notpatientindicators/id/add/$', NotPatientIDCreate.as_view(),
                           name='notpatienid_add'),
                       url(r'^admin/notpatientindicators/id/(?P<pk>\d+)/$', NotPatientIDUpdate.as_view(),
                           name='notpatientid_update'),
                       url(r'^admin/notpatientindicators/id/(?P<pk>\d+)/delete/$', NotPatientIDDelete.as_view(),
                           name='notpatientid_delete'),
                       url(r'^admin/adminquestions/hide_not_patient/$', 'admin_questions_hide_not_patient',
                           name='admin_questions_hide_not_patient'),
                       url(r'^admin/rfalertsettings/(?P<pk>\d+)/$', RFHighDoseAlertSettings.as_view(),
                           name='rf_alert_settings_update'),
                       url(r'^admin/rfalertnotifications/$', 'rf_alert_notifications_view',
                           name='rf_alert_notifications_view'),
                       url(r'^admin/rfrecalculateaccumdoses/', 'rf_recalculate_accum_doses',
                           name='rf_recalculate_accum_doses'),
                       # url(r'^password/$', 'change_password', name='change_password'),
                       url('^change_password/$', auth_views.password_change,
                           {'template_name': 'registration/changepassword.html'}, name='password_change'),
                       url('^change_password/done/$', auth_views.password_change_done,
                           {'template_name': 'registration/changepassworddone.html'}, name='password_change_done'),
                       url('^admin/rabbitmq/$', 'rabbitmq_admin', name='rabbitmq_admin'),
                       url('^admin/rabbitmq/queues/$', 'rabbitmq_queues', name='rabbitmq_queues'),
                       url('^admin/rabbitmq/purge_queue/(?P<queue>[0-9a-zA-Z.@-]+)$', 'rabbitmq_purge',
                           name='rabbitmq_purge'),
                       )

urlpatterns += patterns('remapp.exports.exportviews',
                        url(r'^export/$', 'export', name='export'),
                        url(r'^exportctcsv1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'ctcsv1', name='ctcsv1'),
                        url(r'^exportctxlsx1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'ctxlsx1', name='ctxlsx1'),
                        url(r'^exportdxcsv1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'dxcsv1', name='dxcsv1'),
                        url(r'^exportdxxlsx1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'dxxlsx1', name='dxxlsx1'),
                        url(r'^exportflcsv1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'flcsv1', name='flcsv1'),
                        url(r'^exportrfxlsx1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'rfxlsx1', name='rfxlsx1'),
                        url(r'^exportrfopenskin/(?P<pk>\d+)$', 'rfopenskin', name='rfopenskin'),
                        url(r'^exportmgcsv1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'mgcsv1', name='mgcsv1'),
                        url(r'^exportmgxlsx1/(?P<name>\w+)/(?P<pat_id>\w+)/$', 'mgxlsx1', name='mgxlsx1'),
                        url(r'^exportmgnhsbsp/$', 'mgnhsbsp', name='mgnhsbsp'),
                        url(r'^download/(?P<task_id>[a-f0-9-]{36})$', 'download', name='download'),
                        url(r'^deletefile/$', 'deletefile', name='deletefile'),
                        url(r'^export/abort/(?P<pk>\d+)$', 'export_abort', name='export_abort'),
                        url(r'^export/updateactive$', 'update_active', name='update_active'),
                        url(r'^export/updateerror$', 'update_error', name='update_error'),
                        url(r'^export/updatecomplete$', 'update_complete', name='update_complete'),
                        )

urlpatterns += patterns('remapp.exports',
                        url(r'^xlsx/openrem/ct/', 'ct_export.ctxlsx', name='ct_export_ctxlsx'),
                        )

urlpatterns += patterns('remapp.views',
                        url(r'^charts_off/$', 'charts_off', name='charts_off'),
                        )


urlpatterns += patterns('remapp.netdicom.dicomviews',
                        url(r'admin/dicomstore/(?P<pk>\d+)/start/$', 'run_store', name='run_store'),
                        url(r'admin/dicomstore/(?P<pk>\d+)/stop/$', 'stop_store', name='stop_store'),
                        url(r'admin/dicomstore/statusupdate', 'status_update_store', name='status_update_store'),
                        url(r'admin/queryupdate$', 'q_update', name='query_update'),
                        url(r'admin/queryprocess$', 'q_process', name='q_process'),
                        url(r'admin/queryremote$', 'dicom_qr_page', name='dicom_qr_page'),
                        url(r'admin/queryretrieve$', 'r_start', name='start_retrieve'),
                        url(r'admin/moveupdate$', 'r_update', name='move_update'),
                        )

