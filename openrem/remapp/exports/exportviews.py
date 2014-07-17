# Following two lines added so that sphinx autodocumentation works.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.settings'

import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@csrf_exempt
@login_required
def ctcsv1(request):
    """View to launch celery task to export CT studies to csv file

    :param request: Contains the database filtering parameters
    :type request: GET
    """
    from django.shortcuts import redirect
    from remapp.exports.exportcsv import exportCT2excel

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        job = exportCT2excel.delay(request.GET)

    return redirect('/openrem/export/')


@csrf_exempt
@login_required
def ctxlsx1(request):
    from django.shortcuts import redirect
    from remapp.exports.xlsx import ctxlsx

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        job = ctxlsx.delay(request.GET)
    
    return redirect('/openrem/export/')

@csrf_exempt
@login_required
def flcsv1(request):
    from django.shortcuts import redirect
    from remapp.exports.exportcsv import exportFL2excel

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        job = exportFL2excel.delay(request.GET)
    
    return redirect('/openrem/export/')

@csrf_exempt
@login_required
def mgcsv1(request):
    from django.shortcuts import redirect
    from remapp.exports.exportcsv import exportMG2excel

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        job = exportMG2excel.delay(request.GET)
    
    return redirect('/openrem/export/')

@csrf_exempt
@login_required
def mgnhsbsp(request):
    from django.shortcuts import redirect
    from remapp.exports.mg_csv_nhsbsp import mg_csv_nhsbsp

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        job = mg_csv_nhsbsp.delay(request.GET)
    
    return redirect('/openrem/export/')

@csrf_exempt
@login_required
def export(request):
    import pkg_resources # part of setuptools
    from django.template import RequestContext  
    from django.shortcuts import render_to_response
    from remapp.models import Exports
    from remapp.exports.exportcsv import exportCT2excel

    exptsks = Exports.objects.all().order_by('-export_date')
    
    current = exptsks.filter(status__contains = 'CURRENT')
    complete = exptsks.filter(status__contains = 'COMPLETE')
    
    try:
        vers = pkg_resources.require("openrem")[0].version
    except:
        vers = ''
    admin = {'openremversion' : vers}

    if request.user.groups.filter(name="exportgroup"):
        admin['exportperm'] = True
    if request.user.groups.filter(name="admingroup"):
        admin['adminperm'] = True


    if 'task_id' in request.session.keys() and request.session['task_id']:
        task_id = request.session['task_id']
    return render_to_response('remapp/exports.html', locals(), context_instance=RequestContext(request))


@login_required
def download(request, file_name):
    import mimetypes
    import os
    from django.core.servers.basehttp import FileWrapper
    from django.utils.encoding import smart_str
    from django.shortcuts import redirect
    from openrem.settings import MEDIA_ROOT

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        file_path = os.path.join(MEDIA_ROOT, file_name)
        file_wrapper = FileWrapper(file(file_path,'rb'))
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype )
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
        return response
    else:
        return redirect('/openrem/export/')
        
@csrf_exempt
@login_required
def deletefile(request):
    import os, sys
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    from django.contrib import messages
    from openrem.settings import MEDIA_ROOT
    from remapp.models import Exports
    from remapp.exports import exportviews
    
    
    for task in request.POST:
        export = Exports.objects.filter(task_id__exact = request.POST[task])
        file_path = os.path.join(MEDIA_ROOT, export[0].filename)
        try:
            os.remove(file_path)
            export.delete()
            messages.success(request, "Export file and database entry deleted successfully.")
        except OSError as e:
            messages.error(request, "Export file delete failed - please contact an administrator. Error({0}): {1}".format(e.errno, e.strerror))
        except:
            messages.error(request, "Unexpected error - please contact an administrator: {0}".format(sys.exc_info()[0]))
    
    return HttpResponseRedirect(reverse(exportviews.export))
