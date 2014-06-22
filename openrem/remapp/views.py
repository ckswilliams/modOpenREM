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
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from remapp.models import General_study_module_attributes

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/openrem/')


@login_required
def rf_summary_list_filter(request):
    from remapp.interface.mod_filters import RFSummaryListFilter
    import pkg_resources # part of setuptools
    f = RFSummaryListFilter(request.GET, queryset=General_study_module_attributes.objects.filter(modality_type__contains = 'RF'))

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''
    admin = {'openremversion' : vers}

    if request.user.groups.filter(name="exportgroup"):
        admin['exportperm'] = True
    if request.user.groups.filter(name="admingroup"):
        admin['adminperm'] = True

    return render_to_response(
        'remapp/rffiltered.html',
        {'filter': f, 'admin':admin},
        context_instance=RequestContext(request)
        )

@login_required
def ct_summary_list_filter(request):
    from remapp.interface.mod_filters import CTSummaryListFilter
    import pkg_resources # part of setuptools

    f = CTSummaryListFilter(request.GET, queryset=General_study_module_attributes.objects.filter(modality_type__exact = 'CT'))

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''
    admin = {'openremversion' : vers}

    if request.user.groups.filter(name="exportgroup"):
        admin['exportperm'] = True
    if request.user.groups.filter(name="admingroup"):
        admin['adminperm'] = True
    
    return render_to_response(
        'remapp/ctfiltered.html',
        {'filter': f, 'admin':admin},
        context_instance=RequestContext(request)
        )

@login_required
def mg_summary_list_filter(request):
    from remapp.interface.mod_filters import MGSummaryListFilter
    import pkg_resources # part of setuptools
    filter_data = request.GET.copy()
    if 'page' in filter_data:
        del filter_data['page']
    f = MGSummaryListFilter(filter_data, queryset=General_study_module_attributes.objects.filter(modality_type__exact = 'MG'))

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''
    admin = {'openremversion' : vers}

    if request.user.groups.filter(name="exportgroup"):
        admin['exportperm'] = True
    if request.user.groups.filter(name="admingroup"):
        admin['adminperm'] = True

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
    
    if not Group.objects.filter(name="viewgroup"):
        vg = Group(name="viewgroup")
        vg.save()
    if not Group.objects.filter(name="exportgroup"):
        eg = Group(name="exportgroup")
        eg.save()
    if not Group.objects.filter(name="admingroup"):
        ag = Group(name="admingroup")
        ag.save()
    
    allstudies = General_study_module_attributes.objects.all()
    homedata = { 
        'total' : allstudies.count(),
        'mg' : allstudies.filter(modality_type__exact = 'MG').count(),
        'ct' : allstudies.filter(modality_type__exact = 'CT').count(),
        'rf' : allstudies.filter(modality_type__contains = 'RF').count(),
        }

    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''
    admin = {'openremversion' : vers}

    if request.user.groups.filter(name="exportgroup"):
        admin['exportperm'] = True
    if request.user.groups.filter(name="admingroup"):
        admin['adminperm'] = True

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
                'latest' : latestdatetime,
                'institution' : institution
            }
        ordereddata = OrderedDict(sorted(modalitydata.items(), key=lambda t: t[1]['latest'], reverse=True))
        homedata[modality] = ordereddata
    
    
    return render(request,"remapp/home.html",{'homedata':homedata, 'admin':admin})

@login_required
def study_delete(request, pk, template_name='remapp/study_confirm_delete.html'):
    study = get_object_or_404(General_study_module_attributes, pk=pk)    

    if request.method=='POST':
        if request.user.groups.filter(name="admingroup"):
            study.delete()
        return redirect("/openrem/")

    if request.user.groups.filter(name="admingroup"):
        return render(request, template_name, {'exam':study})

    return redirect("/openrem/")

import os, sys, csv
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from openrem.settings import MEDIA_ROOT
from remapp.models import Size_upload
from remapp.forms import SizeUploadForm

def size_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = SizeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newcsv = Size_upload(sizefile = request.FILES['sizefile'])
            newcsv.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect("/openrem/admin/sizeprocess/{0}/".format(newcsv.id))
    else:
        form = SizeUploadForm() # A empty, unbound form

    # Load documents for the list page
    sizefiles = Size_upload.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'remapp/sizeupload.html',
        {'documents': sizefiles, 'form': form},
        context_instance=RequestContext(request)
    )

from remapp.forms import SizeHeadersForm
def size_process(request, *args, **kwargs):
    
    csvrecord = Size_upload.objects.all().filter(id__exact = kwargs['pk'])

    with open(os.path.join(MEDIA_ROOT, csvrecord[0].sizefile.name), 'rb') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            if csv.Sniffer().has_header(csvfile.read(1024)):
                csvfile.seek(0)
                dataset = csv.DictReader(csvfile)
                messages.success(request, "Hoorah. CSV file found with delimiter {0}. Headers are {1}.".format(dialect.delimiter, dataset.fieldnames))
                fieldnames = tuple(zip(dataset.fieldnames, dataset.fieldnames))
                form = SizeHeadersForm(my_choice = fieldnames)
            else:
                csvfile.seek(0)
                messages.error(request, "Doesn't appear to have a header row. First row: {0}".format(next(csvfile)))
                return HttpResponseRedirect("/openrem/admin/sizeupload")
        except csv.Error as e:
            messages.error(request, "Doesn't appear to be a csv file. Error({0})".format(e))
            return HttpResponseRedirect("/openrem/admin/sizeupload")
        except:
            messages.error(request, "Unexpected error - please contact an administrator: {0}".format(sys.exc_info()[0]))
            return HttpResponseRedirect("/openrem/admin/sizeupload")

    
    
    return render_to_response(
        'remapp/sizeprocess.html',
        {'form':form},
        context_instance=RequestContext(request)
    )


#**********************************************************************#
#                    Testing celery                                    #
@csrf_exempt
def celerytest(request):
    if 'task_id' in request.session.keys() and request.session['task_id']:
        task_id = request.session['task_id']
    return render_to_response('remapp/celerytest.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def do_task(request):
    """ A view the call the task and write the task id to the session """
    from remapp.tasks import do_work
    data = 'Fail'
    if request.is_ajax():
        job = do_work.delay()
        request.session['task_id'] = job.id
        data = job.id
    else:
        data = 'This is not an ajax request!'

    json_data = json.dumps(data)

    return HttpResponse(json_data, mimetype='application/json')

@csrf_exempt
def poll_state(request):
    """ A view to report the progress to the user """
    from celery.result import AsyncResult
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)

    return HttpResponse(json_data, mimetype='application/json')



#**********************************************************************#
