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

Following two lines added so that sphinx autodocumentation works.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import ctypes
import threading
import time

NULL = 0

def ctype_async_raise(thread_obj, exception):
    found = False
    target_tid = 0
    for tid, tobj in threading._active.items():
        if tobj is thread_obj:
            found = True
            target_tid = tid
            break

    if not found:
        raise ValueError("Invalid thread object")

    ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid), ctypes.py_object(exception))
    # ref: http://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
    if ret == 0:
        raise ValueError("Invalid thread ID")
    elif ret > 1:
        # Huh? Why would we notify more than one threads?
        # Because we punch a hole into C level interpreter.
        # So it is better to clean up the mess.
        ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, NULL)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    print "Successfully set asynchronized exception for", target_tid

def run_store(store_pk):
    from remapp.netdicom.storescp import web_store
    try:
        web_store(store_pk=store_pk)
    finally:
        print "Exited"

@csrf_exempt
@login_required
def storescp(request, pk):
    from django.shortcuts import redirect

    if request.user.groups.filter(name="exportgroup") or request.user.groups.filter(name="admingroup"):
        t = threading.Thread(target=run_store, args=(pk,))
        t.daemon = True
        t.start()
        print "Thread ident is {0}".format(t.ident)

    return redirect('/openrem/admin/dicomsummary/')

