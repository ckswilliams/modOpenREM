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
..  module:: dicomviews.py
    :synopsis: To manage the DICOM servers

..  moduleauthor:: Ed McDonagh

"""

# Following two lines added so that sphinx autodocumentation works.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def run_store(request, pk):
    from django.shortcuts import redirect
    from remapp.models import DicomStoreSCP
    from remapp.netdicom.storescp import web_store
    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        store = DicomStoreSCP.objects.get(pk__exact = pk)
        store.run = True
        store.save()
        storetask = web_store.delay(store_pk=pk)
    return redirect('/openrem/admin/dicomsummary/')

@csrf_exempt
@login_required
def stop_store(request, pk):
    from django.shortcuts import redirect
    from remapp.models import DicomStoreSCP
    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        store = DicomStoreSCP.objects.filter(pk__exact = pk)
        if store and store[0].task_id:
            store[0].run = False
            store[0].save()
            store[0].status = "Quit signal sent"
            store[0].save()
        else:
            print "Invalid primary key or no task_id recorded"
    return redirect('/openrem/admin/dicomsummary/')

import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404

@csrf_exempt
def ajax_test(request):

    sometext = '<div id="sharemenu"><p>AJAX fo the win</p></div>'
    return HttpResponse(sometext)
#    if request.is_ajax():
#         try:
#             pass
#         except KeyError:
#             return HttpResponse('Error') # incorrect post
#         # do stuff, e.g. calculate a score
#         sometext = "Here be some text"
#         return HttpResponse(sometext)
#     else:
#         raise Http404

@csrf_exempt
def ajax_test2(request):
    import uuid
    from remapp.netdicom.qrscu import qrscu

    query_id = str(uuid.uuid4())
    print query_id
    task = qrscu.delay(rh="localhost", rp=1104, query_id=query_id)

    resp = {}
    resp['message'] = 'this might be possible'
    resp['query_id'] = query_id
    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def ajax_test3(request):
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import Count
    from remapp.models import DicomQuery

    resp = {}
    data = request.POST
    query_id = data.get('query_id')
    resp['query_id'] = query_id
    try:
        query = DicomQuery.objects.get(query_id=query_id)
    except ObjectDoesNotExist:
        print 'query_id: {0}'.format(query_id)
        queries = DicomQuery.objects.all()
        for q in queries:
            print q.query_id
        resp['status'] = 'not complete'
        resp['message'] = '<h4>Query {0} not yet started</h4>'.format(query_id)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if query.failed:
        resp['status'] = 'complete'
        resp['message'] ='<h4>Query Failed</h4> {0}'.format(query.message)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    study_rsp = query.dicomqrrspstudy_set.all()
    modalities = study_rsp.values('modality').annotate(count=Count('pk'))
    table = ['<table class="table table-bordered">']
    for m in modalities:
        table.append('<tr><td>')
        table.append(m['modality'])
        table.append('</td><td>')
        table.append(str(m['count']))
        table.append('</tr></td>')
    table.append('</table>')
    tablestr = ''.join(table)

    if query.complete:
        resp['status'] = 'complete'
        resp['message'] ='<h4>Query Complete</h4> {0}'.format(tablestr)
    else:
        resp['status'] = 'not complete'
        resp['message'] ='<h4>Query not yet complete</h4><p>Responses so far:</p> {0}'.format(tablestr)
    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
@login_required
def q_process(request, *args, **kwargs):
    import uuid
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from remapp.netdicom.qrscu import qrscu
    from remapp.models import DicomRemoteQR
    from remapp.forms import DicomQueryForm

    if request.method == 'POST':
        form = DicomQueryForm(request.POST)
        if form.is_valid():
            print "Form is valid"
            rh_pk = request.POST['remote_host_field']
            date_from = request.POST['date_from_field']
            date_until = request.POST['date_until_field']
            modalities = request.POST.get('modality_field',None);
            query_id = str(uuid.uuid4())
            print query_id
            rh = DicomRemoteQR.objects.get(pk=rh_pk)
            if rh.hostname:
                host = rh.hostname
            else:
                host = rh.ip
            task = qrscu.delay(rh=host, rp=rh.port, query_id=query_id)

            resp = {}
            resp['message'] = 'Request created'
            resp['status'] = 'not complete'
            resp['query_id'] = query_id

            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            print "Bother, form wasn't valid"
            errors = form.errors
            print errors
            print form

            # Need to find a way to deal with this event
#            render_to_response('remapp/dicomqr.html', {'form': form}, context_instance=RequestContext(request))
            resp = {}
            resp['message'] = errors
            resp['status'] = 'not complete'
            return HttpResponse(
                json.dumps(resp),
                content_type="application/json"
            )



@login_required
def dicom_qr_page(request, *args, **kwargs):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from remapp.forms import DicomQueryForm

    form = DicomQueryForm

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
        'remapp/dicomqr.html',
        {'form':form, 'admin':admin},
        context_instance=RequestContext(request)
    )
