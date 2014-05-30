import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def export_ct_csv(request):
    from django.template import RequestContext  
    from django.shortcuts import render_to_response
    from remapp.models import Exports
    
    exptsks = Exports.objects.all()

    if 'task_id' in request.session.keys() and request.session['task_id']:
        task_id = request.session['task_id']
    return render_to_response('remapp/exports.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def ct_csv(request):
    from remapp.exports.exportcsv import exportCT2excel
    from remapp.exports.exportcsv import getQueryFilters
    from urlparse import parse_qs
    
    postdata = json.loads(request.body)
    queryfilters = parse_qs(postdata['qfilters'], keep_blank_values=True)
    
    data = 'Fail'
    if request.is_ajax():
        job = exportCT2excel.delay(queryfilters)
        request.session['task_id'] = job.id
        data = job.id
    else:
        data = "Not ajax request!"
        
    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def poll_state(request):
    """ A view to report the progress to the user """
    from celery.result import AsyncResult
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
#            data = task.result or task.state
            data = task.result
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')
