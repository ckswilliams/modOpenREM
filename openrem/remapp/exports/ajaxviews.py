import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def do_CT_csv(request):
    from django.http import HttpResponse
    from remapp.exports.exportcsv import exportCT2excel
    from remapp.exports.exportcsv import getQueryFilters
    
    query_filters = getQueryFilters(request)
    job = exportCT2excel.delay(query_filters)
    request.session['task_id'] = job.id
    data = job.id
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
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)

    return HttpResponse(json_data, mimetype='application/json')
