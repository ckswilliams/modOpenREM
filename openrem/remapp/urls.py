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
from remapp.models import Accumulated_projection_xray_dose, General_study_module_attributes


urlpatterns = patterns('remapp.views',

    url(r'^$',
        'openrem_home'),

    url(r'^rf/$',
        'rf_summary_list_filter'),
    url(r'^rf/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=General_study_module_attributes,
            template_name='remapp/rfdetail.html'))),

    url(r'^ct/$',
        'ct_summary_list_filter'),
    url(r'^ct/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=General_study_module_attributes,
            template_name='remapp/ctdetail.html'))),

    url(r'^ct$',
        'ct_summary_list_filter'),


    url(r'^mg/$',
        'mg_summary_list_filter'),
    url(r'^mg/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=General_study_module_attributes,
            template_name='remapp/mgdetail.html'))),

    url(r'^delete/(?P<pk>\d+)$', 'study_delete', name='study_delete'),
    url(r'^admin/sizeupload$', 'size_upload', name='size_upload'),
)

urlpatterns += patterns('remapp.exports',
#    url(r'^export/openrem/rf/', 'exportcsv.exportFL2excel'),
#    url(r'^export/openrem/ct/', 'exportcsv.exportCT2excel'),
#    url(r'^export/openrem/mg/', 'exportcsv.exportMG2excel'),
    url(r'^ct/do_ct_csv$', 'ajaxviews.ct_csv', name="ct_csv"),
    url(r'^do_ct_csv$', 'ajaxviews.ct_csv', name="ct_csv"),
    url(r'^ct/csv_export_task$', 'ajaxviews.ct_csv'),
    url(r'^export/$', 'ajaxviews.export'),
    url(r'^download/(?P<file_name>.+)$', 'ajaxviews.download'),
    url(r'^exportctcsv1/$', 'ajaxviews.ctcsv1'),
    url(r'^exportctxlsx1/$', 'ajaxviews.ctxlsx1'),
    url(r'^exportflcsv1/$', 'ajaxviews.flcsv1'),
    url(r'^exportmgcsv1/$', 'ajaxviews.mgcsv1'),
    url(r'^exportmgnhsbsp/$', 'ajaxviews.mgnhsbsp'),
    url(r'^deletefile/$', 'ajaxviews.deletefile'),
)

urlpatterns += patterns('remapp.exports',
    url(r'^xlsx/openrem/ct/',
        'xlsx.ctxlsx'),
)

urlpatterns += patterns('remapp.views',
    url(r'^celerytest$', 'celerytest', name="celerytest"),
    url(r'^do_task$', 'do_task', name="do_task"),
    url(r'^poll_state$', 'poll_state', name="poll_state"),
)
