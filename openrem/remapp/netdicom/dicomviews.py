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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import remapp

@csrf_exempt
@login_required
def run_store(request, pk):
    from django.shortcuts import redirect
    from remapp.models import DicomStoreSCP
    from remapp.netdicom.storescp import web_store
    if request.user.groups.filter(name="admingroup"):
        store = DicomStoreSCP.objects.get(pk__exact = pk)
        store.run = True
        store.save()
        storetask = web_store(store_pk=pk)
    return redirect('/openrem/admin/dicomsummary/')

@csrf_exempt
@login_required
def stop_store(request, pk):
    from django.shortcuts import redirect
    from remapp.models import DicomStoreSCP
    if request.user.groups.filter(name="admingroup"):
        store = DicomStoreSCP.objects.filter(pk__exact = pk)
        if store:
            store[0].run = False
            store[0].save()
            store[0].status = "Quit signal sent"
            store[0].save()
        else:
            print "Can't stop store SCP: Invalid primary key"
    return redirect('/openrem/admin/dicomsummary/')

import json
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404


@csrf_exempt
def status_update_store(request):
    from remapp.models import DicomStoreSCP
    from remapp.netdicom.tools import echoscu

    resp = {}
    data = request.POST
    scp_pk = data.get('scp_pk')

    echo = echoscu(scp_pk=scp_pk, store_scp=True)

    store = DicomStoreSCP.objects.get(pk=scp_pk)

    if echo is "Success":
        resp['message'] = "<div>Last status: {0}</div>".format(store.status)
        resp['statusindicator'] = "<h3 class='pull-right panel-title'><span class='glyphicon glyphicon-ok' aria-hidden='true'></span><span class='sr-only'>OK:</span> Server is alive</h3>"
        resp['delbutton'] = "<button type='button' class='btn btn-primary' disabled='disabled'>Delete</button>"
        resp['startbutton'] = ""
        resp['stopbutton'] = "<a class='btn btn-danger' href='/openrem/admin/dicomstore/{0}/stop/' role='button'>Stop server</a>".format(scp_pk)
    elif echo is "AssocFail":
        resp['message'] = "<div>Last status: {0}</div>".format(store.status)
        resp['statusindicator'] = "<h3 class='pull-right panel-title status-red'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span><span class='sr-only'>Error:</span> Association fail - server not running?</h3>"
        resp['delbutton'] = "<a class='btn btn-primary' href='/openrem/admin/dicomstore/{0}/delete/' role='button'>Delete</a>".format(scp_pk)
        resp['startbutton'] = "<a class='btn btn-success' href='/openrem/admin/dicomstore/{0}/start/' role='button'>Start server</a>".format(scp_pk)
        resp['stopbutton'] = ""

    return HttpResponse(json.dumps(resp), content_type="application/json")

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
            desc_exclude = form.cleaned_data.get('desc_exclude_field')
            desc_include = form.cleaned_data.get('desc_include_field')
            query_id = str(uuid.uuid4())

            if date_from:
                date_from = date_from.isoformat()
            if date_until:
                date_until = date_until.isoformat()

            if desc_exclude:
                study_desc_exc = map(unicode.lower, map(unicode.strip, desc_exclude.split(',')))
            else:
                study_desc_exc = None
            if desc_include:
                study_desc_inc = map(unicode.lower, map(unicode.strip, desc_include.split(',')))
            else:
                study_desc_inc = None

            task = qrscu.delay(qr_scp_pk=rh_pk, store_scp_pk=store_pk, query_id=query_id, date_from=date_from,
                               date_until=date_until, modalities=modalities, inc_sr=inc_sr, duplicates=duplicates,
                               study_desc_exc=study_desc_exc, study_desc_inc=study_desc_inc)

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

            admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

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
    from remapp.models import DicomStoreSCP, DicomRemoteQR
    from remapp.netdicom.tools import echoscu

    if not request.user.groups.filter(name="importqrgroup"):
        messages.error(request, "You are not in the importqrgroup - please contact your administrator")
        return redirect('/openrem/')

    form = DicomQueryForm

    storestatus = {}
    stores = DicomStoreSCP.objects.all()
    for store in stores:
        echo = echoscu(scp_pk=store.pk, store_scp=True)
        if echo is "Success":
            storestatus[store.name] = "<span class='glyphicon glyphicon-ok' aria-hidden='true'></span><span class='sr-only'>OK:</span> responding to DICOM echo"
        else:
            storestatus[store.name] = "<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span><span class='sr-only'>Error:</span> not responding to DICOM echo"

    qrstatus = {}
    qr = DicomRemoteQR.objects.all()
    for scp in qr:
        echo = echoscu(scp_pk=scp.pk, qr_scp=True)
        if echo is "Success":
            qrstatus[scp.name] = "<span class='glyphicon glyphicon-ok' aria-hidden='true'></span><span class='sr-only'>OK:</span> responding to DICOM echo"
        else:
            qrstatus[scp.name] = "<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span><span class='sr-only'>Error:</span> not responding to DICOM echo"

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/dicomqr.html',
        {'form':form, 'storestatus':storestatus, 'qrstatus':qrstatus, 'admin':admin},
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
