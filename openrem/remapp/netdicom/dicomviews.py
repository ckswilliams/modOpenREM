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
