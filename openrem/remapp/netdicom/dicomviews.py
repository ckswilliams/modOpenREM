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
def q_update(request):
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
        resp['status'] = 'not complete'
        resp['message'] = '<h4>Query {0} not yet started</h4>'.format(query_id)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if query.failed:
        resp['status'] = 'failed'
        resp['message'] ='<h4>Query Failed</h4> {0}'.format(query.message)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    study_rsp = query.dicomqrrspstudy_set.all()
    if not query.complete:
        modalities = study_rsp.values('modalities_in_study').annotate(count=Count('pk'))
        table = ['<table class="table table-bordered"><tr><th>Modalities in study</th><th>Number of responses</th></tr>']
        for m in modalities:
            table.append('<tr><td>')
            if m['modalities_in_study']:
                table.append(', '.join(json.loads(m['modalities_in_study'])))
            else:
                table.append('Unknown')
            table.append('</td><td>')
            table.append(str(m['count']))
            table.append('</tr></td>')
        table.append('</table>')
        tablestr = ''.join(table)
        resp['status'] = 'not complete'
        resp['message'] ='<h4>{0}</h4><p>Responses so far:</p> {1}'.format(query.stage, tablestr)
    else:
        modalities = study_rsp.values('modality').annotate(count=Count('pk'))
        table = ['<table class="table table-bordered"><tr><th>Modality</th><th>Number of responses</th></tr>']
        for m in modalities:
            table.append('<tr><td>')
            if m['modality']:
                table.append(m['modality'])
            else:
                table.append('Unknown - SR only study?')
            table.append('</td><td>')
            table.append(str(m['count']))
            table.append('</tr></td>')
        table.append('</table>')
        tablestr = ''.join(table)
        resp['status'] = 'complete'
        resp['message'] ='<h4>Query complete</h4> {0}'.format(tablestr)

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
@login_required
def q_process(request, *args, **kwargs):
    import uuid
    import datetime
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from remapp.netdicom.qrscu import qrscu
    from remapp.models import DicomRemoteQR
    from remapp.forms import DicomQueryForm

    if request.method == 'POST':
        form = DicomQueryForm(request.POST)
        if form.is_valid():
            rh_pk = form.cleaned_data.get('remote_host_field')
            store_pk = form.cleaned_data.get('store_scp_field')
            date_from = form.cleaned_data.get('date_from_field')
            date_until = form.cleaned_data.get('date_until_field')
            modalities = form.cleaned_data.get('modality_field')
            inc_sr = form.cleaned_data.get('inc_sr_field')
            duplicates = form.cleaned_data.get('duplicates_field')
            query_id = str(uuid.uuid4())
            # rh = DicomRemoteQR.objects.get(pk=rh_pk)
            # if rh.hostname:
            #     host = rh.hostname
            # else:
            #     host = rh.ip

            if date_from:
                date_from = date_from.isoformat()
            if date_until:
                date_until = date_until.isoformat()

            task = qrscu.delay(qr_scp_pk=rh_pk, store_scp_pk=store_pk, query_id=query_id, date_from=date_from,
                               date_until=date_until, modalities=modalities, inc_sr=inc_sr, duplicates=duplicates)

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

            try:
                vers = pkg_resources.require("openrem")[0].version
            except:
                vers = ''
            admin = {'openremversion' : vers}

            for group in request.user.groups.all():
                admin[group.name] = True

            return render_to_response(
                'remapp/dicomqr.html',
                {'form':form, 'admin':admin},
                context_instance=RequestContext(request)
            )
            # return HttpResponse(
            #     json.dumps(resp),
            #     content_type="application/json"
            # )



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

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/dicomqr.html',
        {'form':form, 'admin':admin},
        context_instance=RequestContext(request)
    )

@csrf_exempt
@login_required
def r_start(request):
    from remapp.netdicom.qrscu import movescu
    resp = {}
    data = request.POST
    query_id = data.get('query_id')
    resp['query_id'] = query_id

    movescu.delay(query_id)

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def r_update(request):
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
        resp['status'] = 'not complete'
        resp['message'] = '<h4>Move request {0} not yet started</h4>'.format(query_id)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if query.failed:
        resp['status'] = 'failed'
        resp['message'] ='<h4>Move request failed</h4> {0}'.format(query.message)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if not query.move_complete:
        resp['status'] = 'not complete'
        resp['message'] ='<h4>{0}</h4>'.format(query.stage)
    else:
        resp['status'] = 'move complete'
        resp['message'] = '<h4>Move request complete</h4>'

    return HttpResponse(json.dumps(resp), content_type='application/json')
