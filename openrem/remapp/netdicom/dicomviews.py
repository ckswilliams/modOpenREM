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
from django.core.urlresolvers import reverse_lazy
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
    return redirect(reverse_lazy('dicom_summary'))

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
            store[0].status = u"Quit signal sent"
            store[0].save()
        else:
            print u"Can't stop store SCP: Invalid primary key"
    return redirect(reverse_lazy('dicom_summary'))

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
        resp['message'] = u"<div>Last status: {0}</div>".format(store.status)
        resp['statusindicator'] = u"<h3 class='pull-right panel-title'>" \
                                  u"<span class='glyphicon glyphicon-ok' aria-hidden='true'></span>" \
                                  u"<span class='sr-only'>OK:</span> Server is alive</h3>"
        resp['delbutton'] = u"<button type='button' class='btn btn-primary' disabled='disabled'>Delete</button>"
        resp['startbutton'] = u""
        resp['stopbutton'] = u"<a class='btn btn-danger' href='{0}' role='button'>Stop server</a>".format(
            reverse_lazy('stop_store', kwargs={'pk': scp_pk}))
    elif echo is "AssocFail":
        resp['message'] = u"<div>Last status: {0}</div>".format(store.status)
        resp['statusindicator'] = u"<h3 class='pull-right panel-title status-red'>" \
                                  u"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>" \
                                  u"<span class='sr-only'>Error:</span> Association fail - server not running?</h3>"
        resp['delbutton'] = u"<a class='btn btn-primary' href='{0}' role='button'>Delete</a>".format(
            reverse_lazy('dicomstore_delete', kwargs={'pk': scp_pk}))
        resp['startbutton'] = u"<a class='btn btn-success' href='{0}' role='button'>Start server</a>".format(
            reverse_lazy('run_store', kwargs={'pk': scp_pk}))
        resp['stopbutton'] = u""

    return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def q_update(request):
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import Count
    from remapp.models import DicomQuery

    resp = {}
    data = request.POST
    query_id = data.get('queryID')
    resp['queryID'] = query_id
    try:
        query = DicomQuery.objects.get(query_id=query_id)
    except ObjectDoesNotExist:
        resp['status'] = u'not complete'
        resp['message'] = u'<h4>Query {0} not yet started</h4>'.format(query_id)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if query.failed:
        resp['status'] = u'failed'
        resp['message'] ='<h4>Query Failed</h4> {0}'.format(query.message)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    study_rsp = query.dicomqrrspstudy_set.all()
    if not query.complete:
        modalities = study_rsp.values('modalities_in_study').annotate(count=Count('pk'))
        table = [u'<table class="table table-bordered"><tr><th>Modalities in study</th><th>Number of responses</th></tr>']
        for m in modalities:
            table.append(u'<tr><td>')
            if m['modalities_in_study']:
                table.append(u', '.join(json.loads(m['modalities_in_study'])))
            else:
                table.append(u'Unknown')
            table.append(u'</td><td>')
            table.append(str(m['count']))
            table.append(u'</tr></td>')
        table.append(u'</table>')
        tablestr = ''.join(table)
        resp['status'] = u'not complete'
        resp['message'] = u'<h4>{0}</h4><p>Responses so far:</p> {1}'.format(query.stage, tablestr)
    else:
        modalities = study_rsp.values('modality').annotate(count=Count('pk'))
        table = [u'<table class="table table-bordered"><tr><th>Modality</th><th>Number of responses</th></tr>']
        for m in modalities:
            table.append(u'<tr><td>')
            if m['modality']:
                table.append(m['modality'])
            else:
                table.append(u'Unknown - SR only study?')
            table.append(u'</td><td>')
            table.append(str(m['count']))
            table.append(u'</tr></td>')
        table.append(u'</table>')
        tablestr = u''.join(table)
        resp['status'] = u'complete'
        query_details_text = u"<div class='panel-group' id='accordion'>" \
                             u"<div class='panel panel-default'>" \
                             u"<div class='panel-heading'>  "\
                             u"<h4 class='panel-title'>" \
                             u"<a data-toggle='collapse' data-parent='#accordion' href='#query-details'>" \
                             u"Query details</h4>" \
                             u"</a></h4></div>" \
                             u"<div id='query-details' class='panel-collapse collapse'>" \
                             u"<div class='panel-body'>" \
                             u"<p>{0}</p></div></div></div></div>".format(query.stage)
        not_as_expected_help_text = u"<div class='panel-group' id='accordion'>" \
                                    u"<div class='panel panel-default'>" \
                                    u"<div class='panel-heading'>  "\
                                    u"<h4 class='panel-title'>" \
                                    u"<a data-toggle='collapse' data-parent='#accordion' href='#not-expected'>" \
                                    u"Not what you expected?</h4>" \
                                    u"</a></h4></div>" \
                                    u"<div id='not-expected' class='panel-collapse collapse'>" \
                                    u"<div class='panel-body'>" \
                                    u"<p>For DX and mammography, the query will look for Radiation Dose Structured " \
                                    u"Reports, or images if the RDSR is not available. For Fluoroscopy, RDSRs are " \
                                    u"required. For CT RDSRs are preferred, but Philips dose images can be used and " \
                                    u"for some scanners, particularly older Toshiba scanners that can't create RDSR " \
                                    u"OpenREM can process the data to create an RDSR to import.</p>" \
                                    u"<p>If you haven't got the results you expect, it may be that the imaging system" \
                                    u" is not creating RDSRs or not sending them to the PACS you are querying. In " \
                                    u"either case you will need to have the system reconfigured to create and/or send" \
                                    u" them. If it is a CT scanner that can't create an RDSR (it is too old), it is " \
                                    u"worth trying the 'Toshiba' option, but you will need to be using Orthanc and " \
                                    u"configure your scanner in the " \
                                    u"<a href='https://docs.openrem.org/en/{0}/netdicom-orthanc-config.html" \
                                    u"#guide-to-customising-orthanc-configuration' target='_blank'>" \
                                    u"toshiba_extractor_systems</a> list" \
                                    u". You will need to verify the resulting data to confirm accuracy.</p>" \
                                    u"</div></div></div></div>".format(remapp.__docs_version__)
        resp['message'] = u'<h4>Query complete - there are {1} studies we can move</h4> {0} {2} {3}'.format(
            tablestr, study_rsp.count(), query_details_text, not_as_expected_help_text)

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
            remove_duplicates = form.cleaned_data.get('duplicates_field')
            desc_exclude = form.cleaned_data.get('desc_exclude_field')
            desc_include = form.cleaned_data.get('desc_include_field')
            stationname_exclude = form.cleaned_data.get('stationname_exclude_field')
            stationname_include = form.cleaned_data.get('stationname_include_field')
            get_toshiba_images = form.cleaned_data.get('get_toshiba_images_field')
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
            if stationname_exclude:
                stationname_exc = map(unicode.lower, map(unicode.strip, stationname_exclude.split(',')))
            else:
                stationname_exc = None
            if stationname_include:
                stationname_inc = map(unicode.lower, map(unicode.strip, stationname_include.split(',')))
            else:
                stationname_inc = None

            filters = {
                'stationname_inc': stationname_inc,
                'stationname_exc': stationname_exc,
                'study_desc_inc': study_desc_inc,
                'study_desc_exc': study_desc_exc,
            }

            task = qrscu.delay(qr_scp_pk=rh_pk, store_scp_pk=store_pk, query_id=query_id, date_from=date_from,
                               date_until=date_until, modalities=modalities, inc_sr=inc_sr,
                               remove_duplicates=remove_duplicates, filters=filters,
                               get_toshiba_images=get_toshiba_images,
                               )

            resp = {}
            resp['message'] = u'Request created'
            resp['status'] = u'not complete'
            resp['queryID'] = query_id

            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            print u"Bother, form wasn't valid"
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
                {'form': form, 'admin': admin},
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
        messages.error(request, u"You are not in the importqrgroup - please contact your administrator")
        return redirect(reverse_lazy('home'))

    form = DicomQueryForm

    storestatus = {}
    stores = DicomStoreSCP.objects.all()
    for store in stores:
        echo = echoscu(scp_pk=store.pk, store_scp=True)
        if echo is "Success":
            storestatus[store.name] = u"<span class='glyphicon glyphicon-ok' aria-hidden='true'></span><span class='sr-only'>OK:</span> responding to DICOM echo"
        else:
            storestatus[store.name] = u"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span><span class='sr-only'>Error:</span> not responding to DICOM echo"

    qrstatus = {}
    qr = DicomRemoteQR.objects.all()
    for scp in qr:
        echo = echoscu(scp_pk=scp.pk, qr_scp=True)
        if echo is "Success":
            qrstatus[scp.name] = u"<span class='glyphicon glyphicon-ok' aria-hidden='true'></span><span class='sr-only'>OK:</span> responding to DICOM echo"
        else:
            qrstatus[scp.name] = u"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span><span class='sr-only'>Error:</span> not responding to DICOM echo"

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/dicomqr.html',
        {'form': form, 'storestatus': storestatus, 'qrstatus': qrstatus, 'admin': admin},
        context_instance=RequestContext(request)
    )

@csrf_exempt
@login_required
def r_start(request):
    from remapp.netdicom.qrscu import movescu
    resp = {}
    data = request.POST
    query_id = data.get('queryID')
    resp['queryID'] = query_id

    movescu.delay(query_id)

    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def r_update(request):
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import Count
    from remapp.models import DicomQuery

    resp = {}
    data = request.POST
    query_id = data.get('queryID')
    resp['queryID'] = query_id
    try:
        query = DicomQuery.objects.get(query_id=query_id)
    except ObjectDoesNotExist:
        resp['status'] = u'not complete'
        resp['message'] = u'<h4>Move request {0} not yet started</h4>'.format(query_id)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if query.failed:
        resp['status'] = u'failed'
        resp['message'] = u'<h4>Move request failed</h4> {0}'.format(query.message)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if not query.move_complete:
        resp['status'] = u'not complete'
        resp['message'] = u'<h4>{0}</h4>'.format(query.stage)
    else:
        resp['status'] = u'move complete'
        resp['message'] = u'<h4>Move request complete</h4>'

    return HttpResponse(json.dumps(resp), content_type='application/json')
