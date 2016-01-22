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
#
#    8/10/2014: DJP added new DX section and added DX to home page.
#    9/10/2014: DJP changed DX to CR
#
"""
..  module:: views.
    :synopsis: Module to render appropriate content according to request.

..  moduleauthor:: Ed McDonagh

"""
# from __future__ import unicode_literals
# Following two lines added so that sphinx autodocumentation works.
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import remapp
from remapp.models import GeneralStudyModuleAttr, create_user_profile

try:
    from numpy import *

    plotting = 1
except ImportError:
    plotting = 0


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/openrem/')


@login_required
def dx_summary_list_filter(request):
    from remapp.interface.mod_filters import dx_acq_filter
    from remapp.forms import DXChartOptionsForm
    from openremproject import settings

    if request.user.groups.filter(name='pidgroup'):
        pid = True
    else:
        pid = False

    f = dx_acq_filter(request.GET, pid=pid)

    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        userProfile = request.user.userprofile

    if userProfile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        userProfile.median_available = True
        userProfile.save()
        median_available = True
    else:
        userProfile.median_available = False
        userProfile.save()
        median_available = False

    # Obtain the chart options from the request
    chartOptionsForm = DXChartOptionsForm(request.GET)
    # check whether the form data is valid
    if chartOptionsForm.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            userProfile.plotCharts = chartOptionsForm.cleaned_data['plotCharts']
            userProfile.plotDXAcquisitionMeanDAP = chartOptionsForm.cleaned_data['plotDXAcquisitionMeanDAP']
            userProfile.plotDXAcquisitionFreq = chartOptionsForm.cleaned_data['plotDXAcquisitionFreq']
            userProfile.plotDXStudyMeanDAP = chartOptionsForm.cleaned_data['plotDXStudyMeanDAP']
            userProfile.plotDXStudyFreq = chartOptionsForm.cleaned_data['plotDXStudyFreq']
            userProfile.plotDXRequestMeanDAP = chartOptionsForm.cleaned_data['plotDXRequestMeanDAP']
            userProfile.plotDXRequestFreq = chartOptionsForm.cleaned_data['plotDXRequestFreq']
            userProfile.plotDXAcquisitionMeankVp = chartOptionsForm.cleaned_data['plotDXAcquisitionMeankVp']
            userProfile.plotDXAcquisitionMeanmAs = chartOptionsForm.cleaned_data['plotDXAcquisitionMeanmAs']
            userProfile.plotDXStudyPerDayAndHour = chartOptionsForm.cleaned_data['plotDXStudyPerDayAndHour']
            userProfile.plotDXAcquisitionMeankVpOverTime = chartOptionsForm.cleaned_data[
                'plotDXAcquisitionMeankVpOverTime']
            userProfile.plotDXAcquisitionMeanmAsOverTime = chartOptionsForm.cleaned_data[
                'plotDXAcquisitionMeanmAsOverTime']
            userProfile.plotDXAcquisitionMeanDAPOverTime = chartOptionsForm.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTime']
            userProfile.plotDXAcquisitionMeanDAPOverTimePeriod = chartOptionsForm.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTimePeriod']
            if median_available:
                userProfile.plotAverageChoice = chartOptionsForm.cleaned_data['plotMeanMedianOrBoth']
            userProfile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            formData = {'plotCharts': userProfile.plotCharts,
                        'plotDXAcquisitionMeanDAP': userProfile.plotDXAcquisitionMeanDAP,
                        'plotDXAcquisitionFreq': userProfile.plotDXAcquisitionFreq,
                        'plotDXStudyMeanDAP': userProfile.plotDXStudyMeanDAP,
                        'plotDXStudyFreq': userProfile.plotDXStudyFreq,
                        'plotDXRequestMeanDAP': userProfile.plotDXRequestMeanDAP,
                        'plotDXRequestFreq': userProfile.plotDXRequestFreq,
                        'plotDXAcquisitionMeankVp': userProfile.plotDXAcquisitionMeankVp,
                        'plotDXAcquisitionMeanmAs': userProfile.plotDXAcquisitionMeanmAs,
                        'plotDXStudyPerDayAndHour': userProfile.plotDXStudyPerDayAndHour,
                        'plotDXAcquisitionMeankVpOverTime': userProfile.plotDXAcquisitionMeankVpOverTime,
                        'plotDXAcquisitionMeanmAsOverTime': userProfile.plotDXAcquisitionMeanmAsOverTime,
                        'plotDXAcquisitionMeanDAPOverTime': userProfile.plotDXAcquisitionMeanDAPOverTime,
                        'plotDXAcquisitionMeanDAPOverTimePeriod': userProfile.plotDXAcquisitionMeanDAPOverTimePeriod,
                        'plotMeanMedianOrBoth': userProfile.plotAverageChoice}
            chartOptionsForm = DXChartOptionsForm(formData)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    returnStructure = {'filter': f, 'admin': admin, 'chartOptionsForm': chartOptionsForm}

    return render_to_response(
        'remapp/dxfiltered.html',
        returnStructure,
        context_instance=RequestContext(request)
    )


@login_required
def dx_summary_chart_data(request):
    from remapp.interface.mod_filters import DXSummaryListFilter
    from django.db.models import Q
    from openremproject import settings
    from django.http import JsonResponse

    requestResults = request.GET

    if requestResults.get('acquisitionhist'):
        filters = {}
        if requestResults.get('acquisition_protocol'):
            filters['projectionxrayradiationdose__irradeventxraydata__acquisition_protocol'] = requestResults.get(
                'acquisition_protocol')
        if requestResults.get('acquisition_dap_min'):
            filters['projectionxrayradiationdose__irradeventxraydata__dose_area_product__gte'] = requestResults.get(
                'acquisition_dap_min')
        if requestResults.get('acquisition_dap_max'):
            filters['projectionxrayradiationdose__irradeventxraydata__dose_area_product__lte'] = requestResults.get(
                'acquisition_dap_max')
        if requestResults.get('acquisition_kvp_min'):
            filters[
                'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__kvp__kvp__gte'] = requestResults.get(
                'acquisition_kvp_min')
        if requestResults.get('acquisition_kvp_max'):
            filters[
                'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__kvp__kvp__lte'] = requestResults.get(
                'acquisition_kvp_max')
        if requestResults.get('acquisition_mas_min'):
            filters[
                'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__exposure__exposure__gte'] = requestResults.get(
                'acquisition_mas_min')
        if requestResults.get('acquisition_mas_max'):
            filters[
                'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__exposure__exposure__lte'] = requestResults.get(
                'acquisition_mas_max')
        if requestResults.get('study_description'):
            filters['study_description__icontains'] = requestResults.get('study_description')
        if requestResults.get('requested_procedure'):
            filters['requested_procedure_code_meaning__icontains'] = requestResults.get('requested_procedure')

    else:
        filters = {}
        if requestResults.get('study_description'):
            filters['study_description__icontains'] = requestResults.get('study_description')
        if requestResults.get('acquisition_protocol'):
            filters[
                'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol__icontains'] = requestResults.get(
                'acquisition_protocol')
        if requestResults.get('acquisition_dap_min'):
            filters['projectionxrayradiationdose__irradeventxraydata__dose_area_product__gte'] = requestResults.get(
                'acquisition_dap_min')
        if requestResults.get('acquisition_dap_max'):
            filters['projectionxrayradiationdose__irradeventxraydata__dose_area_product__lte'] = requestResults.get(
                'acquisition_dap_max')
        if requestResults.get('requested_procedure'):
            filters['requested_procedure_code_meaning__icontains'] = requestResults.get('requested_procedure')

    if requestResults.get('accession_number'):
        filters['accession_number'] = requestResults.get('accession_number')
    if requestResults.get('date_after'):
        filters['study_date__gte'] = requestResults.get('date_after')
    if requestResults.get('date_before'):
        filters['study_date__lte'] = requestResults.get('date_before')
    if requestResults.get('institution_name'):
        filters['generalequipmentmoduleattr__institution_name'] = requestResults.get('institution_name')
    if requestResults.get('manufacturer'):
        filters['generalequipmentmoduleattr__manufacturer'] = requestResults.get('manufacturer')
    if requestResults.get('model_name'):
        filters['generalequipmentmoduleattr__manufacturer_model_name'] = requestResults.get('model_name')
    if requestResults.get('patient_age_max'):
        filters['patientstudymoduleattr__patient_age_decimal__lte'] = requestResults.get('patient_age_max')
    if requestResults.get('patient_age_min'):
        filters['patientstudymoduleattr__patient_age_decimal__gte'] = requestResults.get('patient_age_min')
    if requestResults.get('station_name'):
        filters['generalequipmentmoduleattr__station_name'] = requestResults.get('station_name')
    if requestResults.get('display_name'):
        filters['generalequipmentmoduleattr__unique_equipment_name__display_name'] = requestResults.get('display_name')

    f = DXSummaryListFilter(requestResults, queryset=GeneralStudyModuleAttr.objects.filter(
        Q(modality_type__exact='DX') | Q(modality_type__exact='CR'),
        **filters
    ).order_by().distinct())

    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        userProfile = request.user.userprofile

    if userProfile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        userProfile.median_available = True
        userProfile.save()
        median_available = True
    else:
        userProfile.median_available = False
        userProfile.save()
        median_available = False

    returnStructure = \
        dx_plot_calculations(f, userProfile.plotDXAcquisitionMeanDAP, userProfile.plotDXAcquisitionFreq,
                             userProfile.plotDXStudyMeanDAP, userProfile.plotDXStudyFreq,
                             userProfile.plotDXRequestMeanDAP, userProfile.plotDXRequestFreq,
                             userProfile.plotDXAcquisitionMeankVpOverTime, userProfile.plotDXAcquisitionMeanmAsOverTime,
                             userProfile.plotDXAcquisitionMeanDAPOverTime, userProfile.plotDXAcquisitionMeanDAPOverTimePeriod,
                             userProfile.plotDXAcquisitionMeankVp, userProfile.plotDXAcquisitionMeanmAs,
                             userProfile.plotDXStudyPerDayAndHour, requestResults,
                             median_available, userProfile.plotAverageChoice, userProfile.plotSeriesPerSystem,
                             userProfile.plotHistogramBins)

    return JsonResponse(returnStructure, safe=False)


