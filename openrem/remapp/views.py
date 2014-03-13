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
..  module:: views.
    :synopsis: Module to render appropriate content according to request.

..  moduleauthor:: Ed McDonagh

"""

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime
from remapp.models import General_study_module_attributes

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/openrem/')



def rf_summary_list_filter(request):
    from remapp.interface.mod_filters import RFSummaryListFilter
    import pkg_resources # part of setuptools
    f = RFSummaryListFilter(request.GET, queryset=General_study_module_attributes.objects.filter(modality_type__contains = 'RF'))
    admin = {'openremversion' : pkg_resources.require("openrem")[0].version}
    return render_to_response(
        'remapp/rffiltered.html',
        {'filter': f, 'admin':admin},
        context_instance=RequestContext(request)
        )

def ct_summary_list_filter(request):
    from remapp.interface.mod_filters import CTSummaryListFilter
    import pkg_resources # part of setuptools
    f = CTSummaryListFilter(request.GET, queryset=General_study_module_attributes.objects.filter(modality_type__exact = 'CT'))
    admin = {'openremversion' : pkg_resources.require("openrem")[0].version}
    return render_to_response(
        'remapp/ctfiltered.html',
        {'filter': f, 'admin':admin},
        context_instance=RequestContext(request)
        )


def mg_summary_list_filter(request):
    from remapp.interface.mod_filters import MGSummaryListFilter
    import pkg_resources # part of setuptools
    filter_data = request.GET.copy()
    if 'page' in filter_data:
        del filter_data['page']
    f = MGSummaryListFilter(filter_data, queryset=General_study_module_attributes.objects.filter(modality_type__exact = 'MG'))
    admin = {'openremversion' : pkg_resources.require("openrem")[0].version}
    return render_to_response(
        'remapp/mgfiltered.html',
        {'filter': f, 'admin':admin},
        context_instance=RequestContext(request)
        )


def openrem_home(request):
    from remapp.models import General_study_module_attributes
    from datetime import datetime
    import pytz
    from collections import OrderedDict
    import pkg_resources # part of setuptools
    utc = pytz.UTC
    allstudies = General_study_module_attributes.objects.all()
    homedata = { 
        'total' : allstudies.count(),
        'mg' : allstudies.filter(modality_type__exact = 'MG').count(),
        'ct' : allstudies.filter(modality_type__exact = 'CT').count(),
        'rf' : allstudies.filter(modality_type__contains = 'RF').count(),
        }
    admin = {'openremversion' : pkg_resources.require("openrem")[0].version}
    modalities = ('MG','CT','RF')
    for modality in modalities:
        studies = allstudies.filter(modality_type__contains = modality).all()
        stations = studies.values_list('general_equipment_module_attributes__station_name').distinct()
        modalitydata = {}
        for station in stations:
            latestdate = studies.filter(
                general_equipment_module_attributes__station_name__exact = station[0]
                ).latest('study_date').study_date
            latestuid = studies.filter(general_equipment_module_attributes__station_name__exact = station[0]
                ).filter(study_date__exact = latestdate).latest('study_time')
            latestdatetime = datetime.combine(latestuid.study_date, latestuid.study_time)
            latestdatetimeaware = utc.localize(latestdatetime)
            
            inst_name = studies.filter(
                general_equipment_module_attributes__station_name__exact = station[0]
                ).latest('study_date').general_equipment_module_attributes_set.get().institution_name
                
            model_name = studies.filter(
                general_equipment_module_attributes__station_name__exact = station[0]
                ).latest('study_date').general_equipment_module_attributes_set.get().manufacturer_model_name
            
            institution = '{0}, {1}'.format(inst_name,model_name)
                       
            modalitydata[station[0]] = {
                'total' : studies.filter(
                    general_equipment_module_attributes__station_name__exact = station[0]
                    ).count(),
                'latest' : latestdatetimeaware,
                'institution' : institution
            }
        ordereddata = OrderedDict(sorted(modalitydata.items(), key=lambda t: t[1]['latest'], reverse=True))
        homedata[modality] = ordereddata
    
    
    return render(request,"remapp/home.html",{'homedata':homedata, 'admin':admin})

