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
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    if user_profile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        user_profile.median_available = True
        user_profile.save()
        median_available = True
    else:
        user_profile.median_available = False
        user_profile.save()
        median_available = False

    # Obtain the chart options from the request
    chart_options_form = DXChartOptionsForm(request.GET)
    # check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotDXAcquisitionMeanDAP = chart_options_form.cleaned_data['plotDXAcquisitionMeanDAP']
            user_profile.plotDXAcquisitionFreq = chart_options_form.cleaned_data['plotDXAcquisitionFreq']
            user_profile.plotDXStudyMeanDAP = chart_options_form.cleaned_data['plotDXStudyMeanDAP']
            user_profile.plotDXStudyFreq = chart_options_form.cleaned_data['plotDXStudyFreq']
            user_profile.plotDXRequestMeanDAP = chart_options_form.cleaned_data['plotDXRequestMeanDAP']
            user_profile.plotDXRequestFreq = chart_options_form.cleaned_data['plotDXRequestFreq']
            user_profile.plotDXAcquisitionMeankVp = chart_options_form.cleaned_data['plotDXAcquisitionMeankVp']
            user_profile.plotDXAcquisitionMeanmAs = chart_options_form.cleaned_data['plotDXAcquisitionMeanmAs']
            user_profile.plotDXStudyPerDayAndHour = chart_options_form.cleaned_data['plotDXStudyPerDayAndHour']
            user_profile.plotDXAcquisitionMeankVpOverTime = chart_options_form.cleaned_data[
                'plotDXAcquisitionMeankVpOverTime']
            user_profile.plotDXAcquisitionMeanmAsOverTime = chart_options_form.cleaned_data[
                'plotDXAcquisitionMeanmAsOverTime']
            user_profile.plotDXAcquisitionMeanDAPOverTime = chart_options_form.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTime']
            user_profile.plotDXAcquisitionMeanDAPOverTimePeriod = chart_options_form.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTimePeriod']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotDXAcquisitionMeanDAP': user_profile.plotDXAcquisitionMeanDAP,
                         'plotDXAcquisitionFreq': user_profile.plotDXAcquisitionFreq,
                         'plotDXStudyMeanDAP': user_profile.plotDXStudyMeanDAP,
                         'plotDXStudyFreq': user_profile.plotDXStudyFreq,
                         'plotDXRequestMeanDAP': user_profile.plotDXRequestMeanDAP,
                         'plotDXRequestFreq': user_profile.plotDXRequestFreq,
                         'plotDXAcquisitionMeankVp': user_profile.plotDXAcquisitionMeankVp,
                         'plotDXAcquisitionMeanmAs': user_profile.plotDXAcquisitionMeanmAs,
                         'plotDXStudyPerDayAndHour': user_profile.plotDXStudyPerDayAndHour,
                         'plotDXAcquisitionMeankVpOverTime': user_profile.plotDXAcquisitionMeankVpOverTime,
                         'plotDXAcquisitionMeanmAsOverTime': user_profile.plotDXAcquisitionMeanmAsOverTime,
                         'plotDXAcquisitionMeanDAPOverTime': user_profile.plotDXAcquisitionMeanDAPOverTime,
                         'plotDXAcquisitionMeanDAPOverTimePeriod': user_profile.plotDXAcquisitionMeanDAPOverTimePeriod,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice}
            chart_options_form = DXChartOptionsForm(form_data)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form}

    return render_to_response(
        'remapp/dxfiltered.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def dx_summary_chart_data(request):
    from remapp.interface.mod_filters import DXSummaryListFilter
    from django.db.models import Q
    from openremproject import settings
    from django.http import JsonResponse

    request_results = request.GET

    f = DXSummaryListFilter(request_results, queryset=GeneralStudyModuleAttr.objects.filter(
        Q(modality_type__exact='DX') | Q(modality_type__exact='CR')
    ).order_by().distinct())

    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    if user_profile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        user_profile.median_available = True
        user_profile.save()
        median_available = True
    else:
        user_profile.median_available = False
        user_profile.save()
        median_available = False

    return_structure = \
        dx_plot_calculations(f, user_profile.plotDXAcquisitionMeanDAP, user_profile.plotDXAcquisitionFreq,
                             user_profile.plotDXStudyMeanDAP, user_profile.plotDXStudyFreq,
                             user_profile.plotDXRequestMeanDAP, user_profile.plotDXRequestFreq,
                             user_profile.plotDXAcquisitionMeankVpOverTime, user_profile.plotDXAcquisitionMeanmAsOverTime,
                             user_profile.plotDXAcquisitionMeanDAPOverTime, user_profile.plotDXAcquisitionMeanDAPOverTimePeriod,
                             user_profile.plotDXAcquisitionMeankVp, user_profile.plotDXAcquisitionMeanmAs,
                             user_profile.plotDXStudyPerDayAndHour, request_results,
                             median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem,
                             user_profile.plotHistogramBins)

    return JsonResponse(return_structure, safe=False)


def dx_plot_calculations(f, plot_acquisition_mean_dap, plot_acquisition_freq,
                         plot_study_mean_dap, plot_study_freq,
                         plot_request_mean_dap, plot_request_freq,
                         plot_acquisition_mean_kvp_over_time, plot_acquisition_mean_mas_over_time,
                         plot_acquisition_mean_dap_over_time, plot_acquisition_mean_dap_over_time_period,
                         plot_acquisition_mean_kvp, plot_acquisition_mean_mas,
                         plot_study_per_day_and_hour, request_results,
                         median_available, plot_average_choice, plot_series_per_systems, plot_histogram_bins):
    from remapp.models import IrradEventXRayData, Median
    from django.db.models import Avg, Count, Min, Max, FloatField
    import datetime, qsstats
    if plotting:
        import numpy as np

    return_structure = {}

    exp_include = [o.study_instance_uid for o in f]

    if plot_acquisition_mean_dap or plot_acquisition_freq or plot_acquisition_mean_dap_over_time or plot_acquisition_mean_kvp_over_time or plot_acquisition_mean_kvp or plot_acquisition_mean_mas_over_time or plot_acquisition_mean_mas:
        acquisition_filters = {
            'projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid__in': exp_include}
        if request_results.get('acquisition_dap_max'):
            acquisition_filters['dose_area_product__lte'] = request_results.get('acquisition_dap_max')
        if request_results.get('acquisition_dap_min'):
            acquisition_filters['dose_area_product__gte'] = request_results.get('acquisition_dap_min')
        if request_results.get('acquisition_protocol'):
            acquisition_filters['acquisition_protocol__icontains'] = request_results.get('acquisition_protocol')
        if request_results.get('acquisition_kvp_min'):
            acquisition_filters['irradeventxraysourcedata__kvp__kvp__gte'] = request_results.get('acquisition_kvp_min')
        if request_results.get('acquisition_kvp_max'):
            acquisition_filters['irradeventxraysourcedata__kvp__kvp__lte'] = request_results.get('acquisition_kvp_max')
        if request_results.get('acquisition_mas_min'):
            acquisition_filters['irradeventxraysourcedata__exposure__exposure__gte'] = request_results.get(
                'acquisition_mas_min')
        if request_results.get('acquisition_mas_max'):
            acquisition_filters['irradeventxraysourcedata__exposure__exposure__lte'] = request_results.get(
                'acquisition_mas_max')

    if plot_acquisition_mean_dap or plot_acquisition_freq or plot_acquisition_mean_dap_over_time:
        acquisition_events = IrradEventXRayData.objects.exclude(
            dose_area_product__isnull=True
        ).filter(
            **acquisition_filters
        )
        return_structure['acquisition_names'] = list(acquisition_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))

    if plot_study_mean_dap or plot_study_freq:
        study_events = GeneralStudyModuleAttr.objects.exclude(
            projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
        ).exclude(
            study_description__isnull=True
        ).filter(
            study_instance_uid__in=exp_include
        )
        return_structure['study_names'] = list(study_events.values_list('study_description', flat=True).distinct().order_by('study_description'))

    if plot_request_mean_dap or plot_request_freq:
        request_events = GeneralStudyModuleAttr.objects.exclude(
            projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
        ).exclude(
            requested_procedure_code_meaning__isnull=True
        ).filter(
            study_instance_uid__in=exp_include
        )
        return_structure['request_names'] = list(request_events.values_list('requested_procedure_code_meaning', flat=True).distinct().order_by('requested_procedure_code_meaning'))

    if plot_acquisition_mean_kvp_over_time or plot_acquisition_mean_kvp:
        acquisition_kvp_events = IrradEventXRayData.objects.exclude(
            irradeventxraysourcedata__kvp__kvp__isnull=True
        ).filter(
            **acquisition_filters
        )
        return_structure['acquisition_kvp_names'] = list(acquisition_kvp_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))

    if plot_acquisition_mean_mas_over_time or plot_acquisition_mean_mas:
        acquisition_mas_events = IrradEventXRayData.objects.exclude(
            irradeventxraysourcedata__exposure__exposure__isnull=True
        ).filter(
            **acquisition_filters
        )
        return_structure['acquisition_mas_names'] = list(acquisition_mas_events.values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))

    if plot_acquisition_mean_dap or plot_acquisition_freq:
        if plot_series_per_systems and plot_acquisition_mean_dap:
            return_structure['acquisitionSystemList'] = list(acquisition_events.values_list('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['acquisitionSystemList'] = ['All systems']

        return_structure['acquisitionSummary'] = []

        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems and plot_acquisition_mean_dap:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('dose_area_product') * 1000000,
                            median=Median('dose_area_product') / 10000,
                            num=Count('dose_area_product')).order_by('acquisition_protocol'))
            elif plot_acquisition_mean_dap:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('dose_area_product') * 1000000,
                        median=Median('dose_area_product') / 10000,
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems and plot_acquisition_mean_dap:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            median=Median('dose_area_product') / 10000,
                            num=Count('dose_area_product')).order_by('acquisition_protocol'))
            elif plot_acquisition_mean_dap:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        median=Median('dose_area_product') / 10000,
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))

        else:
            if plot_series_per_systems and plot_acquisition_mean_dap:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('dose_area_product') * 1000000,
                            num=Count('dose_area_product')).order_by('acquisition_protocol'))
            elif plot_acquisition_mean_dap:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('dose_area_product') * 1000000,
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.values('acquisition_protocol').distinct().annotate(
                        num=Count('dose_area_product')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionSummary'])):
            return_structure['acquisitionSummary'][index] = list(return_structure['acquisitionSummary'][index])

        # Fill in default values where data for an acquisition protocol is missing for any of the systems
        if plot_series_per_systems and plot_acquisition_mean_dap:
            for index in range(len(return_structure['acquisitionSystemList'])):
                missing_names = list(set(return_structure['acquisition_names']) - set([d['acquisition_protocol'] for d in return_structure['acquisitionSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['acquisitionSummary'][index]).append({'median': 0, 'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['acquisitionSummary'][index]).append({'median': 0, 'acquisition_protocol':missing_name, 'num': 0})
                    else:
                        (return_structure['acquisitionSummary'][index]).append({'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in return_structure['acquisition_names']:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionSummary'][index])[0])
                return_structure['acquisitionSummary'][index] = summary_temp

    if plot_acquisition_mean_dap:
        return_structure['acquisitionHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['acquisition_names']))] for i in xrange(len(return_structure['acquisitionSystemList']))]

        value_ranges = acquisition_events.values('acquisition_protocol').distinct().annotate(
                min_dap=Min('dose_area_product', output_field=FloatField()),
                max_dap=Max('dose_area_product', output_field=FloatField())).order_by('acquisition_protocol')

        for sys_idx, system in enumerate(return_structure['acquisitionSystemList']):
            for acq_idx, acquisition_name in enumerate(return_structure['acquisition_names']):
                if plot_series_per_systems:
                    subqs = acquisition_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            acquisition_protocol=acquisition_name)
                else:
                    subqs = acquisition_events.filter(acquisition_protocol=acquisition_name)

                data_values = subqs.values_list('dose_area_product', flat=True)
                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0], return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(acquisition_protocol=acquisition_name).values_list('min_dap', 'max_dap')[0])
                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0] = return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0].tolist()
                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1] = (return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1] * 1000000).tolist()

    if plot_request_mean_dap or plot_request_freq:
        if plot_series_per_systems and plot_request_mean_dap:
            return_structure['requestSystemList'] = list(request_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['requestSystemList'] = ['All systems']

        return_structure['requestSummary'] = []

        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems and plot_request_mean_dap:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('requested_procedure_code_meaning').distinct().annotate(
                            mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                            median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                            num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            elif plot_request_mean_dap:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                        mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                        num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems and plot_request_mean_dap:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('requested_procedure_code_meaning').distinct().annotate(
                        median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            elif plot_request_mean_dap:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                    num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))

        else:
            if plot_series_per_systems and plot_request_mean_dap:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('requested_procedure_code_meaning').distinct().annotate(
                        mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            elif plot_request_mean_dap:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                    num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                    num=Count('requested_procedure_code_meaning')).order_by('requested_procedure_code_meaning'))

        for index in range(len(return_structure['requestSummary'])):
            return_structure['requestSummary'][index] = list(return_structure['requestSummary'][index])

        # Fill in default values where data for a requested procedure is missing for any of the systems
        if plot_series_per_systems and plot_request_mean_dap:
            for index in range(len(return_structure['requestSystemList'])):
                missing_names = list(set(return_structure['request_names']) - set([d['requested_procedure_code_meaning'] for d in return_structure['requestSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['requestSummary'][index]).append({'median': 0, 'mean': 0,'requested_procedure_code_meaning':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['requestSummary'][index]).append({'median': 0, 'requested_procedure_code_meaning':missing_name, 'num': 0})
                    else:
                        (return_structure['requestSummary'][index]).append({'mean': 0,'requested_procedure_code_meaning':missing_name, 'num': 0})
                # Rearrange the list into the same order as request_names
                summary_temp = []
                for request_name in return_structure['request_names']:
                    summary_temp.append(filter(lambda item: item['requested_procedure_code_meaning'] == request_name, return_structure['requestSummary'][index])[0])
                return_structure['requestSummary'][index] = summary_temp

    if plot_request_mean_dap:
        return_structure['requestHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['request_names']))] for i in xrange(len(return_structure['requestSystemList']))]

        value_ranges = request_events.values('requested_procedure_code_meaning').distinct().annotate(
                min_dap=Min('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField()),
                max_dap=Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField())).order_by('requested_procedure_code_meaning')

        for sys_idx, system in enumerate(return_structure['requestSystemList']):
            for req_idx, request_name in enumerate(return_structure['request_names']):
                if plot_series_per_systems:
                    subqs = request_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            requested_procedure_code_meaning=request_name)
                else:
                    subqs = request_events.filter(requested_procedure_code_meaning=request_name)

                data_values = subqs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', flat=True)
                return_structure['requestHistogramData'][sys_idx][req_idx][0], return_structure['requestHistogramData'][sys_idx][req_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(requested_procedure_code_meaning=request_name).values_list('min_dap', 'max_dap')[0])
                return_structure['requestHistogramData'][sys_idx][req_idx][0] = return_structure['requestHistogramData'][sys_idx][req_idx][0].tolist()
                return_structure['requestHistogramData'][sys_idx][req_idx][1] = (return_structure['requestHistogramData'][sys_idx][req_idx][1] * 1000000).tolist()

    if plot_study_mean_dap or plot_study_freq:
        if plot_series_per_systems and plot_study_mean_dap:
            return_structure['studySystemList'] = list(study_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['studySystemList'] = ['All systems']

        return_structure['studySummary'] = []

        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems and plot_study_mean_dap:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                            mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                            median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                            num=Count('study_description')).order_by('study_description'))
            elif plot_study_mean_dap:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num=Count('study_description')).order_by('study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        num=Count('study_description')).order_by('study_description'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems and plot_study_mean_dap:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                            median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                            num=Count('study_description')).order_by('study_description'))
            elif plot_study_mean_dap:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        median=Median('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') / 10000,
                        num=Count('study_description')).order_by('study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        num=Count('study_description')).order_by('study_description'))

        else:
            if plot_series_per_systems and plot_study_mean_dap:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                            mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                            num=Count('study_description')).order_by('study_description'))
            elif plot_study_mean_dap:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        mean=Avg('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total') * 1000000,
                        num=Count('study_description')).order_by('study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                        num=Count('study_description')).order_by('study_description'))

        for index in range(len(return_structure['studySummary'])):
            return_structure['studySummary'][index] = list(return_structure['studySummary'][index])

        # Fill in default values where data for a study description is missing for any of the systems
        if plot_series_per_systems and plot_study_mean_dap:
            for index in range(len(return_structure['studySystemList'])):
                missing_names = list(set(return_structure['study_names']) - set([d['study_description'] for d in return_structure['studySummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['studySummary'][index]).append({'median': 0, 'mean': 0,'study_description':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['studySummary'][index]).append({'median': 0, 'study_description':missing_name, 'num': 0})
                    else:
                        (return_structure['studySummary'][index]).append({'mean': 0,'study_description':missing_name, 'num': 0})
                # Rearrange the list into the same order as study_names
                summary_temp = []
                for study_name in return_structure['study_names']:
                    summary_temp.append(filter(lambda item: item['study_description'] == study_name, return_structure['studySummary'][index])[0])
                return_structure['studySummary'][index] = summary_temp

        if plot_study_mean_dap:
            return_structure['studyHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['study_names']))] for i in xrange(len(return_structure['studySystemList']))]

            value_ranges = study_events.values('study_description').distinct().annotate(
                    min_dap=Min('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField()),
                    max_dap=Max('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', output_field=FloatField())).order_by('study_description')

            for sys_idx, system in enumerate(return_structure['studySystemList']):
                for stu_idx, study_name in enumerate(return_structure['study_names']):
                    if plot_series_per_systems:
                        subqs = study_events.filter(
                                generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                                study_description=study_name)
                    else:
                        subqs = study_events.filter(study_description=study_name)

                    data_values = subqs.values_list('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', flat=True)
                    return_structure['studyHistogramData'][sys_idx][stu_idx][0], return_structure['studyHistogramData'][sys_idx][stu_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(study_description=study_name).values_list('min_dap', 'max_dap')[0])
                    return_structure['studyHistogramData'][sys_idx][stu_idx][0] = return_structure['studyHistogramData'][sys_idx][stu_idx][0].tolist()
                    return_structure['studyHistogramData'][sys_idx][stu_idx][1] = (return_structure['studyHistogramData'][sys_idx][stu_idx][1] * 1000000).tolist()

    if plot_acquisition_mean_kvp:
        if plot_series_per_systems:
            return_structure['acquisitionkVpSystemList'] = list(acquisition_kvp_events.values_list('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['acquisitionkVpSystemList'] = ['All systems']

        return_structure['acquisitionkVpSummary'] = []

        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['acquisitionkVpSystemList']:
                    return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('irradeventxraysourcedata__kvp__kvp'),
                            median=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('irradeventxraysourcedata__kvp__kvp'),
                        median=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['acquisitionkVpSystemList']:
                    return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            median=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.values('acquisition_protocol').distinct().annotate(
                        median=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000,
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        else:
            if plot_series_per_systems:
                for system in return_structure['acquisitionkVpSystemList']:
                    return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('irradeventxraysourcedata__kvp__kvp'),
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionkVpSummary'].append(acquisition_kvp_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('irradeventxraysourcedata__kvp__kvp'),
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionkVpSummary'])):
            return_structure['acquisitionkVpSummary'][index] = list(return_structure['acquisitionkVpSummary'][index])

        # Fill in default values where data for an acquisition protocol is missing for any of the systems
        if plot_series_per_systems:
            for index in range(len(return_structure['acquisitionkVpSystemList'])):
                missing_names = list(set(return_structure['acquisition_kvp_names']) - set([d['acquisition_protocol'] for d in return_structure['acquisitionkVpSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['acquisitionkVpSummary'][index]).append({'median': 0, 'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['acquisitionkVpSummary'][index]).append({'median': 0, 'acquisition_protocol':missing_name, 'num': 0})
                    else:
                        (return_structure['acquisitionkVpSummary'][index]).append({'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in return_structure['acquisition_kvp_names']:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionkVpSummary'][index])[0])
                return_structure['acquisitionkVpSummary'][index] = summary_temp

        return_structure['acquisitionHistogramkVpData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['acquisition_kvp_names']))] for i in xrange(len(return_structure['acquisitionkVpSystemList']))]

        value_ranges = acquisition_kvp_events.values('acquisition_protocol').distinct().annotate(
                min_kvp=Min('irradeventxraysourcedata__kvp__kvp', output_field=FloatField()),
                max_kvp=Max('irradeventxraysourcedata__kvp__kvp', output_field=FloatField())).order_by('acquisition_protocol')

        for sys_idx, system in enumerate(return_structure['acquisitionkVpSystemList']):
            for acq_idx, acquisition_name in enumerate(return_structure['acquisition_kvp_names']):
                if plot_series_per_systems:
                    subqs = acquisition_kvp_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            acquisition_protocol=acquisition_name)
                else:
                    subqs = acquisition_kvp_events.filter(acquisition_protocol=acquisition_name)

                data_values = subqs.values_list('irradeventxraysourcedata__kvp__kvp', flat=True)
                return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][0], return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(acquisition_protocol=acquisition_name).values_list('min_kvp', 'max_kvp')[0])
                return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][0] = return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][0].tolist()
                return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][1] = return_structure['acquisitionHistogramkVpData'][sys_idx][acq_idx][1].tolist()

    if plot_acquisition_mean_mas:
        if plot_series_per_systems:
            return_structure['acquisitionmAsSystemList'] = list(acquisition_mas_events.values_list('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['acquisitionmAsSystemList'] = ['All systems']

        return_structure['acquisitionmAsSummary'] = []

        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['acquisitionmAsSystemList']:
                    return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                            median=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                        median=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['acquisitionmAsSystemList']:
                    return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            median=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.values('acquisition_protocol').distinct().annotate(
                        median=Median('irradeventxraysourcedata__exposure__exposure') / 10000000000000,
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        else:
            if plot_series_per_systems:
                for system in return_structure['acquisitionmAsSystemList']:
                    return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('acquisition_protocol').distinct().annotate(
                            mean=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                            num=Count('acquisition_protocol')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionmAsSummary'].append(acquisition_mas_events.values('acquisition_protocol').distinct().annotate(
                        mean=Avg('irradeventxraysourcedata__exposure__exposure') / 1000,
                        num=Count('acquisition_protocol')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionmAsSummary'])):
            return_structure['acquisitionmAsSummary'][index] = list(return_structure['acquisitionmAsSummary'][index])

        # Fill in default values where data for an acquisition protocol is missing for any of the systems
        if plot_series_per_systems:
            for index in range(len(return_structure['acquisitionmAsSystemList'])):
                missing_names = list(set(return_structure['acquisition_mas_names']) - set([d['acquisition_protocol'] for d in return_structure['acquisitionmAsSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['acquisitionmAsSummary'][index]).append({'median': 0, 'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['acquisitionmAsSummary'][index]).append({'median': 0, 'acquisition_protocol':missing_name, 'num': 0})
                    else:
                        (return_structure['acquisitionmAsSummary'][index]).append({'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in return_structure['acquisition_mas_names']:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionmAsSummary'][index])[0])
                return_structure['acquisitionmAsSummary'][index] = summary_temp

        return_structure['acquisitionHistogrammAsData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['acquisition_mas_names']))] for i in xrange(len(return_structure['acquisitionmAsSystemList']))]

        value_ranges = acquisition_mas_events.values('acquisition_protocol').distinct().annotate(
                min_mas=Min('irradeventxraysourcedata__exposure__exposure', output_field=FloatField()),
                max_mas=Max('irradeventxraysourcedata__exposure__exposure', output_field=FloatField())).order_by('acquisition_protocol')

        for sys_idx, system in enumerate(return_structure['acquisitionmAsSystemList']):
            for acq_idx, acquisition_name in enumerate(return_structure['acquisition_mas_names']):
                if plot_series_per_systems:
                    subqs = acquisition_mas_events.filter(
                            projection_xray_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            acquisition_protocol=acquisition_name)
                else:
                    subqs = acquisition_mas_events.filter(acquisition_protocol=acquisition_name)

                data_values = subqs.values_list('irradeventxraysourcedata__exposure__exposure', flat=True)
                return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][0], return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(acquisition_protocol=acquisition_name).values_list('min_mas', 'max_mas')[0])
                return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][0] = return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][0].tolist()
                return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][1] = (return_structure['acquisitionHistogrammAsData'][sys_idx][acq_idx][1]/1000).tolist()

    if plot_acquisition_mean_kvp_over_time or plot_acquisition_mean_mas_over_time or plot_acquisition_mean_dap_over_time:
        start_date = f.qs.aggregate(Min('study_date')).get('study_date__min')
        today = datetime.date.today()

        if plot_acquisition_mean_kvp_over_time:
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                return_structure['acquisitionMediankVpoverTime'] = [None] * len(return_structure['acquisition_kvp_names'])
            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                return_structure['acquisitionMeankVpoverTime'] = [None] * len(return_structure['acquisition_kvp_names'])

        if plot_acquisition_mean_mas_over_time:
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                return_structure['acquisitionMedianmAsoverTime'] = [None] * len(return_structure['acquisition_mas_names'])
            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                return_structure['acquisitionMeanmAsoverTime'] = [None] * len(return_structure['acquisition_mas_names'])

        if plot_acquisition_mean_dap_over_time:
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                return_structure['acquisitionMedianDAPoverTime'] = [None] * len(return_structure['acquisition_names'])
            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                return_structure['acquisitionMeanDAPoverTime'] = [None] * len(return_structure['acquisition_names'])

    if plot_acquisition_mean_dap_over_time:
        for idx, protocol in enumerate(return_structure['acquisition_names']):
            subqs = acquisition_events.filter(acquisition_protocol__exact=protocol)

            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                qss = qsstats.QuerySetStats(subqs, 'date_time_started', aggregate=Avg('dose_area_product') * 1000000)
                return_structure['acquisitionMeanDAPoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                qss = qsstats.QuerySetStats(subqs, 'date_time_started', aggregate=Median('dose_area_product') / 10000)
                return_structure['acquisitionMedianDAPoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)

    if plot_acquisition_mean_kvp_over_time:
        for idx, protocol in enumerate(return_structure['acquisition_kvp_names']):
            subqs_kvp = acquisition_kvp_events.filter(acquisition_protocol=protocol)

            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                qss = qsstats.QuerySetStats(subqs_kvp, 'date_time_started', aggregate=Avg('irradeventxraysourcedata__kvp__kvp'))
                return_structure['acquisitionMeankVpoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                qss = qsstats.QuerySetStats(subqs_kvp, 'date_time_started', aggregate=Median('irradeventxraysourcedata__kvp__kvp') / 10000000000)
                return_structure['acquisitionMediankVpoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)

    if plot_acquisition_mean_mas_over_time:
        for idx, protocol in enumerate(return_structure['acquisition_mas_names']):
            subqs_mas = acquisition_mas_events.filter(acquisition_protocol=protocol)

            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                qss = qsstats.QuerySetStats(subqs_mas, 'date_time_started', aggregate=Avg('irradeventxraysourcedata__exposure__exposure') / 1000)
                return_structure['acquisitionMeanmAsoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)
            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                qss = qsstats.QuerySetStats(subqs_mas, 'date_time_started', aggregate=Median( 'irradeventxraysourcedata__exposure__exposure') / 10000000000000)
                return_structure['acquisitionMedianmAsoverTime'][idx] = qss.time_series(start_date, today, interval=plot_acquisition_mean_dap_over_time_period)

    if plot_study_per_day_and_hour:
        # Required for studies per weekday and studies per hour in each weekday plot
        return_structure['studiesPerHourInWeekdays'] = [[0 for x in range(24)] for x in range(7)]
        for day in range(7):
            study_times_on_this_weekday = f.qs.filter(study_date__week_day=day + 1).values('study_workload_chart_time')
            if study_times_on_this_weekday:
                qss = qsstats.QuerySetStats(study_times_on_this_weekday, 'study_workload_chart_time')
                hourly_breakdown = qss.time_series(datetime.datetime(1900, 1, 1, 0, 0), datetime.datetime(1900, 1, 1, 23, 59), interval='hours')
                for hour in range(24):
                    return_structure['studiesPerHourInWeekdays'][day][hour] = hourly_breakdown[hour][1]

    return return_structure


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
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    if user_profile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        user_profile.median_available = True
        user_profile.save()
        median_available = True
    else:
        user_profile.median_available = False
        user_profile.save()
        median_available = False

    # Obtain the chart options from the request
    chart_options_form = CTChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotCTAcquisitionMeanDLP = chart_options_form.cleaned_data['plotCTAcquisitionMeanDLP']
            user_profile.plotCTAcquisitionMeanCTDI = chart_options_form.cleaned_data['plotCTAcquisitionMeanCTDI']
            user_profile.plotCTAcquisitionFreq = chart_options_form.cleaned_data['plotCTAcquisitionFreq']
            user_profile.plotCTStudyMeanDLP = chart_options_form.cleaned_data['plotCTStudyMeanDLP']
            user_profile.plotCTStudyFreq = chart_options_form.cleaned_data['plotCTStudyFreq']
            user_profile.plotCTRequestMeanDLP = chart_options_form.cleaned_data['plotCTRequestMeanDLP']
            user_profile.plotCTRequestFreq = chart_options_form.cleaned_data['plotCTRequestFreq']
            user_profile.plotCTStudyPerDayAndHour = chart_options_form.cleaned_data['plotCTStudyPerDayAndHour']
            user_profile.plotCTStudyMeanDLPOverTime = chart_options_form.cleaned_data['plotCTStudyMeanDLPOverTime']
            user_profile.plotCTStudyMeanDLPOverTimePeriod = chart_options_form.cleaned_data[
                'plotCTStudyMeanDLPOverTimePeriod']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                        'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                        'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                        'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                        'plotCTStudyMeanDLP': user_profile.plotCTStudyMeanDLP,
                        'plotCTStudyFreq': user_profile.plotCTStudyFreq,
                        'plotCTRequestMeanDLP': user_profile.plotCTRequestMeanDLP,
                        'plotCTRequestFreq': user_profile.plotCTRequestFreq,
                        'plotCTStudyPerDayAndHour': user_profile.plotCTStudyPerDayAndHour,
                        'plotCTStudyMeanDLPOverTime': user_profile.plotCTStudyMeanDLPOverTime,
                        'plotCTStudyMeanDLPOverTimePeriod': user_profile.plotCTStudyMeanDLPOverTimePeriod,
                        'plotMeanMedianOrBoth': user_profile.plotAverageChoice}
            chart_options_form = CTChartOptionsForm(form_data)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form}

    return render_to_response(
        'remapp/ctfiltered.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def ct_summary_chart_data(request):
    from remapp.interface.mod_filters import CTSummaryListFilter, CTFilterPlusPid
    from openremproject import settings
    from django.http import JsonResponse

    request_results = request.GET

    if request.user.groups.filter(name='pidgroup'):
        f = CTFilterPlusPid(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='CT').order_by().distinct())
    else:
        f = CTSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='CT').order_by().distinct())

    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    if user_profile.median_available and 'postgresql' in settings.DATABASES['default']['ENGINE']:
        median_available = True
    elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
        user_profile.median_available = True
        user_profile.save()
        median_available = True
    else:
        user_profile.median_available = False
        user_profile.save()
        median_available = False

    return_structure =\
        ct_plot_calculations(f, user_profile.plotCTAcquisitionFreq, user_profile.plotCTAcquisitionMeanCTDI, user_profile.plotCTAcquisitionMeanDLP,
                             user_profile.plotCTRequestFreq, user_profile.plotCTRequestMeanDLP, user_profile.plotCTStudyFreq, user_profile.plotCTStudyMeanDLP,
                             user_profile.plotCTStudyMeanDLPOverTime, user_profile.plotCTStudyMeanDLPOverTimePeriod, user_profile.plotCTStudyPerDayAndHour,
                             request_results, median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins)

    return JsonResponse(return_structure, safe=False)


def ct_plot_calculations(f, plot_acquisition_freq, plot_acquisition_mean_ctdi, plot_acquisition_mean_dlp,
                         plot_request_freq, plot_request_mean_dlp, plot_study_freq, plot_study_mean_dlp,
                         plot_study_mean_dlp_over_time, plot_study_mean_dlp_over_time_period, plot_study_per_day_and_hour,
                         request_results, median_available, plot_average_choice, plot_series_per_systems, plot_histogram_bins):
    from django.db.models import Q, Avg, Count, Min, Max, FloatField
    import datetime, qsstats
    from remapp.models import CtIrradiationEventData, Median
    if plotting:
        import numpy as np

    return_structure = {}

    # Need to exclude all Constant Angle Acquisitions when calculating data for acquisition plots, as Philips
    # Ingenuity uses same name for scan projection radiographs as the corresponding CT acquisition. Also exclude any
    # with null DLP values.
    exp_include = [o.study_instance_uid for o in f]
    acquisition_filters = {'ct_radiation_dose__general_study_module_attributes__study_instance_uid__in': exp_include}
    if request_results.get('acquisition_dlp_max'):
        acquisition_filters['dlp__lte'] = request_results.get('acquisition_dlp_max')
    if request_results.get('acquisition_dlp_min'):
        acquisition_filters['dlp__gte'] = request_results.get('acquisition_dlp_min')
    if request_results.get('acquisition_protocol'):
        acquisition_filters['acquisition_protocol__icontains'] = request_results.get('acquisition_protocol')
    if request_results.get('acquisition_ctdi_max'):
        acquisition_filters['mean_ctdivol__lte'] = request_results.get('acquisition_ctdi_max')
    if request_results.get('acquisition_ctdi_min'):
        acquisition_filters['mean_ctdivol__gte'] = request_results.get('acquisition_ctdi_min')

    if plot_acquisition_mean_dlp or plot_acquisition_mean_ctdi or plot_acquisition_freq:
        acquisition_events = CtIrradiationEventData.objects.exclude(
            ct_acquisition_type__code_meaning__exact=u'Constant Angle Acquisition'
        ).exclude(
            dlp__isnull=True
        ).filter(
            **acquisition_filters
        )
        acquisition_names = list(acquisition_events.exclude(Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values_list('acquisition_protocol', flat=True).distinct().order_by('acquisition_protocol'))
        return_structure['acquisitionNameList'] = acquisition_names

    if plot_study_mean_dlp or plot_study_freq or plot_study_mean_dlp_over_time or plot_study_per_day_and_hour:
        study_events = GeneralStudyModuleAttr.objects.exclude(
            ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
        ).exclude(
            study_description__isnull=True
        ).filter(
            study_instance_uid__in=exp_include
        )
        return_structure['studyNameList'] = list(study_events.values_list('study_description', flat=True).distinct().order_by('study_description'))

    if plot_request_mean_dlp or plot_request_freq:
        request_events = GeneralStudyModuleAttr.objects.exclude(
            ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
        ).exclude(
            requested_procedure_code_meaning__isnull=True
        ).filter(
            study_instance_uid__in=exp_include
        )
        return_structure['requestNameList'] = list(request_events.values_list('requested_procedure_code_meaning', flat=True).distinct().order_by('requested_procedure_code_meaning'))

    if plot_acquisition_mean_dlp or plot_acquisition_mean_ctdi or plot_acquisition_freq:
        if plot_series_per_systems:
            return_structure['acquisitionSystemList'] = list(acquisition_events.values_list('ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['acquisitionSystemList'] = ['All systems']

    if plot_acquisition_mean_dlp:
        return_structure['acquisitionSummary'] = []
        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        mean=Avg('dlp'),
                        median=Median('dlp') / 10000000000,
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    mean=Avg('dlp'),
                    median=Median('dlp') / 10000000000,
                    num=Count('dlp')).order_by('acquisition_protocol'))
        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        median=Median('dlp') / 10000000000,
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    median=Median('dlp') / 10000000000,
                    num=Count('dlp')).order_by('acquisition_protocol'))
        else:
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        mean=Avg('dlp'),
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    mean=Avg('dlp'),
                    num=Count('dlp')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionSummary'])):
            return_structure['acquisitionSummary'][index] = list(return_structure['acquisitionSummary'][index])

        # Fill in default values where data for an acquisition protocol is missing for any of the systems
        if plot_series_per_systems:
            for index in range(len(return_structure['acquisitionSystemList'])):
                missing_names = list(set(acquisition_names) - set([d['acquisition_protocol'] for d in return_structure['acquisitionSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['acquisitionSummary'][index]).append({'median': 0, 'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['acquisitionSummary'][index]).append({'median': 0, 'acquisition_protocol':missing_name, 'num': 0})
                    else:
                        (return_structure['acquisitionSummary'][index]).append({'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in acquisition_names:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionSummary'][index])[0])
                return_structure['acquisitionSummary'][index] = summary_temp

        return_structure['acquisitionHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(acquisition_names))] for i in xrange(len(return_structure['acquisitionSystemList']))]

        value_ranges = acquisition_events.values('acquisition_protocol').distinct().annotate(
            min_dlp=Min('dlp', output_field=FloatField()),
            max_dlp=Max('dlp', output_field=FloatField())).order_by('acquisition_protocol')

        for sys_idx, system in enumerate(return_structure['acquisitionSystemList']):
            for acq_idx, acquisition_name in enumerate(acquisition_names):
                if plot_series_per_systems:
                    subqs = acquisition_events.filter(
                            ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            acquisition_protocol=acquisition_name)
                else:
                    subqs = acquisition_events.filter(acquisition_protocol=acquisition_name)

                data_values = subqs.values_list('dlp', flat=True)

                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0], return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(acquisition_protocol=acquisition_name).values_list('min_dlp', 'max_dlp')[0])
                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0] = return_structure['acquisitionHistogramData'][sys_idx][acq_idx][0].tolist()
                return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1] = return_structure['acquisitionHistogramData'][sys_idx][acq_idx][1].tolist()

    if plot_acquisition_mean_ctdi:
        return_structure['acquisitionSummaryCTDI'] = []
        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        mean=Avg('mean_ctdivol'),
                        median=Median('mean_ctdivol') / 10000000000,
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    mean=Avg('mean_ctdivol'),
                    median=Median('mean_ctdivol') / 10000000000,
                    num=Count('dlp')).order_by('acquisition_protocol'))
        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        median=Median('mean_ctdivol') / 10000000000,
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    median=Median('mean_ctdivol') / 10000000000,
                    num=Count('dlp')).order_by('acquisition_protocol'))
        else:
            if plot_series_per_systems:
                for system in return_structure['acquisitionSystemList']:
                    return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                        Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                        ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'acquisition_protocol').distinct().annotate(
                        mean=Avg('mean_ctdivol'),
                        num=Count('dlp')).order_by('acquisition_protocol'))
            else:
                return_structure['acquisitionSummaryCTDI'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                    'acquisition_protocol').distinct().annotate(
                    mean=Avg('mean_ctdivol'),
                    num=Count('dlp')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionSummaryCTDI'])):
            return_structure['acquisitionSummaryCTDI'][index] = list(return_structure['acquisitionSummaryCTDI'][index])

        if plot_series_per_systems:
            for index in range(len(return_structure['acquisitionSystemList'])):
                missing_names = list(set(acquisition_names) - set([d['acquisition_protocol'] for d in return_structure['acquisitionSummaryCTDI'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['acquisitionSummaryCTDI'][index]).append({'median': 0, 'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['acquisitionSummaryCTDI'][index]).append({'median': 0, 'acquisition_protocol':missing_name, 'num': 0})
                    else:
                        (return_structure['acquisitionSummaryCTDI'][index]).append({'mean': 0,'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in acquisition_names:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionSummaryCTDI'][index])[0])
                return_structure['acquisitionSummaryCTDI'][index] = summary_temp

        return_structure['acquisitionHistogramDataCTDI'] = [[[None for k in xrange(2)] for j in xrange(len(acquisition_names))] for i in xrange(len(return_structure['acquisitionSystemList']))]

        value_ranges = acquisition_events.values('acquisition_protocol').distinct().annotate(
            min_ctdi=Min('mean_ctdivol', output_field=FloatField()),
            max_ctdi=Max('mean_ctdivol', output_field=FloatField())).order_by('acquisition_protocol')

        for sys_idx, system in enumerate(return_structure['acquisitionSystemList']):
            for acq_idx, acquisition_name in enumerate(acquisition_names):
                if plot_series_per_systems:
                    subqs = acquisition_events.filter(
                            ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            acquisition_protocol=acquisition_name)
                else:
                    subqs = acquisition_events.filter(acquisition_protocol=acquisition_name)

                data_values = subqs.values_list('mean_ctdivol', flat=True)

                return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][0], return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(acquisition_protocol=acquisition_name).values_list('min_ctdi', 'max_ctdi')[0])
                return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][0] = return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][0].tolist()
                return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][1] = return_structure['acquisitionHistogramDataCTDI'][sys_idx][acq_idx][1].tolist()

    if plot_acquisition_freq and not plot_acquisition_mean_dlp and not plot_acquisition_mean_ctdi:
        return_structure['acquisitionSummary'] = []
        if plot_series_per_systems:
            for system in return_structure['acquisitionSystemList']:
                return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                    Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).filter(
                    ct_radiation_dose__general_study_module_attributes__generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                    'acquisition_protocol').distinct().annotate(
                    num=Count('dlp')).order_by('acquisition_protocol'))
        else:
            return_structure['acquisitionSummary'].append(acquisition_events.exclude(
                Q(acquisition_protocol__isnull=True) | Q(acquisition_protocol='')).values(
                'acquisition_protocol').distinct().annotate(
                num=Count('dlp')).order_by('acquisition_protocol'))

        for index in range(len(return_structure['acquisitionSummary'])):
            return_structure['acquisitionSummary'][index] = list(return_structure['acquisitionSummary'][index])

        if plot_series_per_systems:
            for index in range(len(return_structure['acquisitionSystemList'])):
                missing_names = list(set(acquisition_names) - set([d['acquisition_protocol'] for d in return_structure['acquisitionSummary'][index]]))
                for missing_name in missing_names:
                    (return_structure['acquisitionSummary'][index]).append({'acquisition_protocol':missing_name, 'num': 0})
                # Rearrange the list into the same order as acquisition_names
                summary_temp = []
                for acquisition_name in acquisition_names:
                    summary_temp.append(filter(lambda item: item['acquisition_protocol'] == acquisition_name, return_structure['acquisitionSummary'][index])[0])
                return_structure['acquisitionSummary'][index] = summary_temp

    if plot_study_mean_dlp or plot_study_freq:
        if plot_series_per_systems:
            return_structure['studySystemList'] = list(study_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['studySystemList'] = ['All systems']

        return_structure['studySummary'] = []

    if plot_study_mean_dlp:
        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                        mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                        median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                    mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                    median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                    num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                    'study_description'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                        median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                    median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                    num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                    'study_description'))

        else:
            if plot_series_per_systems:
                for system in return_structure['studySystemList']:
                    return_structure['studySummary'].append(study_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                        mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'study_description'))
            else:
                return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                    mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                    num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                    'study_description'))

        for index in range(len(return_structure['studySummary'])):
            return_structure['studySummary'][index] = list(return_structure['studySummary'][index])

        if plot_series_per_systems:
            for index in range(len(return_structure['studySystemList'])):
                missing_names = list(set(return_structure['studyNameList']) - set([d['study_description'] for d in return_structure['studySummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['studySummary'][index]).append({'median': 0, 'mean': 0,'study_description':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['studySummary'][index]).append({'median': 0, 'study_description':missing_name, 'num': 0})
                    else:
                        (return_structure['studySummary'][index]).append({'mean': 0,'study_description':missing_name, 'num': 0})
                # Rearrange the list into the same order as return_structure['studyNameList']
                summary_temp = []
                for study_name in return_structure['studyNameList']:
                    summary_temp.append(filter(lambda item: item['study_description'] == study_name, return_structure['studySummary'][index])[0])
                return_structure['studySummary'][index] = summary_temp


        return_structure['studyHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['studyNameList']))] for i in xrange(len(return_structure['studySystemList']))]

        value_ranges = study_events.values('study_description').distinct().annotate(
            min_dlp=Min('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField()),
            max_dlp=Max('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField())).order_by(
            'study_description')

        for sys_idx, system in enumerate(return_structure['studySystemList']):
            for stu_idx, study_name in enumerate(return_structure['studyNameList']):
                if plot_series_per_systems:
                    subqs = study_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            study_description=study_name)
                else:
                    subqs = study_events.filter(study_description=study_name)

                data_values = subqs.values_list(
                    'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                    flat=True)
                return_structure['studyHistogramData'][sys_idx][stu_idx][0], return_structure['studyHistogramData'][sys_idx][stu_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(study_description=study_name).values_list('min_dlp', 'max_dlp')[0])
                return_structure['studyHistogramData'][sys_idx][stu_idx][0] = return_structure['studyHistogramData'][sys_idx][stu_idx][0].tolist()
                return_structure['studyHistogramData'][sys_idx][stu_idx][1] = return_structure['studyHistogramData'][sys_idx][stu_idx][1].tolist()

    elif plot_study_freq:
        if plot_series_per_systems:
            for system in return_structure['studySystemList']:
                return_structure['studySummary'].append(study_events.filter(
                    generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values('study_description').distinct().annotate(
                    num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                    'study_description'))
        else:
            return_structure['studySummary'].append(study_events.values('study_description').distinct().annotate(
                num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                'study_description'))

        for index in range(len(return_structure['studySummary'])):
            return_structure['studySummary'][index] = list(return_structure['studySummary'][index])

        # Fill in default values where data for a study description is missing for any of the systems
        if plot_series_per_systems:
            for index in range(len(return_structure['studySystemList'])):
                missing_names = list(set(return_structure['studyNameList']) - set([d['study_description'] for d in return_structure['studySummary'][index]]))
                for missing_name in missing_names:
                    (return_structure['studySummary'][index]).append({'study_description':missing_name, 'num': 0})
                # Rearrange the list into the same order as return_structure['studyNameList']
                summary_temp = []
                for study_name in return_structure['studyNameList']:
                    summary_temp.append(filter(lambda item: item['study_description'] == study_name, return_structure['studySummary'][index])[0])
                return_structure['studySummary'][index] = summary_temp

    if plot_study_mean_dlp_over_time:
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['studyMedianDLPoverTime'] = [None] * len(return_structure['studyNameList'])
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['studyMeanDLPoverTime'] = [None] * len(return_structure['studyNameList'])
        start_date = study_events.aggregate(Min('study_date')).get('study_date__min')
        today = datetime.date.today()

        for idx, study_name in enumerate(return_structure['studyNameList']):
            subqs = study_events.filter(study_description=study_name)

            if plot_average_choice == 'mean' or plot_average_choice == 'both':
                qss = qsstats.QuerySetStats(subqs, 'study_date', aggregate=Avg(
                    'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'))
                return_structure['studyMeanDLPoverTime'][idx] = qss.time_series(start_date, today,
                                                            interval=plot_study_mean_dlp_over_time_period)

            if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
                qss = qsstats.QuerySetStats(subqs, 'study_date', aggregate=Median(
                    'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000)
                return_structure['studyMedianDLPoverTime'][idx] = qss.time_series(start_date, today,
                                                                                  interval=plot_study_mean_dlp_over_time_period)

    if plot_study_per_day_and_hour:
        # Required for studies per weekday and studies per hour in each weekday plot
        return_structure['studiesPerHourInWeekdays'] = [[0 for x in range(24)] for x in range(7)]
        for day in range(7):
            study_times_on_this_weekday = study_events.filter(study_date__week_day=day + 1).values(
                'study_workload_chart_time')

            if study_times_on_this_weekday:
                qss = qsstats.QuerySetStats(study_times_on_this_weekday, 'study_workload_chart_time')
                hourly_breakdown = qss.time_series(datetime.datetime(1900, 1, 1, 0, 0),
                                                   datetime.datetime(1900, 1, 1, 23, 59), interval='hours')
                for hour in range(24):
                    return_structure['studiesPerHourInWeekdays'][day][hour] = hourly_breakdown[hour][1]

    if plot_request_mean_dlp or plot_request_freq:
        if plot_series_per_systems:
            return_structure['requestSystemList'] = list(request_events.values_list('generalequipmentmoduleattr__unique_equipment_name_id__display_name', flat=True).distinct().order_by('generalequipmentmoduleattr__unique_equipment_name_id__display_name'))
        else:
            return_structure['requestSystemList'] = ['All systems']

        return_structure['requestSummary'] = []

    if plot_request_mean_dlp:
        if median_available and plot_average_choice == 'both':
            if plot_series_per_systems:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values(
                    'requested_procedure_code_meaning').distinct().annotate(
                        mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                        median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'requested_procedure_code_meaning'))

        elif median_available and plot_average_choice == 'median':
            if plot_series_per_systems:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                            num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values(
                    'requested_procedure_code_meaning').distinct().annotate(
                        median=Median('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total') / 10000000000,
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'requested_procedure_code_meaning'))

        else:
            if plot_series_per_systems:
                for system in return_structure['requestSystemList']:
                    return_structure['requestSummary'].append(request_events.filter(
                        generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                        'requested_procedure_code_meaning').distinct().annotate(
                            mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                            num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                            'requested_procedure_code_meaning'))
            else:
                return_structure['requestSummary'].append(request_events.values(
                    'requested_procedure_code_meaning').distinct().annotate(
                        mean=Avg('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total'),
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'requested_procedure_code_meaning'))

        for index in range(len(return_structure['requestSummary'])):
            return_structure['requestSummary'][index] = list(return_structure['requestSummary'][index])

        if plot_series_per_systems:
            # Fill in default values where data for a requested procedure is missing for any of the systems
            for index in range(len(return_structure['requestSystemList'])):
                missing_names = list(set(return_structure['requestNameList']) - set([d['requested_procedure_code_meaning'] for d in return_structure['requestSummary'][index]]))
                for missing_name in missing_names:
                    if median_available and plot_average_choice == 'both':
                        (return_structure['requestSummary'][index]).append({'median': 0, 'mean': 0,'requested_procedure_code_meaning':missing_name, 'num': 0})
                    elif median_available and plot_average_choice == 'median':
                        (return_structure['requestSummary'][index]).append({'median': 0, 'requested_procedure_code_meaning':missing_name, 'num': 0})
                    else:
                        (return_structure['requestSummary'][index]).append({'mean': 0,'requested_procedure_code_meaning':missing_name, 'num': 0})
                # Rearrange the list into the same order as return_structure['requestNameList']
                summary_temp = []
                for request_name in return_structure['requestNameList']:
                    summary_temp.append(filter(lambda item: item['requested_procedure_code_meaning'] == request_name, return_structure['requestSummary'][index])[0])
                return_structure['requestSummary'][index] = summary_temp

        return_structure['requestHistogramData'] = [[[None for k in xrange(2)] for j in xrange(len(return_structure['requestNameList']))] for i in xrange(len(return_structure['requestSystemList']))]

        value_ranges = request_events.values('requested_procedure_code_meaning').distinct().annotate(
            min_dlp=Min('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField()),
            max_dlp=Max('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', output_field=FloatField())).order_by(
            'requested_procedure_code_meaning')

        for sys_idx, system in enumerate(return_structure['requestSystemList']):
            for req_idx, request_name in enumerate(return_structure['requestNameList']):
                if plot_series_per_systems:
                    subqs = request_events.filter(
                            generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).filter(
                            requested_procedure_code_meaning=request_name)
                else:
                    subqs = request_events.filter(requested_procedure_code_meaning=request_name)

                data_values = subqs.values_list(
                    'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                    flat=True)
                return_structure['requestHistogramData'][sys_idx][req_idx][0], return_structure['requestHistogramData'][sys_idx][req_idx][1] = np.histogram([float(x) for x in data_values], bins=plot_histogram_bins, range=value_ranges.filter(requested_procedure_code_meaning=request_name).values_list('min_dlp', 'max_dlp')[0])
                return_structure['requestHistogramData'][sys_idx][req_idx][0] = return_structure['requestHistogramData'][sys_idx][req_idx][0].tolist()
                return_structure['requestHistogramData'][sys_idx][req_idx][1] = return_structure['requestHistogramData'][sys_idx][req_idx][1].tolist()

    elif plot_request_freq:
        if plot_series_per_systems:
            for system in return_structure['requestSystemList']:
                return_structure['requestSummary'].append(request_events.filter(
                    generalequipmentmoduleattr__unique_equipment_name_id__display_name=system).values(
                    'requested_procedure_code_meaning').distinct().annotate(
                        num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                        'requested_procedure_code_meaning'))
        else:
            return_structure['requestSummary'].append(request_events.values('requested_procedure_code_meaning').distinct().annotate(
                num=Count('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')).order_by(
                'requested_procedure_code_meaning'))

        for index in range(len(return_structure['requestSummary'])):
            return_structure['requestSummary'][index] = list(return_structure['requestSummary'][index])

        if plot_series_per_systems:
            # Fill in default values where data for a requested procedure is missing for any of the systems
            for index in range(len(return_structure['requestSystemList'])):
                missing_names = list(set(return_structure['requestNameList']) - set([d['requested_procedure_code_meaning'] for d in return_structure['requestSummary'][index]]))
                for missing_name in missing_names:
                    (return_structure['requestSummary'][index]).append({'requested_procedure_code_meaning':missing_name, 'num': 0})
                # Rearrange the list into the same order as return_structure['requestNameList']
                summary_temp = []
                for request_name in return_structure['requestNameList']:
                    summary_temp.append(filter(lambda item: item['requested_procedure_code_meaning'] == request_name, return_structure['requestSummary'][index])[0])
                return_structure['requestSummary'][index] = summary_temp

    return return_structure


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
        user_profile = request.user.userprofile
    except:
        if request.user.is_authenticated():
            # Create a default userprofile for the user if one doesn't exist
            create_user_profile(sender=request.user, instance=request.user, created=True)
            user_profile = request.user.userprofile

    if request.user.is_authenticated():
        if homedata['mg']:
            user_profile.displayMG = True
        else:
            user_profile.displayMG = False

        if homedata['ct']:
            user_profile.displayCT = True
        else:
            user_profile.displayCT = False

        if homedata['rf']:
            user_profile.displayRF = True
        else:
            user_profile.displayRF = False

        if homedata['dx']:
            user_profile.displayDX = True
        else:
            user_profile.displayDX = False

        user_profile.save()

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


@login_required
def size_download(request, task_id):
    """View to handle downloads of files from the server

    Originally used for download of the export spreadsheets, now also used
    for downloading the patient size import logfiles.

    :param request: Used to get user group.
    :param file_name: Passes name of file to be downloaded.
    :type filename: string

    """
    import mimetypes
    import os
    from django.core.servers.basehttp import FileWrapper
    from django.utils.encoding import smart_str
    from django.shortcuts import redirect
    from django.contrib import messages
    from openremproject.settings import MEDIA_ROOT
    from remapp.models import SizeUpload
    from django.http import HttpResponse

    importperm = False
    if request.user.groups.filter(name="importsizegroup"):
        importperm = True
    try:
        exp = SizeUpload.objects.get(task_id__exact = task_id)
    except:
        messages.error(request, "Can't match the task ID, download aborted")
        return redirect('/openrem/admin/sizeimports/')

    if not importperm:
        messages.error(request, "You don't have permission to download import logs")
        return redirect('/openrem/admin/sizeimports')

    file_path = os.path.join(MEDIA_ROOT, exp.logfile.name)
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(exp.logfile)
    return response


def charts_off(request):
    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        if request.user.is_authenticated():
            # Create a default userprofile for the user if one doesn't exist
            create_user_profile(sender=request.user, instance=request.user, created=True)
            user_profile = request.user.userprofile

    # Switch chart plotting off
    user_profile.plotCharts = False
    user_profile.save()
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