def dx_plot_calculations(f, plotDXAcquisitionMeanDAP, plotDXAcquisitionFreq,
                         plotDXStudyMeanDAP, plotDXStudyFreq,
                         plotDXRequestMeanDAP, plotDXRequestFreq,
                         plotDXAcquisitionMeankVpOverTime, plotDXAcquisitionMeanmAsOverTime,
                         plotDXAcquisitionMeanDAPOverTime, plotDXAcquisitionMeanDAPOverTimePeriod,
                         plotDXAcquisitionMeankVp, plotDXAcquisitionMeanmAs,
                         plotDXStudyPerDayAndHour, requestResults,
                         median_available, plotAverageChoice, plotSeriesPerSystems, plotHistogramBins):
    from remapp.models import IrradEventXRayData, Median
    from django.db.models import Avg, Count, Min, Max, FloatField
    import datetime, qsstats
    if plotting:
        import numpy as np

    returnStructure = {}

    expInclude = [o.study_instance_uid for o in f]
    acquisitionFilters = {
        'projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__in': expInclude}
    if requestResults.get('acquisition_dap_max'):
        acquisitionFilters['dose_area_product__lte'] = requestResults.get('acquisition_dap_max')
    if requestResults.get('acquisition_dap_min'):
        acquisitionFilters['dose_area_product__gte'] = requestResults.get('acquisition_dap_min')
    if requestResults.get('acquisition_protocol'):
        acquisitionFilters['acquisition_protocol__icontains'] = requestResults.get('acquisition_protocol')
    if requestResults.get('acquisition_kvp_min'):
        acquisitionFilters['irradeventxraysourcedata__kvp__kvp__gte'] = requestResults.get('acquisition_kvp_min')
    if requestResults.get('acquisition_kvp_max'):
        acquisitionFilters['irradeventxraysourcedata__kvp__kvp__lte'] = requestResults.get('acquisition_kvp_max')
    if requestResults.get('acquisition_mas_min'):
        acquisitionFilters['irradeventxraysourcedata__exposure__exposure__gte'] = requestResults.get(
            'acquisition_mas_min')
    if requestResults.get('acquisition_mas_max'):
        acquisitionFilters['irradeventxraysourcedata__exposure__exposure__lte'] = requestResults.get(
            'acquisition_mas_max')

    acquisition_events = IrradEventXRayData.objects.exclude(
        dose_area_product__isnull=True
    ).filter(
        **acquisitionFilters
    )
    acquisition_names = list(acquisition_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))
    returnStructure['acquisition_names'] = acquisition_names

    study_events = GeneralStudyModuleAttr.objects.exclude(
        projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
    ).exclude(
        study_description__isnull=True
    ).filter(
        study_instance_uid__in=expInclude
    )
    study_names = list(study_events.values_list('study_description', flat=True).distinct().order_by('study_description'))
    returnStructure['study_names'] = study_names

    request_events = GeneralStudyModuleAttr.objects.exclude(
        projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
    ).exclude(
        requested_procedure_code_meaning__isnull=True
    ).filter(
        study_instance_uid__in=expInclude
    )
    request_names = list(request_events.values_list('requested_procedure_code_meaning', flat=True).distinct().order_by('requested_procedure_code_meaning'))
    returnStructure['request_names'] = request_names

    if plotDXAcquisitionMeankVpOverTime or plotDXAcquisitionMeankVp:
        acquisition_kvp_events = IrradEventXRayData.objects.exclude(
            irradeventxraysourcedata__kvp__kvp__isnull=True
        ).filter(
            **acquisitionFilters
        )
        acquisition_kvp_names = list(acquisition_kvp_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))
        returnStructure['acquisition_kvp_names'] = acquisition_kvp_names

    if plotDXAcquisitionMeanmAsOverTime or plotDXAcquisitionMeanmAs:
        acquisition_mas_events = IrradEventXRayData.objects.exclude(
            irradeventxraysourcedata__exposure__exposure__isnull=True
        ).filter(
            **acquisitionFilters
        )
        acquisition_mas_names = list(acquisition_mas_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))
        returnStructure['acquisition_mas_names'] = acquisition_mas_names

    if plotDXAcquisitionMeanDAP:
        if median_available and plotAverageChoice == 'both':
            acquisitionSummary = acquisition_events.values('acquisition_protocol').annotate(
                mean_dap=Avg('dose_area_product') * 1000000,
                median_dap=Median('dose_area_product') / 10000,
                num_acq=Count('dose_area_product')) \
                .order_by('acquisition_protocol')
        elif median_available and plotAverageChoice == 'median':
            acquisitionSummary = acquisition_events.values('acquisition_protocol').annotate(
                median_dap=Median('dose_area_product') / 10000,
                num_acq=Count('dose_area_product')) \
                .order_by('acquisition_protocol')
        else:
            acquisitionSummary = acquisition_events.values('acquisition_protocol').annotate(
                mean_dap=Avg('dose_area_product') * 1000000,
                num_acq=Count('dose_area_product')) \
                .order_by('acquisition_protocol')
        acquisitionHistogramData = [[None for i in xrange(2)] for i in xrange(len(acquisitionSummary))]
        returnStructure['acquisitionSummary'] = list(acquisitionSummary)

    elif plotDXAcquisitionFreq:
        acquisitionSummary = acquisition_events.values('acquisition_protocol').annotate(
                num_acq=Count('dose_area_product')).order_by('acquisition_protocol')
        returnStructure['acquisitionSummary'] = list(acquisitionSummary)

    if plotDXRequestMeanDAP or plotDXRequestFreq:
        if plotSeriesPerSystems and plotDXRequestMeanDAP:
            requestSystemList = list(request_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            requestSystemList = ['All systems']
        returnStructure['requestSystemList'] = list(requestSystemList)

        if median_available and plotAverageChoice == 'both':
            requestSummary = []
            if plotSeriesPerSystems and plotDXRequestMeanDAP:
                for system in requestSystemList:
                    requestSummary.append(request_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                            'requested_procedure_code_meaning').distinct().annotate(
                            mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                            median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                            num_req=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            elif plotDXRequestMeanDAP:
                requestSummary.append(request_events.values(
                        'requested_procedure_code_meaning').distinct().annotate(
                        mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num_req=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            else:
                requestSummary.append(request_events.values(
                        'requested_procedure_code_meaning').distinct().annotate(
                        num_req=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        elif median_available and plotAverageChoice == 'median':
            requestSummary = []
            if plotSeriesPerSystems and plotDXRequestMeanDAP:
                for system in requestSystemList:
                    requestSummary.append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('requested_procedure_code_meaning').distinct().annotate(
                        median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num_req=Count('requested_procedure_code_meaning')) \
                        .order_by('requested_procedure_code_meaning'))
            elif plotDXRequestMeanDAP:
                requestSummary.append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                    num_req=Count('requested_procedure_code_meaning')) \
                    .order_by('requested_procedure_code_meaning'))
            else:
                requestSummary.append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    num_req=Count('requested_procedure_code_meaning')) \
                    .order_by('requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        else:
            requestSummary = []
            if plotSeriesPerSystems and plotDXRequestMeanDAP:
                for system in requestSystemList:
                    requestSummary.append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('requested_procedure_code_meaning').distinct().annotate(
                        mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        num_req=Count('requested_procedure_code_meaning')) \
                        .order_by('requested_procedure_code_meaning'))
            elif plotDXRequestMeanDAP:
                    requestSummary.append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                        mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        num_req=Count('requested_procedure_code_meaning')) \
                        .order_by('requested_procedure_code_meaning'))
            else:
                    requestSummary.append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                        num_req=Count('requested_procedure_code_meaning')) \
                        .order_by('requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        # Fill in default values where data for a requested procedure is missing for any of the systems
        if plotSeriesPerSystems and plotDXRequestMeanDAP:
            for index in range(len(requestSystemList)):
                missing_request_names = list(set(request_names) - set([d['requested_procedure_code_meaning'] for d in requestSummary[index]]))
                for name in missing_request_names:
                    if median_available and plotAverageChoice == 'both':
                        (requestSummary[index]).append({'median_dap': 0, 'mean_dap': 0,'requested_procedure_code_meaning':name, 'num_req': 0})
                    elif median_available and plotAverageChoice == 'median':
                        (requestSummary[index]).append({'median_dap': 0, 'requested_procedure_code_meaning':name, 'num_req': 0})
                    else:
                        (requestSummary[index]).append({'mean_dap': 0,'requested_procedure_code_meaning':name, 'num_req': 0})
                # Rearrange the list into the same order as request_names
                requestSummaryTemp = []
                for request_name in request_names:
                    requestSummaryTemp.append(filter(lambda item: item['requested_procedure_code_meaning'] == request_name, requestSummary[index] )[0])
                requestSummary[index] = requestSummaryTemp

        returnStructure['requestSummary'] = list(requestSummary)

    if plotDXRequestMeanDAP:
        requestHistogramData = [[[None for k in xrange(2)] for j in xrange(len(request_names))] for i in xrange(len(requestSystemList))]

        requestRanges = request_events.values('requested_procedure_code_meaning').distinct().annotate(
                min_dap=Min('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField()),
                max_dap=Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField())).order_by(
                'requested_procedure_code_meaning')

        for sys_idx, system in enumerate(requestSystemList):
            for req_idx, request_name in enumerate(request_names):
                if plotSeriesPerSystems:
                    subqs = request_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            requested_procedure_code_meaning=request_name)
                else:
                    subqs = request_events.filter(requested_procedure_code_meaning=request_name)

                dapValues = subqs.values_list(
                        'projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
                        flat=True)
                requestHistogramData[sys_idx][req_idx][0], requestHistogramData[sys_idx][req_idx][1] = np.histogram([float(x) for x in dapValues], bins=plotHistogramBins, range=requestRanges.filter(requested_procedure_code_meaning=request_name).values_list('min_dap', 'max_dap')[0])
                requestHistogramData[sys_idx][req_idx][0] = requestHistogramData[sys_idx][req_idx][0].tolist()
                requestHistogramData[sys_idx][req_idx][1] = (requestHistogramData[sys_idx][req_idx][1] * 1000000).tolist()

        returnStructure['requestHistogramData'] = requestHistogramData

    if plotDXStudyMeanDAP:
        if median_available and plotAverageChoice == 'both':
            studySummary = study_events.values('study_description').distinct().annotate(
                mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                num_stu=Count('study_description')) \
                .order_by('study_description')
        elif median_available and plotAverageChoice == 'median':
            studySummary = study_events.values('study_description').distinct().annotate(
                median_dap=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                num_stu=Count('study_description')) \
                .order_by('study_description')
        else:
            studySummary = study_events.values('study_description').distinct().annotate(
                mean_dap=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                num_stu=Count('study_description')) \
                .order_by('study_description')

        returnStructure['studySummary'] = list(studySummary)
        studyHistogramData = [[None for i in xrange(2)] for i in xrange(len(studySummary))]

    elif plotDXStudyFreq:
        studySummary = study_events.values('study_description').distinct().annotate(
                num_stu=Count('study_description')).order_by('study_description')
        returnStructure['studySummary'] = list(studySummary)

    if plotDXAcquisitionMeankVp:
        if median_available and plotAverageChoice == 'both':
            acquisitionkVpSummary = acquisition_kvp_events.values('acquisition_protocol').annotate(
                mean_kVp=Avg('irradeventxraysourcedata__kvp__kvp'),
                median_kVp=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')
        elif median_available and plotAverageChoice == 'median':
            acquisitionkVpSummary = acquisition_kvp_events.values('acquisition_protocol').annotate(
                median_kVp=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')
        else:
            acquisitionkVpSummary = acquisition_kvp_events.values('acquisition_protocol').annotate(
                mean_kVp=Avg('irradeventxraysourcedata__kvp__kvp'),
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')

        returnStructure['acquisitionkVpSummary'] = list(acquisitionkVpSummary)

        acquisitionHistogramkVpData = [[None for i in xrange(2)] for i in xrange(len(acquisitionkVpSummary))]

    if plotDXAcquisitionMeanmAs:
        if median_available and plotAverageChoice == 'both':
            acquisitionmAsSummary = acquisition_mas_events.values('acquisition_protocol').annotate(
                mean_mAs=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                median_mAs=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')
        elif median_available and plotAverageChoice == 'median':
            acquisitionmAsSummary = acquisition_mas_events.values('acquisition_protocol').annotate(
                median_mAs=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')
        else:
            acquisitionmAsSummary = acquisition_mas_events.values('acquisition_protocol').annotate(
                mean_mAs=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                num_acq=Count('acquisition_protocol')).order_by('acquisition_protocol')

        returnStructure['acquisitionmAsSummary'] = list(acquisitionmAsSummary)

        acquisitionHistogrammAsData = [[None for i in xrange(2)] for i in xrange(len(acquisitionmAsSummary))]

    if plotDXAcquisitionMeankVpOverTime or plotDXAcquisitionMeanmAsOverTime or plotDXAcquisitionMeanDAPOverTime:
        startDate = f.qs.aggregate(Min('study_date')).get('study_date__min')
        today = datetime.date.today()

        if plotDXAcquisitionMeankVpOverTime:
            if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                acquisitionMediankVpoverTime = [None] * len(acquisition_kvp_names)
            if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                acquisitionMeankVpoverTime = [None] * len(acquisition_kvp_names)

        if plotDXAcquisitionMeanmAsOverTime:
            if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                acquisitionMedianmAsoverTime = [None] * len(acquisition_mas_names)
            if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                acquisitionMeanmAsoverTime = [None] * len(acquisition_mas_names)

        if plotDXAcquisitionMeanDAPOverTime:
            if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                acquisitionMedianDAPoverTime = [None] * len(acquisition_names)
            if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                acquisitionMeanDAPoverTime = [None] * len(acquisition_names)

    if plotDXAcquisitionMeanDAP or plotDXAcquisitionMeanDAPOverTime:
        for idx, protocol in enumerate(acquisition_names):
            subqs = acquisition_events.filter(acquisition_protocol__exact=protocol)

            if plotDXAcquisitionMeanDAP:
                # Required for mean DAP per acquisition plot
                dapValues = subqs.values_list('dose_area_product', flat=True)
                acquisitionHistogramData[idx][0], acquisitionHistogramData[idx][1] = np.histogram(
                    [float(x) * 1000000 for x in dapValues], bins=plotHistogramBins)
                acquisitionHistogramData[idx][0] = acquisitionHistogramData[idx][0].tolist()
                acquisitionHistogramData[idx][1] = acquisitionHistogramData[idx][1].tolist()
                returnStructure['acquisitionHistogramData'] = acquisitionHistogramData

            if plotDXAcquisitionMeanDAPOverTime:
                # Required for mean DAP over time
                if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                    qss = qsstats.QuerySetStats(subqs, 'date_time_started',
                                                aggregate=Avg('dose_area_product') * 1000000)
                    acquisitionMeanDAPoverTime[idx] = qss.time_series(startDate, today,
                                                                      interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMeanDAPoverTime'] = acquisitionMeanDAPoverTime
                if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                    qss = qsstats.QuerySetStats(subqs, 'date_time_started',
                                                aggregate=Median('dose_area_product') / 10000)
                    acquisitionMedianDAPoverTime[idx] = qss.time_series(startDate, today,
                                                                        interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMedianDAPoverTime'] = acquisitionMedianDAPoverTime

    if plotDXStudyMeanDAP:
        for idx, study in enumerate(study_names):
            subqs = study_events.filter(study_description__exact=study)
            dapValues = subqs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', flat=True)
            studyHistogramData[idx][0], studyHistogramData[idx][1] = np.histogram(
                [float(x) * 1000000 for x in dapValues], bins=plotHistogramBins)
            studyHistogramData[idx][0] = studyHistogramData[idx][0].tolist()
            studyHistogramData[idx][1] = studyHistogramData[idx][1].tolist()
            returnStructure['studyHistogramData'] = studyHistogramData

    if plotDXAcquisitionMeankVp or plotDXAcquisitionMeankVpOverTime:
        for idx, protocol in enumerate(acquisition_kvp_names):
            subqskvp = acquisition_kvp_events.filter(acquisition_protocol=protocol)

            if plotDXAcquisitionMeankVp:
                # Required for mean kVp per acquisition plot
                kVpValues = subqskvp.values_list('irradeventxraysourcedata__kvp__kvp', flat=True)
                acquisitionHistogramkVpData[idx][0], acquisitionHistogramkVpData[idx][1] = np.histogram(
                    [float(x) for x in kVpValues], bins=plotHistogramBins)
                acquisitionHistogramkVpData[idx][0] = acquisitionHistogramkVpData[idx][0].tolist()
                acquisitionHistogramkVpData[idx][1] = acquisitionHistogramkVpData[idx][1].tolist()
                returnStructure['acquisitionHistogramkVpData'] = acquisitionHistogramkVpData

            if plotDXAcquisitionMeankVpOverTime:
                # Required for mean kVp over time
                if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                    qss = qsstats.QuerySetStats(subqskvp, 'date_time_started',
                                                aggregate=Avg('irradeventxraysourcedata__kvp__kvp'))
                    acquisitionMeankVpoverTime[idx] = qss.time_series(startDate, today,
                                                                      interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMeankVpoverTime'] = acquisitionMeankVpoverTime
                if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                    qss = qsstats.QuerySetStats(subqskvp, 'date_time_started',
                                                aggregate=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000)
                    acquisitionMediankVpoverTime[idx] = qss.time_series(startDate, today,
                                                                        interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMediankVpoverTime'] = acquisitionMediankVpoverTime

    if plotDXAcquisitionMeanmAs or plotDXAcquisitionMeanmAsOverTime:
        for idx, protocol in enumerate(acquisition_mas_names):
            subqsmas = acquisition_mas_events.filter(acquisition_protocol=protocol)

            if plotDXAcquisitionMeanmAs:
                # Required for mean mAs per acquisition plot
                uAsValues = subqsmas.values_list('irradeventxraysourcedata__exposure__exposure', flat=True)
                acquisitionHistogrammAsData[idx][0], acquisitionHistogrammAsData[idx][1] = np.histogram(
                    [float(x) / 1000 for x in uAsValues], bins=plotHistogramBins)
                acquisitionHistogrammAsData[idx][0] = acquisitionHistogrammAsData[idx][0].tolist()
                acquisitionHistogrammAsData[idx][1] = acquisitionHistogrammAsData[idx][1].tolist()
                returnStructure['acquisitionHistogrammAsData'] = acquisitionHistogrammAsData

            if plotDXAcquisitionMeanmAsOverTime:
                # Required for mean DAP over time
                if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                    qss = qsstats.QuerySetStats(subqsmas, 'date_time_started',
                                                aggregate=Avg('irradeventxraysourcedata__exposure__exposure') / 1000)
                    acquisitionMeanmAsoverTime[idx] = qss.time_series(startDate, today,
                                                                      interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMeanmAsoverTime'] = acquisitionMeanmAsoverTime
                if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                    qss = qsstats.QuerySetStats(subqsmas, 'date_time_started', aggregate=Median(
                        'irradeventxraysourcedata__exposure__exposure') / 10000000000000)
                    acquisitionMedianmAsoverTime[idx] = qss.time_series(startDate, today,
                                                                        interval=plotDXAcquisitionMeanDAPOverTimePeriod)
                    returnStructure['acquisitionMedianmAsoverTime'] = acquisitionMedianmAsoverTime

    if plotDXStudyPerDayAndHour:
        # Required for studies per weekday and studies per hour in each weekday plot
        studiesPerHourInWeekdays = [[0 for x in range(24)] for x in range(7)]
        for day in range(7):
            studyTimesOnThisWeekday = f.qs.filter(study_date__week_day=day + 1).values('study_workload_chart_time')
            if studyTimesOnThisWeekday:
                qss = qsstats.QuerySetStats(studyTimesOnThisWeekday, 'study_workload_chart_time')
                hourlyBreakdown = qss.time_series(datetime.datetime(1900, 1, 1, 0, 0),
                                                  datetime.datetime(1900, 1, 1, 23, 59), interval='hours')
                for hour in range(24):
                    studiesPerHourInWeekdays[day][hour] = hourlyBreakdown[hour][1]
        returnStructure['studiesPerHourInWeekdays'] = studiesPerHourInWeekdays

    return returnStructure


@login_required
def dx_detail_view(request, pk=None):
    """Detail view for a DX study
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except:
        messages.error(request, 'That study was not found')
        return redirect('/openrem/dx/')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/dxdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def rf_summary_list_filter(request):
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid

    if request.user.groups.filter(name='pidgroup'):
        f = RFFilterPlusPid(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF'))
    else:
        f = RFSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/rffiltered.html',
        {'filter': f, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def rf_detail_view(request, pk=None):
    """Detail view for an RF study
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except:
        messages.error(request, 'That study was not found')
        return redirect('/openrem/rf/')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/rfdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def ct_summary_list_filter(request):
    from remapp.interface.mod_filters import ct_acq_filter
    from remapp.forms import CTChartOptionsForm
    from openremproject import settings

    if request.user.groups.filter(name='pidgroup'):
        pid = True
    else:
        pid = False

    f = ct_acq_filter(request.GET, pid=pid)

    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        userProfile = request.user.userprofile

    if userProfile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        userProfile.median_available = True
        userProfile.save()
        median_available = True
    else:
        userProfile.median_available = False
        userProfile.save()
        median_available = False

    # Obtain the chart options from the request
    chartOptionsForm = CTChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chartOptionsForm.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            userProfile.plotCharts = chartOptionsForm.cleaned_data['plotCharts']
            userProfile.plotCTAcquisitionMeanDLP = chartOptionsForm.cleaned_data['plotCTAcquisitionMeanDLP']
            userProfile.plotCTAcquisitionMeanCTDI = chartOptionsForm.cleaned_data['plotCTAcquisitionMeanCTDI']
            userProfile.plotCTAcquisitionFreq = chartOptionsForm.cleaned_data['plotCTAcquisitionFreq']
            userProfile.plotCTStudyMeanDLP = chartOptionsForm.cleaned_data['plotCTStudyMeanDLP']
            userProfile.plotCTStudyFreq = chartOptionsForm.cleaned_data['plotCTStudyFreq']
            userProfile.plotCTRequestMeanDLP = chartOptionsForm.cleaned_data['plotCTRequestMeanDLP']
            userProfile.plotCTRequestFreq = chartOptionsForm.cleaned_data['plotCTRequestFreq']
            userProfile.plotCTStudyPerDayAndHour = chartOptionsForm.cleaned_data['plotCTStudyPerDayAndHour']
            userProfile.plotCTStudyMeanDLPOverTime = chartOptionsForm.cleaned_data['plotCTStudyMeanDLPOverTime']
            userProfile.plotCTStudyMeanDLPOverTimePeriod = chartOptionsForm.cleaned_data[
                'plotCTStudyMeanDLPOverTimePeriod']
            if median_available:
                userProfile.plotAverageChoice = chartOptionsForm.cleaned_data['plotMeanMedianOrBoth']
            userProfile.save()

        else:
            formData = {'plotCharts': userProfile.plotCharts,
                        'plotCTAcquisitionMeanDLP': userProfile.plotCTAcquisitionMeanDLP,
                        'plotCTAcquisitionMeanCTDI': userProfile.plotCTAcquisitionMeanCTDI,
                        'plotCTAcquisitionFreq': userProfile.plotCTAcquisitionFreq,
                        'plotCTStudyMeanDLP': userProfile.plotCTStudyMeanDLP,
                        'plotCTStudyFreq': userProfile.plotCTStudyFreq,
                        'plotCTRequestMeanDLP': userProfile.plotCTRequestMeanDLP,
                        'plotCTRequestFreq': userProfile.plotCTRequestFreq,
                        'plotCTStudyPerDayAndHour': userProfile.plotCTStudyPerDayAndHour,
                        'plotCTStudyMeanDLPOverTime': userProfile.plotCTStudyMeanDLPOverTime,
                        'plotCTStudyMeanDLPOverTimePeriod': userProfile.plotCTStudyMeanDLPOverTimePeriod,
                        'plotMeanMedianOrBoth': userProfile.plotAverageChoice}
            chartOptionsForm = CTChartOptionsForm(formData)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    returnStructure = {'filter': f, 'admin': admin, 'chartOptionsForm': chartOptionsForm}

    return render_to_response(
        'remapp/ctfiltered.html',
        returnStructure,
        context_instance=RequestContext(request)
    )


@login_required
def ct_summary_chart_data(request):
    from remapp.interface.mod_filters import CTSummaryListFilter, CTFilterPlusPid
    from openremproject import settings
    from django.http import JsonResponse

    requestResults = request.GET

    if request.user.groups.filter(name='pidgroup'):
        f = CTFilterPlusPid(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='CT').order_by().distinct())
    else:
        f = CTSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='CT').order_by().distinct())

    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        userProfile = request.user.userprofile

    if userProfile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        userProfile.median_available = True
        userProfile.save()
        median_available = True
    else:
        userProfile.median_available = False
        userProfile.save()
        median_available = False

    returnStructure =\
        ct_plot_calculations(f, userProfile.plotCTAcquisitionFreq, userProfile.plotCTAcquisitionMeanCTDI, userProfile.plotCTAcquisitionMeanDLP,
                             userProfile.plotCTRequestFreq, userProfile.plotCTRequestMeanDLP, userProfile.plotCTStudyFreq, userProfile.plotCTStudyMeanDLP,
                             userProfile.plotCTStudyMeanDLPOverTime, userProfile.plotCTStudyMeanDLPOverTimePeriod, userProfile.plotCTStudyPerDayAndHour,
                             requestResults, median_available, userProfile.plotAverageChoice, userProfile.plotSeriesPerSystem, userProfile.plotHistogramBins)

    return JsonResponse(returnStructure, safe=False)


def ct_plot_calculations(f, plotCTAcquisitionFreq, plotCTAcquisitionMeanCTDI, plotCTAcquisitionMeanDLP,
                         plotCTRequestFreq, plotCTRequestMeanDLP, plotCTStudyFreq, plotCTStudyMeanDLP,
                         plotCTStudyMeanDLPOverTime, plotCTStudyMeanDLPOverTimePeriod, plotCTStudyPerDayAndHour,
                         requestResults, median_available, plotAverageChoice, plotSeriesPerSystems, plotHistogramBins):
    from django.db.models import Q, Avg, Count, Min, Max, FloatField
    import datetime, qsstats
    from remapp.models import CtIrradiationEventData, Median
    if plotting:
        import numpy as np

    returnStructure = {}

    # Need to exclude all Constant Angle Acquisitions when calculating data for acquisition plots, as Philips
    # Ingenuity uses same name for scan projection radiographs as the corresponding CT acquisition. Also exclude any
    # with null DLP values.
    expInclude = [o.study_instance_uid for o in f]
    acquisitionFilters = {'ct_radiation_dose__general_study_module_attributes__study_instance_uid__in': expInclude}
    if requestResults.get('acquisition_dlp_max'):
        acquisitionFilters['dlp__lte'] = requestResults.get('acquisition_dlp_max')
    if requestResults.get('acquisition_dlp_min'):
        acquisitionFilters['dlp__gte'] = requestResults.get('acquisition_dlp_min')
    if requestResults.get('acquisition_protocol'):
        acquisitionFilters['acquisition_protocol__icontains'] = requestResults.get('acquisition_protocol')
    if requestResults.get('acquisition_ctdi_max'):
        acquisitionFilters['mean_ctdivol__lte'] = requestResults.get('acquisition_ctdi_max')
    if requestResults.get('acquisition_ctdi_min'):
        acquisitionFilters['mean_ctdivol__gte'] = requestResults.get('acquisition_ctdi_min')

    acquisition_events = CtIrradiationEventData.objects.exclude(
        ct_acquisition_type__code_meaning__exact=u'Constant Angle Acquisition'
    ).exclude(
        dlp__isnull=True
    ).filter(
        **acquisitionFilters
    )

    study_events = GeneralStudyModuleAttr.objects.exclude(
        ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
    ).exclude(
        study_description__isnull=True
    ).filter(
        study_instance_uid__in=expInclude
    )

    request_events = GeneralStudyModuleAttr.objects.exclude(
        ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
    ).exclude(
        requested_procedure_code_meaning__isnull=True
    ).filter(
        study_instance_uid__in=expInclude
    )

    if plotCTAcquisitionMeanDLP or plotCTAcquisitionMeanCTDI or plotCTAcquisitionFreq:
        # Required for mean DLP per acquisition plot
        if plotCTAcquisitionMeanCTDI:
            if median_available and plotAverageChoice == 'both':
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(mean_ctdi=Avg('mean_ctdivol'),
                                                                median_ctdi=Median('mean_ctdivol') / 10000000000,
                                                                mean_dlp=Avg('dlp'),
                                                                median_dlp=Median('dlp') / 10000000000,
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')
            elif median_available and plotAverageChoice == 'median':
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(median_ctdi=Median('mean_ctdivol') / 10000000000,
                                                                median_dlp=Median('dlp') / 10000000000,
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')
            else:
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(mean_ctdi=Avg('mean_ctdivol'),
                                                                mean_dlp=Avg('dlp'),
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')
            acquisitionHistogramDataCTDI = [[None for i in xrange(2)] for i in xrange(len(acquisitionSummary))]
        else:
            if median_available and plotAverageChoice == 'both':
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(mean_dlp=Avg('dlp'),
                                                                median_dlp=Median('dlp') / 10000000000,
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')
            elif median_available and plotAverageChoice == 'median':
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(median_dlp=Median('dlp') / 10000000000,
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')
            else:
                acquisitionSummary = acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(mean_dlp=Avg('dlp'),
                                                                num_acq=Count('dlp')).order_by('acquisition_protocol')

        returnStructure['acquisitionSummary'] = list(acquisitionSummary)
        acquisitionHistogramData = [[None for i in xrange(2)] for i in xrange(len(acquisitionSummary))]

        for idx, protocol in enumerate(acquisitionSummary):
            dlpValues = acquisition_events.filter(
                acquisition_protocol=protocol.get('acquisition_protocol')).values_list('dlp', flat=True)
            acquisitionHistogramData[idx][0], acquisitionHistogramData[idx][1] = np.histogram(
                [float(x) for x in dlpValues], bins=plotHistogramBins)
            acquisitionHistogramData[idx][0] = acquisitionHistogramData[idx][0].tolist()
            acquisitionHistogramData[idx][1] = acquisitionHistogramData[idx][1].tolist()
            returnStructure['acquisitionHistogramData'] = list(acquisitionHistogramData)

            if plotCTAcquisitionMeanCTDI:
                ctdiValues = acquisition_events.filter(
                    acquisition_protocol=protocol.get('acquisition_protocol')).values_list('mean_ctdivol', flat=True)
                acquisitionHistogramDataCTDI[idx][0], acquisitionHistogramDataCTDI[idx][1] = np.histogram(
                    [float(x) for x in ctdiValues], bins=plotHistogramBins)
                acquisitionHistogramDataCTDI[idx][0] = acquisitionHistogramDataCTDI[idx][0].tolist()
                acquisitionHistogramDataCTDI[idx][1] = acquisitionHistogramDataCTDI[idx][1].tolist()
                returnStructure['acquisitionHistogramDataCTDI'] = acquisitionHistogramDataCTDI

    if plotCTStudyMeanDLP or plotCTStudyFreq or plotCTStudyPerDayAndHour or plotCTStudyMeanDLPOverTime:
        # Required for mean DLP per study type plot
        if median_available and plotAverageChoice == 'both':
            studySummary = study_events.values('study_description').distinct().annotate(
                mean_dlp=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                median_dlp=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                num_acq=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                'study_description')
        elif median_available and plotAverageChoice == 'median':
            studySummary = study_events.values('study_description').distinct().annotate(
                median_dlp=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                num_acq=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                'study_description')
        else:
            studySummary = study_events.values('study_description').distinct().annotate(
                mean_dlp=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                num_acq=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                'study_description')
        returnStructure['studySummary'] = list(studySummary)

        if plotCTStudyMeanDLP:
            studyHistogramData = [[None for i in xrange(2)] for i in xrange(len(studySummary))]

        if plotCTStudyMeanDLPOverTime:
            # Required for mean DLP per study type per week plot
            if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                studyMedianDLPoverTime = [None] * len(studySummary)
            if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                studyMeanDLPoverTime = [None] * len(studySummary)
            startDate = study_events.aggregate(Min('study_date')).get('study_date__min')
            today = datetime.date.today()

        if plotCTStudyMeanDLP or plotCTStudyMeanDLPOverTime:
            for idx, study in enumerate(studySummary):
                # Required for Mean DLP per study type plot AND mean DLP per study type per week plot
                subqs = study_events.filter(study_description=study.get('study_description'))

                if plotCTStudyMeanDLP:
                    # Required for mean DLP per study type plot
                    dlpValues = subqs.values_list(
                        'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', flat=True)
                    studyHistogramData[idx][0], studyHistogramData[idx][1] = np.histogram([float(x) for x in dlpValues],
                                                                                          bins=plotHistogramBins)
                    studyHistogramData[idx][0] = studyHistogramData[idx][0].tolist()
                    studyHistogramData[idx][1] = studyHistogramData[idx][1].tolist()
                    returnStructure['studyHistogramData'] = studyHistogramData

                if plotCTStudyMeanDLPOverTime:
                    # Required for mean DLP per study type per time period plot
                    if plotAverageChoice == 'mean' or plotAverageChoice == 'both':
                        qss = qsstats.QuerySetStats(subqs, 'study_date', aggregate=Avg(
                            'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'))
                        studyMeanDLPoverTime[idx] = qss.time_series(startDate, today,
                                                                    interval=plotCTStudyMeanDLPOverTimePeriod)
                        returnStructure['studyMeanDLPoverTime'] = studyMeanDLPoverTime
                    if median_available and (plotAverageChoice == 'median' or plotAverageChoice == 'both'):
                        qss = qsstats.QuerySetStats(subqs, 'study_date', aggregate=Median(
                            'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000)
                        studyMedianDLPoverTime[idx] = qss.time_series(startDate, today,
                                                                      interval=plotCTStudyMeanDLPOverTimePeriod)
                        returnStructure['studyMedianDLPoverTime'] = studyMedianDLPoverTime

        if plotCTStudyPerDayAndHour:
            # Required for studies per weekday and studies per hour in each weekday plot
            studiesPerHourInWeekdays = [[0 for x in range(24)] for x in range(7)]
            for day in range(7):
                studyTimesOnThisWeekday = study_events.filter(study_date__week_day=day + 1).values(
                    'study_workload_chart_time')

                if studyTimesOnThisWeekday:
                    qss = qsstats.QuerySetStats(studyTimesOnThisWeekday, 'study_workload_chart_time')
                    hourlyBreakdown = qss.time_series(datetime.datetime(1900, 1, 1, 0, 0),
                                                      datetime.datetime(1900, 1, 1, 23, 59), interval='hours')
                    for hour in range(24):
                        studiesPerHourInWeekdays[day][hour] = hourlyBreakdown[hour][1]
            returnStructure['studiesPerHourInWeekdays'] = studiesPerHourInWeekdays

    if plotCTRequestMeanDLP or plotCTRequestFreq:

        requestNameList = list(request_events.values_list('requested_procedure_code_meaning', flat=True).distinct().order_by('requested_procedure_code_meaning'))
        returnStructure['requestNameList'] = requestNameList

        if plotSeriesPerSystems:
            requestSystemList = list(request_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            requestSystemList = ['All systems']
        returnStructure['requestSystemList'] = requestSystemList

        if median_available and plotAverageChoice == 'both':
            requestSummary = []
            for system in requestSystemList:
                if plotSeriesPerSystems:
                    requestSummary.append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean_dlp=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            median_dlp=Median(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
                else:
                    requestSummary.append(request_events.values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean_dlp=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            median_dlp=Median(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        elif median_available and plotAverageChoice == 'median':
            requestSummary = []
            for system in requestSystemList:
                if plotSeriesPerSystems:
                    requestSummary.append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            median_dlp=Median(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
                else:
                    requestSummary.append(request_events.values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            median_dlp=Median(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        else:
            requestSummary = []
            for system in requestSystemList:
                if plotSeriesPerSystems:
                    requestSummary.append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean_dlp=Avg(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
                else:
                    requestSummary.append(request_events.values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean_dlp=Avg(
                                'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            num_req=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))

            for index in range(len(requestSummary)):
                requestSummary[index] = list(requestSummary[index])

        # Fill in default values where data for a requested procedure is missing for any of the systems
        for index in range(len(requestSystemList)):
            missing_request_names = list(set(requestNameList) - set([d['requested_procedure_code_meaning'] for d in requestSummary[index]]))
            for name in missing_request_names:
                if median_available and plotAverageChoice == 'both':
                    (requestSummary[index]).append({'median_dlp': 0, 'mean_dlp': 0,'requested_procedure_code_meaning':name, 'num_req': 0})
                elif median_available and plotAverageChoice == 'median':
                    (requestSummary[index]).append({'median_dlp': 0, 'requested_procedure_code_meaning':name, 'num_req': 0})
                else:
                    (requestSummary[index]).append({'mean_dlp': 0,'requested_procedure_code_meaning':name, 'num_req': 0})
            # Rearrange the list into the same order as requestNameList
            requestSummaryTemp = []
            for request_name in requestNameList:
                requestSummaryTemp.append(filter(lambda item: item['requested_procedure_code_meaning'] == request_name, requestSummary[index] )[0])
            requestSummary[index] = requestSummaryTemp

        returnStructure['requestSummary'] = requestSummary

        if plotCTRequestMeanDLP:
            requestHistogramData = [[[None for k in xrange(2)] for j in xrange(len(requestNameList))] for i in xrange(len(requestSystemList))]

            requestRanges = request_events.values('requested_procedure_code_meaning').distinct().annotate(
                min_dlp=Min('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField()),
                max_dlp=Max('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField())).order_by(
                'requested_procedure_code_meaning')

            for sys_idx, system in enumerate(requestSystemList):
                for req_idx, request_name in enumerate(requestNameList):
                    if plotSeriesPerSystems:
                        subqs = request_events.filter(
                                generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                                requested_procedure_code_meaning=request_name)
                    else:
                        subqs = request_events.filter(requested_procedure_code_meaning=request_name)

                    dlpValues = subqs.values_list(
                        'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                        flat=True)
                    requestHistogramData[sys_idx][req_idx][0], requestHistogramData[sys_idx][req_idx][1] = np.histogram([float(x) for x in dlpValues], bins=plotHistogramBins, range=requestRanges.filter(requested_procedure_code_meaning=request_name).values_list('min_dlp', 'max_dlp')[0])
                    requestHistogramData[sys_idx][req_idx][0] = requestHistogramData[sys_idx][req_idx][0].tolist()
                    requestHistogramData[sys_idx][req_idx][1] = requestHistogramData[sys_idx][req_idx][1].tolist()

            returnStructure['requestHistogramData'] = requestHistogramData

    return returnStructure


@login_required
def ct_detail_view(request, pk=None):
    """Detail view for a CT study
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except:
        messages.error(request, 'That study was not found')
        return redirect('/openrem/ct/')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/ctdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def mg_summary_list_filter(request):
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    filter_data = request.GET.copy()
    if 'page' in filter_data:
        del filter_data['page']

    if request.user.groups.filter(name='pidgroup'):
        f = MGFilterPlusPid(filter_data, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='MG'))
    else:
        f = MGSummaryListFilter(filter_data, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='MG'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/mgfiltered.html',
        {'filter': f, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def mg_detail_view(request, pk=None):
    """Detail view for a CT study
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except:
        messages.error(request, 'That study was not found')
        return redirect('/openrem/mg/')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/mgdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin},
        context_instance=RequestContext(request)
    )


def openrem_home(request):
    from remapp.models import GeneralStudyModuleAttr, PatientIDSettings, DicomDeleteSettings
    from django.db.models import Q  # For the Q "OR" query used for DX and CR
    from datetime import datetime
    import pytz
    from collections import OrderedDict
    utc = pytz.UTC

    test_dicom_store_settings = DicomDeleteSettings.objects.all()
    if not test_dicom_store_settings:
        DicomDeleteSettings.objects.create()

    if not Group.objects.filter(name="viewgroup"):
        vg = Group(name="viewgroup")
        vg.save()
    if not Group.objects.filter(name="exportgroup"):
        eg = Group(name="exportgroup")
        eg.save()
    if not Group.objects.filter(name="admingroup"):
        ag = Group(name="admingroup")
        ag.save()
    if not Group.objects.filter(name="pidgroup"):
        pg = Group(name="pidgroup")
        pg.save()
    if not Group.objects.filter(name="importsizegroup"):
        sg = Group(name="importsizegroup")
        sg.save()
    if not Group.objects.filter(name="importqrgroup"):
        qg = Group(name="importqrgroup")
        qg.save()

    id_settings = PatientIDSettings.objects.all()
    if not id_settings:
        PatientIDSettings.objects.create()

    users_in_groups = {'any': False, 'admin': False}
    for g in Group.objects.all():
        if Group.objects.get(name=g).user_set.all():
            users_in_groups['any'] = True
            if g.name == 'admingroup':
                users_in_groups['admin'] = True

    allstudies = GeneralStudyModuleAttr.objects.all()
    homedata = {
        'total': allstudies.count(),
        'mg': allstudies.filter(modality_type__exact='MG').count(),
        'ct': allstudies.filter(modality_type__exact='CT').count(),
        'rf': allstudies.filter(modality_type__contains='RF').count(),
        'dx': allstudies.filter(Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).count(),
    }

    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        if request.user.is_authenticated():
            # Create a default userprofile for the user if one doesn't exist
            create_user_profile(sender=request.user, instance=request.user, created=True)
            userProfile = request.user.userprofile

    if request.user.is_authenticated():
        if homedata['mg']:
            userProfile.displayMG = True
        else:
            userProfile.displayMG = False

        if homedata['ct']:
            userProfile.displayCT = True
        else:
            userProfile.displayCT = False

        if homedata['rf']:
            userProfile.displayRF = True
        else:
            userProfile.displayRF = False

        if homedata['dx']:
            userProfile.displayDX = True
        else:
            userProfile.displayDX = False

        userProfile.save()

    admin = dict(openremversion=remapp.__version__, docsversion=remapp.__docs_version__)

    for group in request.user.groups.all():
        admin[group.name] = True

    modalities = ('MG', 'CT', 'RF', 'DX')
    for modality in modalities:
        # 10/10/2014, DJP: added code to combine DX with CR
        if modality == 'DX':
            # studies = allstudies.filter(modality_type__contains = modality).all()
            studies = allstudies.filter(Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).all()
        else:
            studies = allstudies.filter(modality_type__contains=modality).all()
        # End of 10/10/2014 DJP code changes

        display_names = studies.values_list(
            'generalequipmentmoduleattr__unique_equipment_name__display_name').distinct()
        modalitydata = {}
        for display_name in display_names:
            latestdate = studies.filter(
                generalequipmentmoduleattr__unique_equipment_name__display_name__exact=display_name[0]
            ).latest('study_date').study_date
            latestuid = studies.filter(
                generalequipmentmoduleattr__unique_equipment_name__display_name__exact=display_name[0]
                ).filter(study_date__exact=latestdate).latest('study_time')
            latestdatetime = datetime.combine(latestuid.study_date, latestuid.study_time)

            try:
                displayname = (display_name[0]).encode('utf-8')
            except AttributeError:
                displayname = "Error has occurred - import probably unsuccessful"

            modalitydata[display_name[0]] = {
                'total': studies.filter(
                    generalequipmentmoduleattr__unique_equipment_name__display_name__exact=display_name[0]
                ).count(),
                'latest': latestdatetime,
                'displayname': displayname
            }
        ordereddata = OrderedDict(sorted(modalitydata.items(), key=lambda t: t[1]['latest'], reverse=True))
        homedata[modality] = ordereddata

    return render(request, "remapp/home.html",
                  {'homedata': homedata, 'admin': admin, 'users_in_groups': users_in_groups})


@login_required
def study_delete(request, pk, template_name='remapp/study_confirm_delete.html'):
    study = get_object_or_404(GeneralStudyModuleAttr, pk=pk)

    if request.method == 'POST':
        if request.user.groups.filter(name="admingroup"):
            study.delete()
            messages.success(request, "Study deleted")
        else:
            messages.error(request, "Only members of the admingroup are allowed to delete studies")
        return redirect(request.POST['return_url'])

    if request.user.groups.filter(name="admingroup"):
        return render(request, template_name, {'exam': study,'return_url': request.META['HTTP_REFERER']})

    if 'HTTP_REFERER' in request.META.keys():
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect("/openrem/")




import os, sys, csv
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from openremproject.settings import MEDIA_ROOT
from remapp.models import SizeUpload
from remapp.forms import SizeUploadForm


@login_required
def size_upload(request):
    """Form for upload of csv file containing patient size information. POST request passes database entry ID to size_process

    :param request: If POST, contains the file upload information
    """

    if not request.user.groups.filter(name="importsizegroup"):
        messages.error(request, "You are not in the import size group - please contact your administrator")
        return redirect('/openrem/')

    # Handle file upload
    if request.method == 'POST' and request.user.groups.filter(name="importsizegroup"):
        form = SizeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newcsv = SizeUpload(sizefile=request.FILES['sizefile'])
            newcsv.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect("/openrem/admin/sizeprocess/{0}/".format(newcsv.id))
    else:
        form = SizeUploadForm()  # A empty, unbound form

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    # Render list page with the documents and the form
    return render_to_response(
        'remapp/sizeupload.html',
        {'form': form, 'admin': admin},
        context_instance=RequestContext(request)
    )


from remapp.forms import SizeHeadersForm


@login_required
def size_process(request, *args, **kwargs):
    """Form for csv column header patient size imports through the web interface. POST request launches import task

    :param request: If POST, contains the field header information
    :param pk: From URL, identifies database patient size import record
    :type pk: kwarg
    """
    from remapp.extractors.ptsizecsv2db import websizeimport

    if not request.user.groups.filter(name="importsizegroup"):
        messages.error(request, "You are not in the import size group - please contact your administrator")
        return redirect('/openrem/')

    if request.method == 'POST':

        itemsInPost = len(request.POST.values())
        uniqueItemsInPost = len(set(request.POST.values()))

        if itemsInPost == uniqueItemsInPost:
            csvrecord = SizeUpload.objects.all().filter(id__exact=kwargs['pk'])[0]

            if not csvrecord.sizefile:
                messages.error(request, "File to be processed doesn't exist. Do you wish to try again?")
                return HttpResponseRedirect("/openrem/admin/sizeupload")

            csvrecord.height_field = request.POST['height_field']
            csvrecord.weight_field = request.POST['weight_field']
            csvrecord.id_field = request.POST['id_field']
            csvrecord.id_type = request.POST['id_type']
            csvrecord.save()

            job = websizeimport.delay(csv_pk=kwargs['pk'])

            return HttpResponseRedirect("/openrem/admin/sizeimports")

        else:
            messages.error(request, "Duplicate column header selection. Each field must have a different header.")
            return HttpResponseRedirect("/openrem/admin/sizeprocess/{0}/".format(kwargs['pk']))

    else:

        csvrecord = SizeUpload.objects.all().filter(id__exact=kwargs['pk'])
        with open(os.path.join(MEDIA_ROOT, csvrecord[0].sizefile.name), 'rb') as csvfile:
            try:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                if csv.Sniffer().has_header(csvfile.read(1024)):
                    csvfile.seek(0)
                    dataset = csv.DictReader(csvfile)
                    messages.success(request, "CSV file with column headers found.")
                    fieldnames = tuple(zip(dataset.fieldnames, dataset.fieldnames))
                    form = SizeHeadersForm(my_choice=fieldnames)
                else:
                    csvfile.seek(0)
                    messages.error(request,
                                   "Doesn't appear to have a header row. First row: {0}. The uploaded file has been deleted.".format(
                                       next(csvfile)))
                    csvrecord[0].sizefile.delete()
                    return HttpResponseRedirect("/openrem/admin/sizeupload")
            except csv.Error as e:
                messages.error(request,
                               "Doesn't appear to be a csv file. Error({0}). The uploaded file has been deleted.".format(
                                   e))
                csvrecord[0].sizefile.delete()
                return HttpResponseRedirect("/openrem/admin/sizeupload")
            except:
                messages.error(request,
                               "Unexpected error - please contact an administrator: {0}.".format(sys.exc_info()[0]))
                csvrecord[0].sizefile.delete()
                return HttpResponseRedirect("/openrem/admin/sizeupload")

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/sizeprocess.html',
        {'form': form, 'csvid': kwargs['pk'], 'admin': admin},
        context_instance=RequestContext(request)
    )


def size_imports(request, *args, **kwargs):
    """Lists patient size imports in the web interface

    :param request:
    """
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from remapp.models import SizeUpload

    if not request.user.groups.filter(name="importsizegroup") and not request.user.groups.filter(name="admingroup"):
        messages.error(request, "You are not in the import size group - please contact your administrator")
        return redirect('/openrem/')

    imports = SizeUpload.objects.all().order_by('-import_date')

    current = imports.filter(status__contains='CURRENT')
    complete = imports.filter(status__contains='COMPLETE')
    errors = imports.filter(status__contains='ERROR')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/sizeimports.html',
        {'admin': admin, 'current': current, 'complete': complete, 'errors': errors},
        context_instance=RequestContext(request)
    )


@csrf_exempt
@login_required
def size_delete(request):
    """Task to delete records of patient size imports through the web interface

    :param request: Contains the task ID
    :type request: POST
    """
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    from django.contrib import messages
    from remapp.models import SizeUpload

    for task in request.POST:
        uploads = SizeUpload.objects.filter(task_id__exact=request.POST[task])
        for upload in uploads:
            try:
                upload.logfile.delete()
                upload.delete()
                messages.success(request, "Export file and database entry deleted successfully.")
            except OSError as e:
                messages.error(request,
                               "Export file delete failed - please contact an administrator. Error({0}): {1}".format(
                                   e.errno, e.strerror))
            except:
                messages.error(request,
                               "Unexpected error - please contact an administrator: {0}".format(sys.exc_info()[0]))

    return HttpResponseRedirect(reverse(size_imports))


@login_required
def size_abort(request, pk):
    """View to abort current patient size imports

    :param request: Contains the task primary key
    :type request: POST
    """
    from celery.task.control import revoke
    from django.http import HttpResponseRedirect
    from django.shortcuts import get_object_or_404
    from remapp.models import SizeUpload

    size_import = get_object_or_404(SizeUpload, pk=pk)

    if request.user.groups.filter(name="importsizegroup") or request.users.groups.filter(name="admingroup"):
        revoke(size_import.task_id, terminate=True)
        size_import.logfile.delete()
        size_import.sizefile.delete()
        size_import.delete()
    else:
        messages.error(request, "Only members of the importsizegroup or admingroup can abort a size import task")

    return HttpResponseRedirect("/openrem/admin/sizeimports/")


def charts_off(request):
    try:
        # See if the user has plot settings in userprofile
        userProfile = request.user.userprofile
    except:
        if request.user.is_authenticated():
            # Create a default userprofile for the user if one doesn't exist
            create_user_profile(sender=request.user, instance=request.user, created=True)
            userProfile = request.user.userprofile

    # Switch chart plotting off
    userProfile.plotCharts = False
    userProfile.save()
    if request.user.get_full_name():
        name = request.user.get_full_name()
    else:
        name = request.user.get_username()
    messages.success(request, "Chart plotting has been turned off for {0}".format(name))

    # Redirect to the calling page, removing '&plotCharts=on' from the url
    return redirect((request.META['HTTP_REFERER']).replace('&plotCharts=on',''))


@login_required
def display_names_view(request):
    from django.db.models import Q
    from remapp.models import UniqueEquipmentNames

    f = UniqueEquipmentNames.objects.order_by('display_name')

    ct_names = f.filter(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CT").distinct()
    mg_names = f.filter(generalequipmentmoduleattr__general_study_module_attributes__modality_type="MG").distinct()
    dx_names = f.filter(Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") | Q(
        generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR")).distinct()
    rf_names = f.filter(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF").distinct()
    ot_names = f.filter(~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF") & ~Q(
        generalequipmentmoduleattr__general_study_module_attributes__modality_type="MG") & ~Q(
        generalequipmentmoduleattr__general_study_module_attributes__modality_type="CT") & ~Q(
        generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") & ~Q(
        generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR")).distinct()

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'name_list': f, 'admin': admin,
                        'ct_names': ct_names, 'mg_names': mg_names, 'dx_names': dx_names, 'rf_names': rf_names,
                        'ot_names': ot_names}

    return render_to_response(
        'remapp/displaynameview.html',
        return_structure,
        context_instance=RequestContext(request)
    )


def display_name_gen_hash(eq):
    from remapp.tools.hash_id import hash_id

    eq.manufacturer_hash = hash_id(eq.manufacturer)
    eq.institution_name_hash = hash_id(eq.institution_name)
    eq.station_name_hash = hash_id(eq.station_name)
    eq.institutional_department_name_hash = hash_id(eq.institutional_department_name)
    eq.manufacturer_model_name_hash = hash_id(eq.manufacturer_model_name)
    eq.device_serial_number_hash = hash_id(eq.device_serial_number)
    eq.software_versions_hash = hash_id(eq.software_versions)
    eq.gantry_id_hash = hash_id(eq.gantry_id)
    eq.hash_generated = True
    eq.save()


@login_required
def display_name_update(request, pk):
    from remapp.models import UniqueEquipmentNames
    from remapp.forms import UpdateDisplayNameForm

    if request.method == 'POST':
        form = UpdateDisplayNameForm(request.POST)
        if form.is_valid():
            new_display_name = form.cleaned_data['display_name']
            display_name_data = UniqueEquipmentNames.objects.get(pk=pk)
            if not display_name_data.hash_generated:
                display_name_gen_hash(display_name_data)
            display_name_data.display_name = new_display_name
            display_name_data.save()
            return HttpResponseRedirect('/openrem/viewdisplaynames/')

    else:
        max_pk = UniqueEquipmentNames.objects.all().order_by('-pk').values_list('pk')[0][0]
        if int(pk) <= max_pk:
            f = UniqueEquipmentNames.objects.filter(pk=pk)
        else:
            return HttpResponseRedirect('/openrem/viewdisplaynames/')

        form = UpdateDisplayNameForm(initial={'display_name': (f.values_list('display_name')[0][0]).encode('utf-8')},
                                     auto_id=False)

        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

        for group in request.user.groups.all():
            admin[group.name] = True

        return_structure = {'name_list': f, 'admin': admin, 'form': form}

    return render_to_response('remapp/displaynameupdate.html',
                              return_structure,
                              context_instance=RequestContext(request))


@login_required
def chart_options_view(request):
    from remapp.forms import GeneralChartOptionsDisplayForm, DXChartOptionsDisplayForm, CTChartOptionsDisplayForm
    from openremproject import settings

    if request.method == 'POST':
        general_form = GeneralChartOptionsDisplayForm(request.POST)
        ct_form = CTChartOptionsDisplayForm(request.POST)
        dx_form = DXChartOptionsDisplayForm(request.POST)
        if general_form.is_valid() and ct_form.is_valid() and dx_form.is_valid():
            try:
                # See if the user has plot settings in userprofile
                user_profile = request.user.userprofile
            except:
                # Create a default userprofile for the user if one doesn't exist
                create_user_profile(sender=request.user, instance=request.user, created=True)
                user_profile = request.user.userprofile

            user_profile.plotCharts = general_form.cleaned_data['plotCharts']
            user_profile.plotInitialSortingDirection = general_form.cleaned_data['plotInitialSortingDirection']
            if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                user_profile.plotAverageChoice = general_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.plotSeriesPerSystem = general_form.cleaned_data['plotSeriesPerSystem']
            user_profile.plotHistogramBins = general_form.cleaned_data['plotHistogramBins']

            user_profile.plotCTAcquisitionMeanDLP = ct_form.cleaned_data['plotCTAcquisitionMeanDLP']
            user_profile.plotCTAcquisitionMeanCTDI = ct_form.cleaned_data['plotCTAcquisitionMeanCTDI']
            user_profile.plotCTAcquisitionFreq = ct_form.cleaned_data['plotCTAcquisitionFreq']
            user_profile.plotCTStudyMeanDLP = ct_form.cleaned_data['plotCTStudyMeanDLP']
            user_profile.plotCTStudyFreq = ct_form.cleaned_data['plotCTStudyFreq']
            user_profile.plotCTRequestMeanDLP = ct_form.cleaned_data['plotCTRequestMeanDLP']
            user_profile.plotCTRequestFreq = ct_form.cleaned_data['plotCTRequestFreq']
            user_profile.plotCTStudyPerDayAndHour = ct_form.cleaned_data['plotCTStudyPerDayAndHour']
            user_profile.plotCTStudyMeanDLPOverTime = ct_form.cleaned_data['plotCTStudyMeanDLPOverTime']
            user_profile.plotCTStudyMeanDLPOverTimePeriod = ct_form.cleaned_data['plotCTStudyMeanDLPOverTimePeriod']
            user_profile.plotCTInitialSortingChoice = ct_form.cleaned_data['plotCTInitialSortingChoice']

            user_profile.plotDXAcquisitionMeanDAP = dx_form.cleaned_data['plotDXAcquisitionMeanDAP']
            user_profile.plotDXAcquisitionFreq = dx_form.cleaned_data['plotDXAcquisitionFreq']
            user_profile.plotDXAcquisitionMeankVp = dx_form.cleaned_data['plotDXAcquisitionMeankVp']
            user_profile.plotDXAcquisitionMeanmAs = dx_form.cleaned_data['plotDXAcquisitionMeanmAs']
            user_profile.plotDXStudyPerDayAndHour = dx_form.cleaned_data['plotDXStudyPerDayAndHour']
            user_profile.plotDXAcquisitionMeanDAPOverTime = dx_form.cleaned_data['plotDXAcquisitionMeanDAPOverTime']
            user_profile.plotDXAcquisitionMeanDAPOverTimePeriod = dx_form.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTimePeriod']
            user_profile.plotDXInitialSortingChoice = dx_form.cleaned_data['plotDXInitialSortingChoice']

            user_profile.save()

        messages.success(request, "Chart options have been updated")

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    general_form_data = {'plotCharts': user_profile.plotCharts,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice,
                         'plotInitialSortingDirection': user_profile.plotInitialSortingDirection,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem,
                         'plotHistogramBins': user_profile.plotHistogramBins}

    ct_form_data = {'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                    'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                    'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                    'plotCTStudyMeanDLP': user_profile.plotCTStudyMeanDLP,
                    'plotCTStudyFreq': user_profile.plotCTStudyFreq,
                    'plotCTRequestMeanDLP': user_profile.plotCTRequestMeanDLP,
                    'plotCTRequestFreq': user_profile.plotCTRequestFreq,
                    'plotCTStudyPerDayAndHour': user_profile.plotCTStudyPerDayAndHour,
                    'plotCTStudyMeanDLPOverTime': user_profile.plotCTStudyMeanDLPOverTime,
                    'plotCTStudyMeanDLPOverTimePeriod': user_profile.plotCTStudyMeanDLPOverTimePeriod,
                    'plotCTInitialSortingChoice': user_profile.plotCTInitialSortingChoice}

    dx_form_data = {'plotDXAcquisitionMeanDAP': user_profile.plotDXAcquisitionMeanDAP,
                    'plotDXAcquisitionFreq': user_profile.plotDXAcquisitionFreq,
                    'plotDXAcquisitionMeankVp': user_profile.plotDXAcquisitionMeankVp,
                    'plotDXAcquisitionMeanmAs': user_profile.plotDXAcquisitionMeanmAs,
                    'plotDXStudyPerDayAndHour': user_profile.plotDXStudyPerDayAndHour,
                    'plotDXAcquisitionMeanDAPOverTime': user_profile.plotDXAcquisitionMeanDAPOverTime,
                    'plotDXAcquisitionMeanDAPOverTimePeriod': user_profile.plotDXAcquisitionMeanDAPOverTimePeriod,
                    'plotDXInitialSortingChoice': user_profile.plotDXInitialSortingChoice}

    general_chart_options_form = GeneralChartOptionsDisplayForm(general_form_data)
    ct_chart_options_form = CTChartOptionsDisplayForm(ct_form_data)
    dx_chart_options_form = DXChartOptionsDisplayForm(dx_form_data)

    return_structure = {'admin': admin,
                        'GeneralChartOptionsForm': general_chart_options_form,
                        'CTChartOptionsForm': ct_chart_options_form,
                        'DXChartOptionsForm': dx_chart_options_form,
                        }

    return render_to_response(
        'remapp/displaychartoptions.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def dicom_summary(request):
    """Displays current DICOM configuration
    """
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.models import DicomDeleteSettings, DicomRemoteQR, DicomStoreSCP

    try:
        del_settings = DicomDeleteSettings.objects.get()
    except ObjectDoesNotExist:
        DicomDeleteSettings.objects.create()
        del_settings = DicomDeleteSettings.objects.get()

    store = DicomStoreSCP.objects.all()
    remoteqr = DicomRemoteQR.objects.all()

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    # Render list page with the documents and the form
    return render_to_response(
        'remapp/dicomsummary.html',
        {'store': store, 'remoteqr': remoteqr, 'admin': admin, 'del_settings': del_settings},
        context_instance=RequestContext(request)
    )


class DicomStoreCreate(CreateView):
    from remapp.forms import DicomStoreForm
    from remapp.models import DicomStoreSCP

    model = DicomStoreSCP
    form_class = DicomStoreForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomStoreUpdate(UpdateView):
    from remapp.forms import DicomStoreForm
    from remapp.models import DicomStoreSCP

    model = DicomStoreSCP
    form_class = DicomStoreForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomStoreDelete(DeleteView):
    from remapp.models import DicomStoreSCP

    model = DicomStoreSCP
    success_url = reverse_lazy('dicom_summary')

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomQRCreate(CreateView):
    from remapp.forms import DicomQRForm
    from remapp.models import DicomRemoteQR

    model = DicomRemoteQR
    form_class = DicomQRForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomQRUpdate(UpdateView):
    from remapp.forms import DicomQRForm
    from remapp.models import DicomRemoteQR

    model = DicomRemoteQR
    form_class = DicomQRForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomQRDelete(DeleteView):
    from remapp.models import DicomRemoteQR

    model = DicomRemoteQR
    success_url = reverse_lazy('dicom_summary')

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class PatientIDSettingsUpdate(UpdateView):
    from remapp.models import PatientIDSettings

    model = PatientIDSettings
    fields = ['name_stored', 'name_hashed', 'id_stored', 'id_hashed', 'accession_hashed', 'dob_stored']

    def get_context_data(self, **context):

        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class DicomDeleteSettingsUpdate(UpdateView):
    from remapp.models import DicomDeleteSettings
    from remapp.forms import DicomDeleteSettingsForm

    model = DicomDeleteSettings
    form_class = DicomDeleteSettingsForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context
