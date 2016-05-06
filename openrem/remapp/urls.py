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

from django.conf.urls import patterns, include, url
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from remapp.models import AccumProjXRayDose, GeneralStudyModuleAttr
from remapp.views import DicomStoreCreate, DicomStoreUpdate, DicomStoreDelete
from remapp.views import DicomQRCreate, DicomQRUpdate, DicomQRDelete
from remapp.views import PatientIDSettingsUpdate, DicomDeleteSettingsUpdate, SkinDoseMapCalcSettingsUpdate


urlpatterns = patterns('remapp.views',

    url(r'^$',
        'openrem_home', name='home'),

    url(r'^rf/$',
        'rf_summary_list_filter'),
    url(r'^rf/chart/$',
        'rf_summary_chart_data', name='rf_summary_chart_data'),
    url(r'^rf/(?P<pk>\d+)/$', 'rf_detail_view', name='rf_detail_view'),
    url(r'^rf/(?P<pk>\d+)/skin_map/$', 'rf_detail_view_skin_map', name='rf_detail_view_skin_map'),

    url(r'^ct/$',
        'ct_summary_list_filter'),
    url(r'^ct/chart/$',
        'ct_summary_chart_data', name='ct_summary_chart_data'),
    url(r'^ct/(?P<pk>\d+)/$', 'ct_detail_view', name='ct_detail_view'),

    url(r'^dx/$',
        'dx_summary_list_filter', name='dx_summary'),
    url(r'^dx/chart/$',
        'dx_summary_chart_data', name='dx_summary_chart_data'),
    url(r'^dx/(?P<pk>\d+)/$', 'dx_detail_view', name='dx_detail_view'),

    url(r'^mg/$',
        'mg_summary_list_filter'),
    url(r'^mg/chart/$',
        'mg_summary_chart_data', name='mg_summary_chart_data'),
    url(r'^mg/(?P<pk>\d+)/$', 'mg_detail_view', name='mg_detail_view'),

    url(r'^viewdisplaynames/$',
        'display_names_view'),

    url(r'^delete/(?P<pk>\d+)$', 'study_delete', name='study_delete'),
    url(r'^admin/sizeupload$', 'size_upload', name='size_upload'),
    url(r'^admin/sizeprocess/(?P<pk>\d+)/$', 'size_process', name='size_process'),
    url(r'^admin/sizeimports', 'size_imports', name='size_imports'),
    url(r'^admin/sizedelete', 'size_delete', name='size_delete'),
    url(r'^admin/sizeimport/abort/(?P<pk>\d+)$', 'size_abort'),
    url(r'^admin/sizelogs/(?P<task_id>[a-f0-9-]{36})$', 'size_download', name='size_download'),
    url(r'^updatedisplaynames/$', 'display_name_update', name='display_name_update'),
    url(r'^chartoptions/$', 'chart_options_view', name='chart_options_view'),
    url(r'^admin/dicomsummary', 'dicom_summary', name='dicom_summary'),
    url(r'^admin/dicomstore/add/$', DicomStoreCreate.as_view(), name='dicomstore_add'),
    url(r'^admin/dicomstore/(?P<pk>\d+)/$', DicomStoreUpdate.as_view(), name='dicomstore_update'),
    url(r'^admin/dicomstore/(?P<pk>\d+)/delete/$', DicomStoreDelete.as_view(), name='dicomstore_delete'),
    url(r'^admin/dicomqr/add/$', DicomQRCreate.as_view(), name='dicomqr_add'),
    url(r'^admin/dicomqr/(?P<pk>\d+)/$', DicomQRUpdate.as_view(), name='dicomqr_update'),
    url(r'^admin/dicomqr/(?P<pk>\d+)/delete/$', DicomQRDelete.as_view(), name='dicomqr_delete'),
    url(r'^admin/patientidsettings/(?P<pk>\d+)/$', PatientIDSettingsUpdate.as_view(), name='patient_id_settings_update'),
    url(r'^admin/dicomdelsettings/(?P<pk>\d+)/$', DicomDeleteSettingsUpdate.as_view(), name='dicom_delete_settings_update'),
    url(r'^admin/skindosemapsettings/(?P<pk>\d+)/$', SkinDoseMapCalcSettingsUpdate.as_view(), name='skin_dose_map_settings_update'),
)

urlpatterns += patterns('remapp.exports.exportviews',
    url(r'^export/$', 'export'),
    url(r'^exportctcsv1/(?P<name>\w+)/(?P<patid>\w+)/$', 'ctcsv1'),
    url(r'^exportctxlsx1/(?P<name>\w+)/(?P<patid>\w+)/$', 'ctxlsx1'),
    url(r'^exportdxcsv1/(?P<name>\w+)/(?P<patid>\w+)/$', 'dxcsv1'),
    url(r'^exportdxxlsx1/(?P<name>\w+)/(?P<patid>\w+)/$', 'dxxlsx1'),
    url(r'^exportflcsv1/(?P<name>\w+)/(?P<patid>\w+)/$', 'flcsv1'),
    url(r'^exportrfxlsx1/(?P<name>\w+)/(?P<patid>\w+)/$', 'rfxlsx1'),
    url(r'^exportrfopenskin/(?P<pk>\d+)$', 'rfopenskin'),
    url(r'^exportmgcsv1/(?P<name>\w+)/(?P<patid>\w+)/$', 'mgcsv1'),
    url(r'^exportmgnhsbsp/$', 'mgnhsbsp'),
    url(r'^download/(?P<task_id>[a-f0-9-]{36})$', 'download'),
    url(r'^deletefile/$', 'deletefile'),
    url(r'^export/abort/(?P<pk>\d+)$', 'export_abort'),
)

urlpatterns += patterns('remapp.exports',
    url(r'^xlsx/openrem/ct/',
        'xlsx.ctxlsx'),
)

urlpatterns += patterns('remapp.views',
    url(r'^charts_off/$',
        'charts_off'),
)


urlpatterns += patterns('remapp.netdicom.dicomviews',
    url(r'admin/dicomstore/(?P<pk>\d+)/start/$', 'run_store'),
    url(r'admin/dicomstore/(?P<pk>\d+)/stop/$', 'stop_store'),
    url(r'admin/dicomstore/statusupdate', 'status_update_store'),
    url(r'admin/queryupdate$', 'q_update', name='q_update'),
    url(r'admin/queryprocess$', 'q_process', name='q_process'),
    url(r'admin/queryremote$', 'dicom_qr_page', name='dicom_qr_page'),
    url(r'admin/queryretrieve$', 'r_start', name='r_start'),
    url(r'admin/moveupdate$', 'r_update', name='r_update'),
)
