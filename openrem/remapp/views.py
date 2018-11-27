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


import csv
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import json
import logging
import remapp
from openremproject.settings import MEDIA_ROOT
from remapp.forms import SizeUploadForm
from remapp.models import GeneralStudyModuleAttr, create_user_profile
from remapp.models import SizeUpload

try:
    from numpy import *

    plotting = 1
except ImportError:
    plotting = 0


from django.template.defaultfilters import register


logger = logging.getLogger(__name__)


@register.filter
def multiply(value, arg):
    """
    Return multiplication within Django templates

    :param value: the value to multiply
    :param arg: the second value to multiply
    :return: the multiplication
    """
    try:
        value = float(value)
        arg = float(arg)
        return value * arg
    except ValueError:
        return None


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))


@login_required
def dx_summary_list_filter(request):
    from remapp.interface.mod_filters import dx_acq_filter
    from remapp.forms import DXChartOptionsForm, itemsPerPageForm
    from openremproject import settings

    pid = bool(request.user.groups.filter(name='pidgroup'))
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
            user_profile.plotSeriesPerSystem = chart_options_form.cleaned_data['plotSeriesPerSystem']
            user_profile.plotHistograms = chart_options_form.cleaned_data['plotHistograms']
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
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem,
                         'plotHistograms': user_profile.plotHistograms}
            chart_options_form = DXChartOptionsForm(form_data)

    # Obtain the number of items per page from the request
    items_per_page_form = itemsPerPageForm(request.GET)
    # check whether the form data is valid
    if items_per_page_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.itemsPerPage = items_per_page_form.cleaned_data['itemsPerPage']
            user_profile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            form_data = {'itemsPerPage': user_profile.itemsPerPage}
            items_per_page_form = itemsPerPageForm(form_data)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form, 'itemsPerPageForm': items_per_page_form}

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

    f = DXSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
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
                             user_profile.plotDXStudyPerDayAndHour,
                             median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem,
                             user_profile.plotHistogramBins, user_profile.plotHistograms,
                             user_profile.plotCaseInsensitiveCategories)

    return JsonResponse(return_structure, safe=False)


def dx_plot_calculations(f, plot_acquisition_mean_dap, plot_acquisition_freq,
                         plot_study_mean_dap, plot_study_freq,
                         plot_request_mean_dap, plot_request_freq,
                         plot_acquisition_mean_kvp_over_time, plot_acquisition_mean_mas_over_time,
                         plot_acquisition_mean_dap_over_time, plot_acquisition_mean_dap_over_time_period,
                         plot_acquisition_mean_kvp, plot_acquisition_mean_mas,
                         plot_study_per_day_and_hour,
                         median_available, plot_average_choice, plot_series_per_systems,
                         plot_histogram_bins, plot_histograms, plot_case_insensitive_categories):
    from interface.chart_functions import average_chart_inc_histogram_data, average_chart_over_time_data, workload_chart_data
    from django.utils.datastructures import MultiValueDictKeyError

    return_structure = {}

    if plot_study_mean_dap or plot_study_freq or plot_study_per_day_and_hour or plot_request_mean_dap or plot_request_freq:
        try:
            if f.form.data['acquisition_protocol']:
                exp_include = f.qs.values_list('study_instance_uid')
        except MultiValueDictKeyError:
            pass
        except KeyError:
            pass

    if plot_study_mean_dap or plot_study_freq or plot_study_per_day_and_hour:
        try:
            if f.form.data['acquisition_protocol']:
                # The user has filtered on acquisition_protocol, so need to use the slow method of querying the database
                # to avoid studies being duplicated when there is more than one of a particular acquisition type in a
                # study.
                study_events = GeneralStudyModuleAttr.objects.exclude(
                    projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
                ).filter(study_instance_uid__in=exp_include)
            else:
                # The user hasn't filtered on acquisition, so we can use the faster database querying.
                study_events = f.qs
        except MultiValueDictKeyError:
            study_events = f.qs
        except KeyError:
            pass

    if plot_request_mean_dap or plot_request_freq:
        try:
            if f.form.data['acquisition_protocol']:
                # The user has filtered on acquisition_protocol, so need to use the slow method of querying the database
                # to avoid studies being duplicated when there is more than one of a particular acquisition type in a
                # study.
                request_events = GeneralStudyModuleAttr.objects.exclude(
                    projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__isnull=True
                ).filter(study_instance_uid__in=exp_include)
            else:
                # The user hasn't filtered on acquisition, so we can use the faster database querying.
                request_events = f.qs
        except MultiValueDictKeyError:
            request_events = f.qs
        except KeyError:
            request_events = f.qs

    if plot_acquisition_mean_dap or plot_acquisition_freq:
        result = average_chart_inc_histogram_data(f.qs,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                                  'projectionxrayradiationdose__irradeventxraydata__dose_area_product',
                                                  1000000,
                                                  plot_acquisition_mean_dap, plot_acquisition_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['acquisitionSystemList'] = result['system_list']
        return_structure['acquisition_names'] = result['series_names']
        return_structure['acquisitionSummary'] = result['summary']
        if plot_acquisition_mean_dap and plot_histograms:
            return_structure['acquisitionHistogramData'] = result['histogram_data']

    if plot_request_mean_dap or plot_request_freq:
        result = average_chart_inc_histogram_data(request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'requested_procedure_code_meaning',
                                                  'projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
                                                  1000000,
                                                  plot_request_mean_dap, plot_request_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['requestSystemList'] = result['system_list']
        return_structure['request_names'] = result['series_names']
        return_structure['requestSummary'] = result['summary']
        if plot_request_mean_dap and plot_histograms:
            return_structure['requestHistogramData'] = result['histogram_data']

    if plot_study_mean_dap or plot_study_freq:
        result = average_chart_inc_histogram_data(study_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
                                                  1000000,
                                                  plot_study_mean_dap, plot_study_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['studySystemList'] = result['system_list']
        return_structure['study_names'] = result['series_names']
        return_structure['studySummary'] = result['summary']
        if plot_study_mean_dap and plot_histograms:
            return_structure['studyHistogramData'] = result['histogram_data']

    if plot_acquisition_mean_kvp:
        result = average_chart_inc_histogram_data(f.qs,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                                  'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__kvp__kvp',
                                                  1,
                                                  plot_acquisition_mean_kvp, 0,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['acquisitionkVpSystemList'] = result['system_list']
        return_structure['acquisition_kvp_names'] = result['series_names']
        return_structure['acquisitionkVpSummary'] = result['summary']
        if plot_histograms:
            return_structure['acquisitionHistogramkVpData'] = result['histogram_data']

    if plot_acquisition_mean_mas:
        result = average_chart_inc_histogram_data(f.qs,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                                  'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__exposure__exposure',
                                                  0.001,
                                                  plot_acquisition_mean_mas, 0,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['acquisitionmAsSystemList'] = result['system_list']
        return_structure['acquisition_mas_names'] = result['series_names']
        return_structure['acquisitionmAsSummary'] = result['summary']
        if plot_histograms:
            return_structure['acquisitionHistogrammAsData'] = result['histogram_data']

    if plot_acquisition_mean_dap_over_time:
        result = average_chart_over_time_data(f.qs,
                                              'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                              'projectionxrayradiationdose__irradeventxraydata__dose_area_product',
                                              'study_date',
                                              'projectionxrayradiationdose__irradeventxraydata__date_time_started',
                                              median_available, plot_average_choice,
                                              1000000, plot_acquisition_mean_dap_over_time_period,
                                              case_insensitive_categories=plot_case_insensitive_categories)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['acquisitionMedianDAPoverTime'] = result['median_over_time']
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['acquisitionMeanDAPoverTime'] = result['mean_over_time']
        if not plot_acquisition_mean_dap and not plot_acquisition_freq:
            return_structure['acquisition_names'] = result['series_names']

    if plot_acquisition_mean_kvp_over_time:
        result = average_chart_over_time_data(f.qs,
                                              'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                              'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__kvp__kvp',
                                              'study_date',
                                              'projectionxrayradiationdose__irradeventxraydata__date_time_started',
                                              median_available, plot_average_choice,
                                              1, plot_acquisition_mean_dap_over_time_period,
                                              case_insensitive_categories=plot_case_insensitive_categories)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['acquisitionMediankVpoverTime'] = result['median_over_time']
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['acquisitionMeankVpoverTime'] = result['mean_over_time']
        return_structure['acquisition_kvp_names'] = result['series_names']

    if plot_acquisition_mean_mas_over_time:
        result = average_chart_over_time_data(f.qs,
                                              'projectionxrayradiationdose__irradeventxraydata__acquisition_protocol',
                                              'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__exposure__exposure',
                                              'study_date',
                                              'projectionxrayradiationdose__irradeventxraydata__date_time_started',
                                              median_available, plot_average_choice,
                                              0.001, plot_acquisition_mean_dap_over_time_period,
                                              case_insensitive_categories=plot_case_insensitive_categories)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['acquisitionMedianmAsoverTime'] = result['median_over_time']
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['acquisitionMeanmAsoverTime'] = result['mean_over_time']
        return_structure['acquisition_mas_names'] = result['series_names']

    if plot_study_per_day_and_hour:
        result = workload_chart_data(study_events)
        return_structure['studiesPerHourInWeekdays'] = result['workload']

    return return_structure


@login_required
def dx_detail_view(request, pk=None):
    """Detail view for a DX study
    """

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except:
        messages.error(request, 'That study was not found')
        return redirect(reverse_lazy('dx_summary_list_filter'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    projection_set = study.projectionxrayradiationdose_set.get()
    events_all = projection_set.irradeventxraydata_set.select_related(
        'anatomical_structure', 'laterality', 'target_region', 'image_view',
        'patient_orientation_modifier_cid', 'acquisition_plane').all()
    accum_integrated = projection_set.accumxraydose_set.get().accumintegratedprojradiogdose_set.get()

    return render_to_response(
        'remapp/dxdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin,
         'projection_set': projection_set, 'events_all': events_all, 'accum_integrated': accum_integrated},
        context_instance=RequestContext(request)
    )


@login_required
def rf_summary_list_filter(request):
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid
    from openremproject import settings
    from remapp.forms import RFChartOptionsForm, itemsPerPageForm
    from remapp.models import HighDoseMetricAlertSettings

    if request.user.groups.filter(name='pidgroup'):
        f = RFFilterPlusPid(
            request.GET, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').order_by(
            ).distinct())
    else:
        f = RFSummaryListFilter(
            request.GET, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').order_by(
            ).distinct())

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
    chart_options_form = RFChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotRFStudyPerDayAndHour = chart_options_form.cleaned_data['plotRFStudyPerDayAndHour']
            user_profile.plotRFStudyFreq = chart_options_form.cleaned_data['plotRFStudyFreq']
            user_profile.plotRFStudyDAP = chart_options_form.cleaned_data['plotRFStudyDAP']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.plotSeriesPerSystem = chart_options_form.cleaned_data['plotSeriesPerSystem']
            user_profile.plotHistograms = chart_options_form.cleaned_data['plotHistograms']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotRFStudyPerDayAndHour': user_profile.plotRFStudyPerDayAndHour,
                         'plotRFStudyFreq': user_profile.plotRFStudyFreq,
                         'plotRFStudyDAP': user_profile.plotRFStudyDAP,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem,
                         'plotHistograms': user_profile.plotHistograms}
            chart_options_form = RFChartOptionsForm(form_data)

    # Obtain the number of items per page from the request
    items_per_page_form = itemsPerPageForm(request.GET)
    # check whether the form data is valid
    if items_per_page_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.itemsPerPage = items_per_page_form.cleaned_data['itemsPerPage']
            user_profile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            form_data = {'itemsPerPage': user_profile.itemsPerPage}
            items_per_page_form = itemsPerPageForm(form_data)

    # Import total DAP and total dose at reference point alert levels. Create with default values if not found.
    try:
        HighDoseMetricAlertSettings.objects.get()
    except ObjectDoesNotExist:
        HighDoseMetricAlertSettings.objects.create()
    alert_levels = HighDoseMetricAlertSettings.objects.values('show_accum_dose_over_delta_weeks', 'alert_total_dap_rf', 'alert_total_rp_dose_rf', 'accum_dose_delta_weeks')[0]

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}


    # # Calculate skin dose map for all objects in the database
    # import cPickle as pickle
    # import gzip
    # num_studies = f.count()
    # current_study = 0
    # for study in f:
    #     current_study += 1
    #     print "working on " + str(study.pk) + " (" + str(current_study) + " of " + str(num_studies) + ")"
    #     # Check to see if there is already a skin map pickle with the same study ID.
    #     try:
    #         study_date = study.study_date
    #         if study_date:
    #             skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', "{0:0>4}".format(study_date.year), "{0:0>2}".format(study_date.month), "{0:0>2}".format(study_date.day), 'skin_map_'+str(study.pk)+'.p')
    #         else:
    #             skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', 'skin_map_' + str(study.pk) + '.p')
    #     except:
    #         skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', 'skin_map_'+str(study.pk)+'.p')
    #
    #     from remapp.version import __skin_map_version__
    #     loaded_existing_data = False
    #     if os.path.exists(skin_map_path):
    #         with gzip.open(skin_map_path, 'rb') as pickle_file:
    #             existing_skin_map_data = pickle.load(pickle_file)
    #         try:
    #             if existing_skin_map_data['skin_map_version'] == __skin_map_version__:
    #                 loaded_existing_data = True
    #                 print str(study.pk) + " already calculated"
    #         except KeyError:
    #             pass
    #
    #     if not loaded_existing_data:
    #         from remapp.tools.make_skin_map import make_skin_map
    #         make_skin_map(study.pk)
    #         print str(study.pk) + " done"

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form, 'itemsPerPageForm': items_per_page_form, 'alertLevels': alert_levels}

    return render_to_response(
        'remapp/rffiltered.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def rf_summary_chart_data(request):
    from remapp.interface.mod_filters import RFSummaryListFilter, RFFilterPlusPid
    from openremproject import settings
    from django.http import JsonResponse

    if request.user.groups.filter(name='pidgroup'):
        f = RFFilterPlusPid(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='RF').order_by().distinct())
    else:
        f = RFSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='RF').order_by().distinct())

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
        rf_plot_calculations(f, median_available, user_profile.plotAverageChoice,
                             user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins,
                             user_profile.plotRFStudyPerDayAndHour, user_profile.plotRFStudyFreq,
                             user_profile.plotRFStudyDAP, user_profile.plotHistograms,
                             user_profile.plotCaseInsensitiveCategories)

    return JsonResponse(return_structure, safe=False)


def rf_plot_calculations(f, median_available, plot_average_choice, plot_series_per_systems,
                         plot_histogram_bins, plot_study_per_day_and_hour, plot_study_freq, plot_study_dap,
                         plot_histograms, plot_case_insensitive_categories):
    from interface.chart_functions import average_chart_inc_histogram_data, workload_chart_data

    return_structure = {}

    if plot_study_per_day_and_hour or plot_study_freq or plot_study_dap:
        # No acquisition-level filters, so can use f.qs for all charts at the moment.
        #exp_include = f.qs.values_list('study_instance_uid')
        #study_events = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=exp_include)
        study_events = f.qs

    if plot_study_per_day_and_hour:
        result = workload_chart_data(study_events)
        return_structure['studiesPerHourInWeekdays'] = result['workload']

    if plot_study_freq or plot_study_dap:
        result = average_chart_inc_histogram_data(study_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
                                                  1000000,
                                                  plot_study_dap, plot_study_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['studySystemList'] = result['system_list']
        return_structure['studyNameList'] = result['series_names']
        return_structure['studySummary'] = result['summary']
        if plot_study_dap and plot_histograms:
            return_structure['studyHistogramData'] = result['histogram_data']

    return return_structure


@login_required
def rf_detail_view(request, pk=None):
    """Detail view for an RF study
    """
    from django.db.models import Sum
    import numpy as np
    import operator
    from remapp.models import HighDoseMetricAlertSettings, SkinDoseMapCalcSettings
    from django.core.exceptions import ObjectDoesNotExist
    from datetime import timedelta

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'That study was not found')
        return redirect(reverse_lazy('rf_summary_list_filter'))

    # get the totals
    irradiation_types = [(u'Fluoroscopy',), (u'Acquisition',)]
    stu_dose_totals = [(0, 0), (0, 0)]
    stu_time_totals = [0, 0]
    total_dap = 0
    total_dose = 0
    # Iterate over the planes (for bi-plane systems, for single plane systems there is only one)
    projection_xray_dose_set = study.projectionxrayradiationdose_set.get()
    accumxraydose_set_all_planes = projection_xray_dose_set.accumxraydose_set.select_related('acquisition_plane').all()
    events_all = projection_xray_dose_set.irradeventxraydata_set.select_related(
        'irradiation_event_type', 'patient_table_relationship_cid', 'patient_orientation_cid',
        'patient_orientation_modifier_cid', 'acquisition_plane').all()
    for dose_ds in accumxraydose_set_all_planes:
        accum_dose_ds = dose_ds.accumprojxraydose_set.get()
        stu_dose_totals[0] = tuple(map(operator.add, stu_dose_totals[0],
                                       (accum_dose_ds.fluoro_dose_area_product_total*1000000,
                                        accum_dose_ds.fluoro_dose_rp_total)))
        stu_dose_totals[1] = tuple(map(operator.add, stu_dose_totals[1],
                                       (accum_dose_ds.acquisition_dose_area_product_total*1000000,
                                        accum_dose_ds.acquisition_dose_rp_total)))
        stu_time_totals[0] = stu_time_totals[0] + accum_dose_ds.total_fluoro_time
        stu_time_totals[1] = stu_time_totals[1] + accum_dose_ds.total_acquisition_time
        total_dap = total_dap + accum_dose_ds.dose_area_product_total
        total_dose = total_dose + accum_dose_ds.dose_rp_total

    # get info for different Acquisition Types
    stu_inc_totals = GeneralStudyModuleAttr.objects.filter(
            pk=pk,
            projectionxrayradiationdose__irradeventxraydata__irradiation_event_type__code_meaning__contains=
            'Acquisition'
        ).annotate(
            sum_dap=Sum('projectionxrayradiationdose__irradeventxraydata__dose_area_product')*1000000,
            sum_dose_rp=Sum('projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__dose_rp')
        ).order_by('projectionxrayradiationdose__irradeventxraydata__irradiation_event_type')
    stu_dose_totals.extend(stu_inc_totals.values_list('sum_dap', 'sum_dose_rp').order_by(
        'projectionxrayradiationdose__irradeventxraydata__irradiation_event_type'))
    acq_irr_types = stu_inc_totals.values_list(
        'projectionxrayradiationdose__irradeventxraydata__irradiation_event_type__code_meaning').order_by(
            'projectionxrayradiationdose__irradeventxraydata__irradiation_event_type').distinct()
    # stu_time_totals = [None] * len(stu_irr_types)
    for _, irr_type in enumerate(acq_irr_types):
        stu_time_totals.append(GeneralStudyModuleAttr.objects.filter(
            pk=pk,
            projectionxrayradiationdose__irradeventxraydata__irradiation_event_type__code_meaning=
            irr_type[0]).aggregate(
                Sum('projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__irradiation_duration')
            ).values()[0])
    irradiation_types.extend([(u'- ' + acq_type[0],) for acq_type in acq_irr_types])

    # Add the study totals
    irradiation_types.append((u'Total',))
    stu_dose_totals.append((total_dap*1000000, total_dose))
    # does total duration (summed over fluoroscopy and acquisitions) means something?
    stu_time_totals.append(stu_time_totals[0]+stu_time_totals[1])

    study_totals = np.column_stack((irradiation_types, stu_dose_totals, stu_time_totals)).tolist()

    try:
        SkinDoseMapCalcSettings.objects.get()
    except ObjectDoesNotExist:
        SkinDoseMapCalcSettings.objects.create()

    # Import total DAP and total dose at reference point alert levels. Create with default values if not found.
    try:
        HighDoseMetricAlertSettings.objects.get()
    except ObjectDoesNotExist:
        HighDoseMetricAlertSettings.objects.create()
    alert_levels = HighDoseMetricAlertSettings.objects.values('show_accum_dose_over_delta_weeks', 'alert_total_dap_rf', 'alert_total_rp_dose_rf', 'accum_dose_delta_weeks')[0]

    # Obtain the studies that are within delta weeks if needed
    if alert_levels['show_accum_dose_over_delta_weeks']:
        patient_id = study.patientmoduleattr_set.values_list('patient_id', flat=True)[0]
        if patient_id:
            study_date = study.study_date
            week_delta = HighDoseMetricAlertSettings.objects.values_list('accum_dose_delta_weeks', flat=True)[0]
            oldest_date = (study_date - timedelta(weeks=week_delta))
            included_studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF', patientmoduleattr__patient_id__exact=patient_id, study_date__range=[oldest_date, study_date])
        else:
            included_studies = None
    else:
        included_studies = None

    admin = {'openremversion': remapp.__version__,
             'docsversion': remapp.__docs_version__,
             'enable_skin_dose_maps': SkinDoseMapCalcSettings.objects.values_list('enable_skin_dose_maps', flat=True)[0]}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/rfdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin,
         'study_totals': study_totals,
         'projection_xray_dose_set': projection_xray_dose_set,
         'accumxraydose_set_all_planes': accumxraydose_set_all_planes,
         'events_all': events_all,
         'alert_levels': alert_levels,
         'studies_in_week_delta': included_studies},
        context_instance=RequestContext(request)
    )


@login_required
def rf_detail_view_skin_map(request, pk=None):
    """View to calculate a skin dose map. Currently just a copy of rf_detail_view
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr
    from django.http import JsonResponse
    import cPickle as pickle
    import gzip

    from django.core.exceptions import ObjectDoesNotExist
    try:
        GeneralStudyModuleAttr.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'That study was not found')
        return redirect(reverse_lazy('rf_summary_list_filter'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    # Check to see if there is already a skin map pickle with the same study ID.
    try:
        study_date = GeneralStudyModuleAttr.objects.get(pk=pk).study_date
        if study_date:
            skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', "{0:0>4}".format(study_date.year), "{0:0>2}".format(study_date.month), "{0:0>2}".format(study_date.day), 'skin_map_'+str(pk)+'.p')
        else:
            skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', 'skin_map_' + str(pk) + '.p')
    except:
        skin_map_path = os.path.join(MEDIA_ROOT, 'skin_maps', 'skin_map_'+str(pk)+'.p')

    from remapp.version import __skin_map_version__

    # If patient weight is missing from the database then db_pat_mass will be undefined
    try:
        db_pat_mass = float(GeneralStudyModuleAttr.objects.get(pk=pk).patientstudymoduleattr_set.get().patient_weight)
    except (ValueError, TypeError):
        db_pat_mass = 73.2
    if not db_pat_mass:
        db_pat_mass = 73.2

    # If patient weight is missing from the database then db_pat_mass will be undefined
    try:
        db_pat_height = float(
            GeneralStudyModuleAttr.objects.get(pk=pk).patientstudymoduleattr_set.get().patient_size) * 100
    except (ValueError, TypeError):
        db_pat_height = 178.6
    if not db_pat_height:
        db_pat_height = 178.6

    loaded_existing_data = False
    pat_mass_unchanged = False
    pat_height_unchanged = False
    if os.path.exists(skin_map_path):
        with gzip.open(skin_map_path, 'rb') as f:
            existing_skin_map_data = pickle.load(f)
        try:
            if existing_skin_map_data['skin_map_version'] == __skin_map_version__:
                # Round the float values to 1 decimal place and convert to string before comparing
                if str(round(existing_skin_map_data['patient_height'], 1)) == str(round(db_pat_height, 1)):
                    pat_height_unchanged = True

                # Round the float values to 1 decimal place and convert to string before comparing
                if str(round(existing_skin_map_data['patient_mass'], 1)) == str(round(db_pat_mass, 1)):
                    pat_mass_unchanged = True

                if pat_height_unchanged and pat_mass_unchanged:
                    return_structure = existing_skin_map_data
                    loaded_existing_data = True
        except KeyError:
            pass

    if not loaded_existing_data:
        from remapp.tools.make_skin_map import make_skin_map
        make_skin_map(pk)
        with gzip.open(skin_map_path, 'rb') as f:
            return_structure = pickle.load(f)

    return_structure['primary_key'] = pk
    return JsonResponse(return_structure, safe=False)


@login_required
def ct_summary_list_filter(request):
    from remapp.interface.mod_filters import ct_acq_filter
    from remapp.forms import CTChartOptionsForm, itemsPerPageForm
    from openremproject import settings

    pid = bool(request.user.groups.filter(name='pidgroup'))
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
            user_profile.plotCTStudyMeanCTDI = chart_options_form.cleaned_data['plotCTStudyMeanCTDI']
            user_profile.plotCTStudyFreq = chart_options_form.cleaned_data['plotCTStudyFreq']
            user_profile.plotCTStudyNumEvents = chart_options_form.cleaned_data['plotCTStudyNumEvents']
            user_profile.plotCTRequestMeanDLP = chart_options_form.cleaned_data['plotCTRequestMeanDLP']
            user_profile.plotCTRequestFreq = chart_options_form.cleaned_data['plotCTRequestFreq']
            user_profile.plotCTRequestNumEvents = chart_options_form.cleaned_data['plotCTRequestNumEvents']
            user_profile.plotCTStudyPerDayAndHour = chart_options_form.cleaned_data['plotCTStudyPerDayAndHour']
            user_profile.plotCTStudyMeanDLPOverTime = chart_options_form.cleaned_data['plotCTStudyMeanDLPOverTime']
            user_profile.plotCTStudyMeanDLPOverTimePeriod = chart_options_form.cleaned_data[
                'plotCTStudyMeanDLPOverTimePeriod']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.plotSeriesPerSystem = chart_options_form.cleaned_data['plotSeriesPerSystem']
            user_profile.plotHistograms = chart_options_form.cleaned_data['plotHistograms']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                         'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                         'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                         'plotCTStudyMeanDLP': user_profile.plotCTStudyMeanDLP,
                         'plotCTStudyMeanCTDI': user_profile.plotCTStudyMeanCTDI,
                         'plotCTStudyFreq': user_profile.plotCTStudyFreq,
                         'plotCTStudyNumEvents': user_profile.plotCTStudyNumEvents,
                         'plotCTRequestMeanDLP': user_profile.plotCTRequestMeanDLP,
                         'plotCTRequestFreq': user_profile.plotCTRequestFreq,
                         'plotCTRequestNumEvents': user_profile.plotCTRequestNumEvents,
                         'plotCTStudyPerDayAndHour': user_profile.plotCTStudyPerDayAndHour,
                         'plotCTStudyMeanDLPOverTime': user_profile.plotCTStudyMeanDLPOverTime,
                         'plotCTStudyMeanDLPOverTimePeriod': user_profile.plotCTStudyMeanDLPOverTimePeriod,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem,
                         'plotHistograms': user_profile.plotHistograms}
            chart_options_form = CTChartOptionsForm(form_data)

    # Obtain the number of items per page from the request
    items_per_page_form = itemsPerPageForm(request.GET)
    # check whether the form data is valid
    if items_per_page_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.itemsPerPage = items_per_page_form.cleaned_data['itemsPerPage']
            user_profile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            form_data = {'itemsPerPage': user_profile.itemsPerPage}
            items_per_page_form = itemsPerPageForm(form_data)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form, 'itemsPerPageForm': items_per_page_form}

    return render_to_response(
        'remapp/ctfiltered.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def ct_summary_chart_data(request):
    from remapp.interface.mod_filters import ct_acq_filter
    from openremproject import settings
    from django.http import JsonResponse

    pid = bool(request.user.groups.filter(name='pidgroup'))
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

    return_structure =\
        ct_plot_calculations(f, user_profile.plotCTAcquisitionFreq, user_profile.plotCTAcquisitionMeanCTDI, user_profile.plotCTAcquisitionMeanDLP,
                             user_profile.plotCTRequestFreq, user_profile.plotCTRequestMeanDLP, user_profile.plotCTRequestNumEvents,
                             user_profile.plotCTStudyFreq, user_profile.plotCTStudyMeanDLP, user_profile.plotCTStudyMeanCTDI, user_profile.plotCTStudyNumEvents,
                             user_profile.plotCTStudyMeanDLPOverTime, user_profile.plotCTStudyMeanDLPOverTimePeriod, user_profile.plotCTStudyPerDayAndHour,
                             median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem,
                             user_profile.plotHistogramBins, user_profile.plotHistograms, user_profile.plotCaseInsensitiveCategories)

    return JsonResponse(return_structure, safe=False)


def ct_plot_calculations(f, plot_acquisition_freq, plot_acquisition_mean_ctdi, plot_acquisition_mean_dlp,
                         plot_request_freq, plot_request_mean_dlp, plot_request_num_events,
                         plot_study_freq, plot_study_mean_dlp, plot_study_mean_ctdi, plot_study_num_events,
                         plot_study_mean_dlp_over_time, plot_study_mean_dlp_over_time_period, plot_study_per_day_and_hour,
                         median_available, plot_average_choice, plot_series_per_systems, plot_histogram_bins,
                         plot_histograms, plot_case_insensitive_categories):
    from interface.chart_functions import average_chart_inc_histogram_data, average_chart_over_time_data, workload_chart_data

    return_structure = {}

    if plot_study_mean_dlp or plot_study_mean_ctdi or plot_study_freq or plot_study_num_events or plot_study_mean_dlp_over_time or plot_study_per_day_and_hour or plot_request_mean_dlp or plot_request_freq or plot_request_num_events:
        prefetch_list = ['generalequipmentmoduleattr__unique_equipment_name_id__display_name']
        if plot_study_mean_dlp or plot_study_freq or plot_study_mean_ctdi or plot_study_num_events or plot_study_mean_dlp_over_time or plot_study_per_day_and_hour:
            prefetch_list.append('study_description')
        if plot_study_mean_dlp or plot_study_freq or plot_request_mean_dlp or plot_request_freq:
            prefetch_list.append('ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')
        if plot_study_mean_ctdi:
            prefetch_list.append('ctradiationdose__ctirradiationeventdata__mean_ctdivol')
        if plot_study_num_events:
            prefetch_list.append('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events')
        if plot_study_mean_dlp_over_time:
            prefetch_list.append('study_date')
        if plot_request_freq or plot_request_mean_dlp or plot_request_num_events:
            prefetch_list.append('requested_procedure_code_meaning')
        if plot_request_num_events:
            prefetch_list.append('ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events')

        if ('acquisition_protocol' in f.form.data and f.form.data['acquisition_protocol']) or ('ct_acquisition_type' in f.form.data and f.form.data['ct_acquisition_type']):
            # The user has filtered on acquisition_protocol, so need to use the slow method of querying the database
            # to avoid studies being duplicated when there is more than one of a particular acquisition type in a
            # study.
            try:
                exp_include = f.qs.values_list('study_instance_uid')
                study_and_request_events = GeneralStudyModuleAttr.objects.exclude(
                    ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
                ).filter(study_instance_uid__in=exp_include).values(*prefetch_list)
            except KeyError:
                study_and_request_events = f.qs.values(*prefetch_list)
        else:
            # The user hasn't filtered on acquisition, so we can use the faster database querying.
            study_and_request_events = f.qs.values(*prefetch_list)

    if plot_acquisition_mean_dlp or plot_acquisition_freq or plot_acquisition_mean_ctdi:
        prefetch_list = ['generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                         'ctradiationdose__ctirradiationeventdata__acquisition_protocol']
        if plot_acquisition_mean_dlp:
            prefetch_list.append('ctradiationdose__ctirradiationeventdata__dlp')
        if plot_acquisition_mean_ctdi:
            prefetch_list.append('ctradiationdose__ctirradiationeventdata__mean_ctdivol')

        if plot_histograms and 'ct_acquisition_type' in f.form.data and f.form.data['ct_acquisition_type']:
            # The user has filtered on acquisition_protocol, so need to use the slow method of querying the database
            # to avoid studies being duplicated when there is more than one of a particular acquisition type in a
            # study.
            try:
                exp_include = f.qs.values_list('study_instance_uid')
                acquisition_events = GeneralStudyModuleAttr.objects.exclude(
                    ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total__isnull=True
                ).filter(study_instance_uid__in=exp_include,
                         ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__iexact=f.form.data['ct_acquisition_type']).values(*prefetch_list)
            except KeyError:
                acquisition_events = f.qs.values(*prefetch_list)
        else:
            acquisition_events = f.qs.values(*prefetch_list)

    if plot_acquisition_mean_dlp or plot_acquisition_freq:
        result = average_chart_inc_histogram_data(acquisition_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'ctradiationdose__ctirradiationeventdata__acquisition_protocol',
                                                  'ctradiationdose__ctirradiationeventdata__dlp',
                                                  1,
                                                  plot_acquisition_mean_dlp, plot_acquisition_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  exclude_constant_angle=True,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['acquisitionSystemList'] = result['system_list']
        return_structure['acquisitionNameList'] = result['series_names']
        return_structure['acquisitionSummary'] = result['summary']
        if plot_acquisition_mean_dlp and plot_histograms:
            return_structure['acquisitionHistogramData'] = result['histogram_data']

    if plot_acquisition_mean_ctdi:
        result = average_chart_inc_histogram_data(acquisition_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'ctradiationdose__ctirradiationeventdata__acquisition_protocol',
                                                  'ctradiationdose__ctirradiationeventdata__mean_ctdivol',
                                                  1,
                                                  plot_acquisition_mean_ctdi, plot_acquisition_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  exclude_constant_angle=True,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['acquisitionSystemListCTDI'] = result['system_list']
        return_structure['acquisitionNameListCTDI'] = result['series_names']
        return_structure['acquisitionSummaryCTDI'] = result['summary']
        if plot_histograms:
            return_structure['acquisitionHistogramDataCTDI'] = result['histogram_data']

    if plot_study_mean_dlp or plot_study_freq:
        result = average_chart_inc_histogram_data(study_and_request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                                                  1,
                                                  plot_study_mean_dlp, plot_study_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['studySystemList'] = result['system_list']
        return_structure['studyNameList'] = result['series_names']
        return_structure['studySummary'] = result['summary']
        if plot_study_mean_dlp and plot_histograms:
            return_structure['studyHistogramData'] = result['histogram_data']

    if plot_study_mean_ctdi:
        result = average_chart_inc_histogram_data(study_and_request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'ctradiationdose__ctirradiationeventdata__mean_ctdivol',
                                                  1,
                                                  plot_study_mean_ctdi, 0,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  exclude_constant_angle=True,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['studySystemListCTDI'] = result['system_list']
        return_structure['studyNameListCTDI'] = result['series_names']
        return_structure['studySummaryCTDI'] = result['summary']
        if plot_histograms:
            return_structure['studyHistogramDataCTDI'] = result['histogram_data']

    if plot_study_num_events:
        result = average_chart_inc_histogram_data(study_and_request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events',
                                                  1,
                                                  plot_study_num_events, 0,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['studySummaryNumEvents'] = result['summary']
        if not plot_study_mean_dlp and not plot_study_freq:
            return_structure['studySystemList'] = result['system_list']
            return_structure['studyNameList'] = result['series_names']
        if plot_study_num_events and plot_histograms:
            return_structure['studyHistogramDataNumEvents'] = result['histogram_data']

    if plot_request_mean_dlp or plot_request_freq:
        result = average_chart_inc_histogram_data(study_and_request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'requested_procedure_code_meaning',
                                                  'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                                                  1,
                                                  plot_request_mean_dlp, plot_request_freq,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['requestSystemList'] = result['system_list']
        return_structure['requestNameList'] = result['series_names']
        return_structure['requestSummary'] = result['summary']
        if plot_request_mean_dlp and plot_histograms:
            return_structure['requestHistogramData'] = result['histogram_data']

    if plot_request_num_events:
        result = average_chart_inc_histogram_data(study_and_request_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'requested_procedure_code_meaning',
                                                  'ctradiationdose__ctaccumulateddosedata__total_number_of_irradiation_events',
                                                  1,
                                                  plot_request_num_events, 0,
                                                  plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins,
                                                  calculate_histograms=plot_histograms,
                                                  case_insensitive_categories=plot_case_insensitive_categories)

        return_structure['requestSummaryNumEvents'] = result['summary']
        if not plot_request_mean_dlp and not plot_request_freq:
            return_structure['requestSystemList'] = result['system_list']
            return_structure['requestNameList'] = result['series_names']
        if plot_request_num_events and plot_histograms:
            return_structure['requestHistogramDataNumEvents'] = result['histogram_data']

    if plot_study_mean_dlp_over_time:
        result = average_chart_over_time_data(study_and_request_events,
                                              'study_description',
                                              'ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total',
                                              'study_date', 'study_date',
                                              median_available, plot_average_choice,
                                              1, plot_study_mean_dlp_over_time_period,
                                              case_insensitive_categories=plot_case_insensitive_categories)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['studyMedianDLPoverTime'] = result['median_over_time']
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['studyMeanDLPoverTime'] = result['mean_over_time']
        if not plot_study_mean_dlp and not plot_study_freq:
            return_structure['studyNameList'] = result['series_names']

    if plot_study_per_day_and_hour:
        result = workload_chart_data(study_and_request_events)
        return_structure['studiesPerHourInWeekdays'] = result['workload']

    return return_structure


@login_required
def ct_detail_view(request, pk=None):
    """Detail view for a CT study
    """
    from django.contrib import messages
    from remapp.models import GeneralStudyModuleAttr

    try:
        study = GeneralStudyModuleAttr.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'That study was not found')
        return redirect(reverse_lazy('ct_summary_list_filter'))

    events_all = study.ctradiationdose_set.get().ctirradiationeventdata_set.select_related(
        'ct_acquisition_type', 'ctdiw_phantom_type').all()

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return render_to_response(
        'remapp/ctdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin, 'events_all': events_all},
        context_instance=RequestContext(request)
    )


@login_required
def mg_summary_list_filter(request):
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    from openremproject import settings
    from remapp.forms import MGChartOptionsForm, itemsPerPageForm

    filter_data = request.GET.copy()
    if 'page' in filter_data:
        del filter_data['page']

    if request.user.groups.filter(name='pidgroup'):
        f = MGFilterPlusPid(
            filter_data, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='MG').order_by(
            ).distinct())
    else:
        f = MGSummaryListFilter(
            filter_data, queryset=GeneralStudyModuleAttr.objects.filter(modality_type__exact='MG').order_by(
            ).distinct())

    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        user_profile.median_available = True
        user_profile.save()
    else:
        user_profile.median_available = False
        user_profile.save()

    # Obtain the chart options from the request
    chart_options_form = MGChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotMGStudyPerDayAndHour = chart_options_form.cleaned_data['plotMGStudyPerDayAndHour']
            user_profile.plotMGAGDvsThickness = chart_options_form.cleaned_data['plotMGAGDvsThickness']
            user_profile.plotMGkVpvsThickness = chart_options_form.cleaned_data['plotMGkVpvsThickness']
            user_profile.plotMGmAsvsThickness = chart_options_form.cleaned_data['plotMGmAsvsThickness']
            user_profile.plotSeriesPerSystem = chart_options_form.cleaned_data['plotSeriesPerSystem']
            # Uncomment the following line when there's at least one bar chart for mammo
            #user_profile.plotHistograms = chart_options_form.cleaned_data['plotHistograms']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotMGStudyPerDayAndHour': user_profile.plotMGStudyPerDayAndHour,
                         'plotMGAGDvsThickness': user_profile.plotMGAGDvsThickness,
                         'plotMGkVpvsThickness': user_profile.plotMGkVpvsThickness,
                         'plotMGmAsvsThickness': user_profile.plotMGmAsvsThickness,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem}
                         # Uncomment the following line when there's at least one bar chart for mammo
                         #'plotHistograms': user_profile.plotHistograms}
            chart_options_form = MGChartOptionsForm(form_data)

    # Obtain the number of items per page from the request
    items_per_page_form = itemsPerPageForm(request.GET)
    # check whether the form data is valid
    if items_per_page_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.itemsPerPage = items_per_page_form.cleaned_data['itemsPerPage']
            user_profile.save()

        # If submit was not clicked then use the settings already stored in the user's profile
        else:
            form_data = {'itemsPerPage': user_profile.itemsPerPage}
            items_per_page_form = itemsPerPageForm(form_data)

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'filter': f, 'admin': admin, 'chartOptionsForm': chart_options_form, 'itemsPerPageForm': items_per_page_form}

    return render_to_response(
        'remapp/mgfiltered.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def mg_summary_chart_data(request):
    from remapp.interface.mod_filters import MGSummaryListFilter, MGFilterPlusPid
    from openremproject import settings
    from django.http import JsonResponse

    if request.user.groups.filter(name='pidgroup'):
        f = MGFilterPlusPid(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='MG').order_by().distinct())
    else:
        f = MGSummaryListFilter(request.GET, queryset=GeneralStudyModuleAttr.objects.filter(
            modality_type__exact='MG').order_by().distinct())

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
        mg_plot_calculations(f, median_available, user_profile.plotAverageChoice,
                             user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins,
                             user_profile.plotMGStudyPerDayAndHour, user_profile.plotMGAGDvsThickness,
                             user_profile.plotMGkVpvsThickness, user_profile.plotMGmAsvsThickness)

    return JsonResponse(return_structure, safe=False)


def mg_plot_calculations(f, median_available, plot_average_choice, plot_series_per_systems,
                         plot_histogram_bins, plot_study_per_day_and_hour, plot_agd_vs_thickness,
                         plot_kvp_vs_thickness, plot_mas_vs_thickness):
    from interface.chart_functions import workload_chart_data, scatter_plot_data

    return_structure = {}

    if plot_study_per_day_and_hour:
        # No acquisition-level filters, so can use f.qs for all charts at the moment.
        # exp_include = f.qs.values_list('study_instance_uid')
        # study_events = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=exp_include)
        study_events = f.qs

        result = workload_chart_data(study_events)
        return_structure['studiesPerHourInWeekdays'] = result['workload']

    if plot_agd_vs_thickness:
        result = scatter_plot_data(f.qs,
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraymechanicaldata__compression_thickness',
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__average_glandular_dose',
                                   1,
                                   plot_series_per_systems,
                                   'generalequipmentmoduleattr__unique_equipment_name_id__display_name')
        return_structure['AGDvsThickness'] = result['scatterData']
        return_structure['maxThicknessAndAGD'] = result['maxXandY']
        return_structure['AGDvsThicknessSystems'] = result['system_list']

    if plot_kvp_vs_thickness:
        result = scatter_plot_data(f.qs,
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraymechanicaldata__compression_thickness',
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__kvp__kvp',
                                   1,
                                   plot_series_per_systems,
                                   'generalequipmentmoduleattr__unique_equipment_name_id__display_name')
        return_structure['kVpvsThickness'] = result['scatterData']
        return_structure['maxThicknessAndkVp'] = result['maxXandY']
        return_structure['kVpvsThicknessSystems'] = result['system_list']

    if plot_mas_vs_thickness:
        result = scatter_plot_data(f.qs,
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraymechanicaldata__compression_thickness',
                                   'projectionxrayradiationdose__irradeventxraydata__irradeventxraysourcedata__exposure__exposure',
                                   0.001,
                                   plot_series_per_systems,
                                   'generalequipmentmoduleattr__unique_equipment_name_id__display_name')
        return_structure['mAsvsThickness'] = result['scatterData']
        return_structure['maxThicknessAndmAs'] = result['maxXandY']
        return_structure['mAsvsThicknessSystems'] = result['system_list']

    return return_structure


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
        return redirect(reverse_lazy('mg_summary_list_filter'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    projection_xray_dose_set = study.projectionxrayradiationdose_set.get()
    accum_mammo_set = projection_xray_dose_set.accumxraydose_set.get().accummammographyxraydose_set.select_related(
        'laterality').all()
    events_all = projection_xray_dose_set.irradeventxraydata_set.select_related(
        'laterality', 'image_view').all()

    return render_to_response(
        'remapp/mgdetail.html',
        {'generalstudymoduleattr': study, 'admin': admin,
         'projection_xray_dose_set': projection_xray_dose_set,
         'accum_mammo_set': accum_mammo_set,
         'events_all': events_all},
        context_instance=RequestContext(request)
    )


def openrem_home(request):
    from remapp.models import PatientIDSettings, DicomDeleteSettings, AdminTaskQuestions, HomePageAdminSettings
    from django.db.models import Q  # For the Q "OR" query used for DX and CR
    from collections import OrderedDict

    try:
        HomePageAdminSettings.objects.get()
    except ObjectDoesNotExist:
        HomePageAdminSettings.objects.create()

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

    try:
        # See if the user has plot settings in userprofile
        user_profile = request.user.userprofile
    except:
        if request.user.is_authenticated():
            # Create a default userprofile for the user if one doesn't exist
            create_user_profile(sender=request.user, instance=request.user, created=True)
            user_profile = request.user.userprofile

    allstudies = GeneralStudyModuleAttr.objects.all()
    modalities = OrderedDict()
    modalities['CT'] = {'name': 'CT', 'count': allstudies.filter(modality_type__exact='CT').count()}
    modalities['RF'] = {'name': 'Fluoroscopy', 'count': allstudies.filter(modality_type__exact='RF').count()}
    modalities['MG'] = {'name': 'Mammography', 'count': allstudies.filter(modality_type__exact='MG').count()}
    modalities['DX'] = {'name': 'Radiography', 'count': allstudies.filter(
        Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).count()}

    mods_to_delete = []
    for modality in modalities:
        if not modalities[modality]['count']:
            mods_to_delete += [modality,]
            if request.user.is_authenticated():
                setattr(user_profile, "display{0}".format(modality), False)
        else:
            if request.user.is_authenticated():
                setattr(user_profile, "display{0}".format(modality), True)
    if request.user.is_authenticated():
        user_profile.save()

    for modality in mods_to_delete:
        del modalities[modality]

    homedata = {
        'total': allstudies.count(),
    }

    # Determine whether to calculate workload settings
    display_workload_stats = HomePageAdminSettings.objects.values_list('enable_workload_stats', flat=True)[0]
    home_config = {'display_workload_stats': display_workload_stats}
    if display_workload_stats:
        if request.user.is_authenticated():
            home_config['day_delta_a'] = user_profile.summaryWorkloadDaysA
            home_config['day_delta_b'] = user_profile.summaryWorkloadDaysB
        else:
            home_config['day_delta_a'] = 7
            home_config['day_delta_b'] = 28

    admin = dict(openremversion=remapp.__version__, docsversion=remapp.__docs_version__)

    for group in request.user.groups.all():
        admin[group.name] = True

    admin_questions = {}
    admin_questions_true = False
    if request.user.groups.filter(name="admingroup"):
        not_patient_indicator_question = AdminTaskQuestions.get_solo().ask_revert_to_074_question
        admin_questions['not_patient_indicator_question'] = not_patient_indicator_question
        # if any(value for value in admin_questions.itervalues()):
        #     admin_questions_true = True  # Don't know why this doesn't work
        if not_patient_indicator_question:
            admin_questions_true = True  # Doing this instead

    #from remapp.tools.send_high_dose_alert_emails import send_rf_high_dose_alert_email
    #send_rf_high_dose_alert_email(417637)
    #send_rf_high_dose_alert_email(417973)
    # # Send a test e-mail
    # from django.core.mail import send_mail
    # from openremproject import settings
    # from remapp.models import HighDoseMetricAlertSettings
    # from django.contrib.auth.models import User
    #
    # try:
    #     HighDoseMetricAlertSettings.objects.get()
    # except ObjectDoesNotExist:
    #     HighDoseMetricAlertSettings.objects.create()
    #
    # send_alert_emails = HighDoseMetricAlertSettings.objects.values_list('send_high_dose_metric_alert_emails', flat=True)[0]
    # if send_alert_emails:
    #     recipients = User.objects.filter(highdosemetricalertrecipients__receive_high_dose_metric_alerts__exact=True).values_list('email', flat=True)
    #     send_mail('OpenREM high dose alert test',
    #               'This is a test for high dose alert e-mails from OpenREM',
    #               settings.EMAIL_DOSE_ALERT_SENDER,
    #               recipients,
    #               fail_silently=False)
    # # End of sending a test e-mail

    return render(request, "remapp/home.html",
                  {'homedata': homedata, 'admin': admin, 'users_in_groups': users_in_groups,
                   'admin_questions': admin_questions, 'admin_questions_true': admin_questions_true,
                   'modalities': modalities, 'home_config': home_config})


@csrf_exempt
def update_modality_totals(request):
    """AJAX function to update study numbers automatically

    :param request: request object
    :return: dictionary of totals
    """
    from django.db.models import Q

    if request.is_ajax():
        allstudies = GeneralStudyModuleAttr.objects.all()
        resp = {
            'total': allstudies.count(),
            'total_mg': allstudies.filter(modality_type__exact='MG').count(),
            'total_ct': allstudies.filter(modality_type__exact='CT').count(),
            'total_rf': allstudies.filter(modality_type__contains='RF').count(),
            'total_dx': allstudies.filter(Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).count(),
        }

        return HttpResponse(json.dumps(resp), content_type="application/json")


@csrf_exempt
def update_latest_studies(request):
    """AJAX function to calculate the latest studies for each display name for a particular modality.

    :param request: Request object
    :return: HTML table of modalities
    """
    from django.db.models import Q, Min
    from datetime import datetime
    from collections import OrderedDict
    from remapp.models import HomePageAdminSettings

    if request.is_ajax():
        data = request.POST
        modality = data.get('modality')
        if modality == 'DX':
            studies = GeneralStudyModuleAttr.objects.filter(
                Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).all()
        else:
            studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact=modality).all()

        display_names = studies.values_list(
            'generalequipmentmoduleattr__unique_equipment_name__display_name').distinct().annotate(
            pk_value=Min('generalequipmentmoduleattr__unique_equipment_name__pk'))

        modalitydata = {}

        if request.user.is_authenticated():
            day_delta_a = request.user.userprofile.summaryWorkloadDaysA
            day_delta_b = request.user.userprofile.summaryWorkloadDaysB
        else:
            day_delta_a = 7
            day_delta_b = 28

        for display_name, pk in display_names:
            display_name_studies = studies.filter(generalequipmentmoduleattr__unique_equipment_name__display_name__exact=display_name)
            latestdate = display_name_studies.latest('study_date').study_date
            latestuid = display_name_studies.filter(study_date__exact=latestdate).latest('study_time')
            latestdatetime = datetime.combine(latestuid.study_date, latestuid.study_time)

            try:
                displayname = display_name.encode('utf-8')
            except AttributeError:
                displayname = u"Unexpected display name non-ASCII issue"

            modalitydata[display_name] = {
                'total': display_name_studies.count(),
                'latest': latestdatetime,
                'displayname': displayname,
                'displayname_pk': modality.lower() + str(pk)
            }
        ordereddata = OrderedDict(sorted(modalitydata.items(), key=lambda t: t[1]['latest'], reverse=True))

        admin = {}
        for group in request.user.groups.all():
            admin[group.name] = True

        template = 'remapp/home-list-modalities.html'
        data = ordereddata

        display_workload_stats = HomePageAdminSettings.objects.values_list('enable_workload_stats', flat=True)[0]
        home_config = {
            'display_workload_stats': display_workload_stats,
            'day_delta_a': day_delta_a,
            'day_delta_b': day_delta_b
        }

        return render(request, template, {'data': data, 'modality': modality.lower(), 'home_config': home_config,
                                          'admin': admin})


@csrf_exempt
def update_study_workload(request):
    """AJAX function to calculate the number of studies in two user-defined time periods for a particular modality.

    :param request: Request object
    :return: HTML table of modalities
    """
    from django.db.models import Q, Min
    from datetime import datetime, timedelta
    from collections import OrderedDict

    if request.is_ajax():
        data = request.POST
        modality = data.get('modality')
        if modality == 'DX':
            studies = GeneralStudyModuleAttr.objects.filter(
                Q(modality_type__exact='DX') | Q(modality_type__exact='CR')).all()
        else:
            studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact=modality).all()

        display_names = studies.values_list(
            'generalequipmentmoduleattr__unique_equipment_name__display_name').distinct().annotate(
            pk_value=Min('generalequipmentmoduleattr__unique_equipment_name__pk'))

        modalitydata = {}

        if request.user.is_authenticated():
            day_delta_a = request.user.userprofile.summaryWorkloadDaysA
            day_delta_b = request.user.userprofile.summaryWorkloadDaysB
        else:
            day_delta_a = 7
            day_delta_b = 28

        today = datetime.now()
        date_a = (today - timedelta(days=day_delta_a))
        date_b = (today - timedelta(days=day_delta_b))

        for display_name, pk in display_names:
            display_name_studies = studies.filter(generalequipmentmoduleattr__unique_equipment_name__display_name__exact=display_name)

            try:
                displayname = display_name.encode('utf-8')
            except AttributeError:
                displayname = u"Unexpected display name non-ASCII issue"

            modalitydata[display_name] = {
                'studies_in_past_days_a': display_name_studies.filter(study_date__range=[date_a, today]).count(),
                'studies_in_past_days_b': display_name_studies.filter(study_date__range=[date_b, today]).count(),
                'displayname': displayname,
                'displayname_pk': modality.lower() + str(pk)
            }
        data = OrderedDict(sorted(modalitydata.items(), key=lambda t: t[1]['displayname_pk'], reverse=True))

        template = 'remapp/home-modality-workload.html'

        return render(request, template, {'data': data, 'modality': modality.lower()})


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
        return redirect(reverse_lazy('home'))


@login_required
def size_upload(request):
    """Form for upload of csv file containing patient size information. POST request passes database entry ID to size_process

    :param request: If POST, contains the file upload information
    """

    if not request.user.groups.filter(name="importsizegroup"):
        messages.error(request, "You are not in the import size group - please contact your administrator")
        return redirect(reverse_lazy('home'))

    # Handle file upload
    if request.method == 'POST' and request.user.groups.filter(name="importsizegroup"):
        form = SizeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newcsv = SizeUpload(sizefile=request.FILES['sizefile'])
            newcsv.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse_lazy('size_process', kwargs={'pk': newcsv.id}))

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
        return redirect(reverse_lazy('home'))

    if request.method == 'POST':

        itemsInPost = len(request.POST.values())
        uniqueItemsInPost = len(set(request.POST.values()))

        if itemsInPost == uniqueItemsInPost:
            csvrecord = SizeUpload.objects.all().filter(id__exact=kwargs['pk'])[0]

            if not csvrecord.sizefile:
                messages.error(request, "File to be processed doesn't exist. Do you wish to try again?")
                return HttpResponseRedirect(reverse_lazy('size_upload'))

            csvrecord.height_field = request.POST['height_field']
            csvrecord.weight_field = request.POST['weight_field']
            csvrecord.id_field = request.POST['id_field']
            csvrecord.id_type = request.POST['id_type']
            csvrecord.save()

            websizeimport.delay(csv_pk=kwargs['pk'])

            return HttpResponseRedirect(reverse_lazy('size_imports'))

        else:
            messages.error(request, "Duplicate column header selection. Each field must have a different header.")
            return HttpResponseRedirect(reverse_lazy('size_process', kwargs={'pk': kwargs['pk']}))

    else:

        csvrecord = SizeUpload.objects.all().filter(id__exact=kwargs['pk'])
        with open(os.path.join(MEDIA_ROOT, csvrecord[0].sizefile.name), 'rb') as csvfile:
            try:
                # dialect = csv.Sniffer().sniff(csvfile.read(1024))
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
                    return HttpResponseRedirect(reverse_lazy('size_upload'))
            except csv.Error as e:
                messages.error(request,
                               "Doesn't appear to be a csv file. Error({0}). The uploaded file has been deleted.".format(
                                   e))
                csvrecord[0].sizefile.delete()
                return HttpResponseRedirect(reverse_lazy('size_upload'))
            except:
                messages.error(request,
                               "Unexpected error - please contact an administrator: {0}.".format(sys.exc_info()[0]))
                csvrecord[0].sizefile.delete()
                return HttpResponseRedirect(reverse_lazy('size_upload'))

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
    if not request.user.groups.filter(name="importsizegroup") and not request.user.groups.filter(name="admingroup"):
        messages.error(request, "You are not in the import size group - please contact your administrator")
        return redirect(reverse_lazy('home'))

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
    from django.core.urlresolvers import reverse
    from django.contrib import messages

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

    return HttpResponseRedirect(reverse('size_imports'))


@login_required
def size_abort(request, pk):
    """View to abort current patient size imports

    :param request: Contains the task primary key
    :type request: POST
    """
    from celery.task.control import revoke
    from remapp.models import SizeUpload

    size_import = get_object_or_404(SizeUpload, pk=pk)

    if request.user.groups.filter(name="importsizegroup") or request.users.groups.filter(name="admingroup"):
        revoke(size_import.task_id, terminate=True)
        size_import.logfile.delete()
        size_import.sizefile.delete()
        size_import.delete()
    else:
        messages.error(request, "Only members of the importsizegroup or admingroup can abort a size import task")

    return HttpResponseRedirect(reverse_lazy('size_imports'))


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
    from django.core.servers.basehttp import FileWrapper
    from django.utils.encoding import smart_str

    importperm = False
    if request.user.groups.filter(name="importsizegroup"):
        importperm = True
    try:
        exp = SizeUpload.objects.get(task_id__exact = task_id)
    except:
        messages.error(request, "Can't match the task ID, download aborted")
        return redirect(reverse_lazy('size_imports'))

    if not importperm:
        messages.error(request, "You don't have permission to download import logs")
        return redirect(reverse_lazy('size_imports'))

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
    return redirect((request.META['HTTP_REFERER']).replace('&plotCharts=on', ''))


@login_required
def display_names_view(request):
    from django.db.models import Q
    from remapp.models import UniqueEquipmentNames

    f = UniqueEquipmentNames.objects.order_by('display_name')

    # if user_defined_modality is filled, we should use this value, otherwise the value of modality type in the general_study module
    # so we look if the concatenation of the user_defined_modality (empty if not used) and modality_type starts with a specific modality type
    ct_names = f.filter(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CT").distinct()
    mg_names = f.filter(generalequipmentmoduleattr__general_study_module_attributes__modality_type="MG").distinct()
    dx_names = f.filter(Q(user_defined_modality="DX") | Q(user_defined_modality="dual") | (
            Q(user_defined_modality__isnull=True) & (
            Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") |
            Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR")))).distinct()
    rf_names = f.filter(Q(user_defined_modality="RF") | Q(user_defined_modality="dual") | (
            Q(user_defined_modality__isnull=True) &
            Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF"))).distinct()
    ot_names = f.filter(~Q(user_defined_modality__isnull=True) | (
            ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF") &
            ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="MG") &
            ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CT") &
            ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") &
            ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR"))).distinct()

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'name_list': f, 'admin': admin,
                        'ct_names': ct_names, 'mg_names': mg_names, 'dx_names': dx_names, 'rf_names': rf_names,
                        'ot_names': ot_names, 'modalities': ['CT', 'RF', 'MG', 'DX', 'OT']}

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
def display_name_update(request):
    from remapp.models import UniqueEquipmentNames
    from remapp.forms import UpdateDisplayNamesForm

    if request.method == 'POST':
        error_message = ''
        new_display_name = request.POST.get('new_display_name')
        new_user_defined_modality = request.POST.get('new_user_defined_modality')
        for pk in request.POST.get('pks').split(','):
            display_name_data = UniqueEquipmentNames.objects.get(pk=int(pk))
            if not display_name_data.hash_generated:
                display_name_gen_hash(display_name_data)
            if new_display_name:
                display_name_data.display_name = new_display_name
            if new_user_defined_modality and (not display_name_data.user_defined_modality == new_user_defined_modality):
                # See if change is valid otherwise return validation error
                # Assuming modality is always the same, so we take the first
                try:
                    modality = \
                        GeneralStudyModuleAttr.objects.filter(generalequipmentmoduleattr__unique_equipment_name__pk=pk)[
                            0].modality_type
                except:
                    modality = ''
                if modality in {'DX', 'CR', 'RF', 'dual', 'OT'}:
                    display_name_data.user_defined_modality = new_user_defined_modality
                    # We can't reimport as new modality type, instead we just change the modality type value
                    if new_user_defined_modality == 'dual':
                        status_message = reset_dual(pk=pk)
                        messages.info(request, status_message)
                        display_name_data.save()
                        continue
                    GeneralStudyModuleAttr.objects.filter(
                        generalequipmentmoduleattr__unique_equipment_name__pk=pk).update(
                        modality_type=new_user_defined_modality)
                elif not modality:
                    error_message = error_message + 'Can\'t determine modality type for' \
                                                    ' ' + display_name_data.display_name + ', ' \
                                                                                           'user defined modality type not set.\n'
                else:
                    error_message = error_message + 'Modality type change is not allowed for' \
                                                    ' ' + display_name_data.display_name + ' (only changing from DX ' \
                                                                                           'to RF and vice versa is allowed).\n'
            display_name_data.save()

        if error_message:
            messages.error(request, error_message)
        return HttpResponseRedirect(reverse_lazy('display_names_view'))

    else:
        if request.GET.__len__() == 0:
            return HttpResponseRedirect(reverse_lazy('display_names_view'))

        max_pk = UniqueEquipmentNames.objects.all().order_by('-pk').values_list('pk')[0][0]
        for current_pk in request.GET:
            if int(current_pk) > max_pk:
                return HttpResponseRedirect(reverse_lazy('display_names_view'))

        f = UniqueEquipmentNames.objects.filter(pk__in=map(int, request.GET.values()))

        form = UpdateDisplayNamesForm(
            initial={'display_names': [x.encode('utf-8') for x in f.values_list('display_name', flat=True)]},
            auto_id=False)

        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

        for group in request.user.groups.all():
            admin[group.name] = True

        return_structure = {'name_list': f, 'admin': admin, 'form': form}

    return render_to_response('remapp/displaynameupdate.html',
                              return_structure,
                              context_instance=RequestContext(request))


def display_name_populate(request):
    """AJAX view to populate the modality tables for the display names view

    :param request: Request object containing modality
    :return: HTML table
    """
    from django.db.models import Q
    from remapp.models import UniqueEquipmentNames

    if request.is_ajax():
        data = request.POST
        modality = data.get('modality')
        f = UniqueEquipmentNames.objects.order_by('display_name')
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in request.user.groups.all():
            admin[group.name] = True
        if modality in ['MG', 'CT']:
            name_set = f.filter(
                generalequipmentmoduleattr__general_study_module_attributes__modality_type=modality).distinct()
            dual = False
        elif modality == 'DX':
            name_set = f.filter(Q(user_defined_modality="DX") | Q(user_defined_modality="dual") | (
                    Q(user_defined_modality__isnull=True) & (
                    Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") |
                    Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR")))).distinct()
            dual = True
        elif modality == 'RF':
            name_set = f.filter(Q(user_defined_modality="RF") | Q(user_defined_modality="dual") | (
                    Q(user_defined_modality__isnull=True) &
                    Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF"))).distinct()
            dual = True
        elif modality == 'OT':
            name_set = f.filter(  # ~Q(user_defined_modality__isnull=True) | (
                ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="RF") &
                ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="MG") &
                ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CT") &
                ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="DX") &
                ~Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type="CR")).distinct()
            dual = False
        else:
            name_set = None
            dual = False
        template = 'remapp/displayname-modality.html'
        return render(request, template, {
            'name_set': name_set,
            'admin': admin,
            'modality': modality,
            'dual': dual,
        })


def display_name_modality_filter(equip_name_pk=None, modality=None):
    """Function to filter the studies to a particular unique_name entry and particular modality.

    :param equip_name_pk: Primary key of entry in unique names table
    :param modality: Modality to filter on
    :return: Reduced queryset of studies, plus count of pre-modality filtered studies for modality OT
    """
    from django.db.models import Q

    if not equip_name_pk:
        logger.error("Display name modality filter function called without a primary key ID for the unique names table")
        return
    if not modality or modality not in ['CT', 'RF', 'MG', 'DX', 'OT']:
        logger.error("Display name modality filter function called without an appropriate modality specified")
        return

    studies_all = GeneralStudyModuleAttr.objects.filter(
        generalequipmentmoduleattr__unique_equipment_name__pk=equip_name_pk)
    count_all = studies_all.count()
    if modality in ['CT', 'MG', 'RF']:
        studies = studies_all.filter(modality_type__exact=modality)
    elif modality == 'DX':
        studies = studies_all.filter(
            Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type__exact="DX") |
            Q(generalequipmentmoduleattr__general_study_module_attributes__modality_type__exact="CR")
        )
    else:  # modality == 'OT'
        studies = studies_all.exclude(
            modality_type__exact='CT'
        ).exclude(
            modality_type__exact='MG'
        ).exclude(
            modality_type__exact='DX'
        ).exclude(
            modality_type__exact='CR'
        ).exclude(
            modality_type__exact='RF'
        )
    return studies, count_all


def display_name_last_date_and_count(request):
    """AJAX view to return the most recent study date associated with an entry in the equipment database along with
    the number of studies

    :param request: Request object containing modality and equipment table ID
    :return: HTML table data element
    """

    if request.is_ajax():
        data = request.POST
        modality = data.get('modality')
        equip_name_pk = data.get('equip_name_pk')
        latest = None
        studies, count_all = display_name_modality_filter(equip_name_pk=equip_name_pk, modality=modality)
        count = studies.count()
        if count:
            latest = studies.latest('study_date').study_date
        template_latest = 'remapp/displayname-last-date.html'
        template_count = 'remapp/displayname-count.html'
        count_html = render_to_string(template_count, {'count': count, 'count_all': count_all, }, request=request)
        latest_html = render_to_string(template_latest, {'latest': latest, }, request=request)
        return_html = {'count_html': count_html, 'latest_html': latest_html}
        html_dict = json.dumps(return_html)
        return HttpResponse(html_dict, content_type='application/json')


@login_required
def review_summary_list(request, equip_name_pk=None, modality=None, delete_equip=None):
    """View to list partial and broken studies

    :param request:
    :param equip_name_pk: UniqueEquipmentNames primary key
    :param modality: modality to filter by
    :return:
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from remapp.models import UniqueEquipmentNames

    if not equip_name_pk:
        logger.error("Attempt to load review_summary_list without equip_name_pk")
        messages.error(request,
                       "Partial and broken imports can only be reviewed with the correct "
                       "link from the display name page")
        return HttpResponseRedirect(reverse_lazy('display_names_view'))

    if not request.user.groups.filter(name="admingroup"):
        messages.error(request, "You are not in the administrator group - please contact your administrator")
        return redirect(reverse_lazy('display_names_view'))

    if request.method == 'GET':
        equipment = UniqueEquipmentNames.objects.get(pk=equip_name_pk)
        studies_list, count_all = display_name_modality_filter(equip_name_pk=equip_name_pk, modality=modality)
        paginator = Paginator(studies_list, 25)
        page = request.GET.get('page')
        try:
            studies = paginator.page(page)
        except PageNotAnInteger:
            studies = paginator.page(1)
        except EmptyPage:
            studies = paginator.page(paginator.num_pages)

        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

        for group in request.user.groups.all():
            admin[group.name] = True

        template = 'remapp/review_summary_list.html'
        return render(request, template, {
            'modality': modality, 'equipment': equipment, 'equip_name_pk': equip_name_pk, 'studies': studies,
            'studies_count': studies_list.count(), 'count_all': count_all, 'admin': admin})

    if request.method == 'POST' and request.user.groups.filter(name="admingroup") and equip_name_pk and modality:
        delete_equip = bool(request.POST['delete_equip'] == u"True")
        if not delete_equip:
            studies, count_all = display_name_modality_filter(equip_name_pk=equip_name_pk, modality=modality)
            studies.delete()
            messages.info(request, "Studies deleted")
            return redirect(reverse_lazy('review_summary_list', kwargs={'equip_name_pk': equip_name_pk,
                                                                        'modality': modality}))
        else:
            studies, count_all = display_name_modality_filter(equip_name_pk=equip_name_pk, modality=modality)
            if count_all > studies.count():
                messages.warning(request,
                                 "Can't delete table entry - non-{0} studies are associated with it".format(modality))
                logger.warning("Can't delete table entry - non-{0} studies are associated with it".format(modality))
                return redirect(reverse_lazy('review_summary_list', kwargs={'equip_name_pk': equip_name_pk,
                                                                            'modality': modality}))
            else:
                studies.delete()
                UniqueEquipmentNames.objects.get(pk=equip_name_pk).delete()
                messages.info(request, "Studies and equipment name table entry deleted")
                return redirect(reverse_lazy('display_names_view'))
    else:
        messages.error(request, "Incorrect attempt to delete studies.")
        return redirect(reverse_lazy('review_summary_list', kwargs={'equip_name_pk': equip_name_pk,
                                                                    'modality': modality}))


@login_required
def review_studies_delete(request):
    """AJAX function to replace Delete button with delete form for associated studies

    :param request:
    :return:
    """
    if request.is_ajax() and request.user.groups.filter(name="admingroup"):
        data = request.POST
        template = 'remapp/review_studies_delete_button.html'
        return render(request, template, {'delete_equip': False, 'modality': data['modality'],
                                          'equip_name_pk': data['equip_name_pk']})


@login_required
def review_studies_equip_delete(request):
    """AJAX function to replace Delete button with delete form for equipment table entry and studies

    :param request:
    :return:
    """
    if request.is_ajax() and request.user.groups.filter(name="admingroup"):
        data = request.POST
        template = 'remapp/review_studies_delete_button.html'
        return render(request, template, {'delete_equip': True, 'modality': data['modality'],
                                          'equip_name_pk': data['equip_name_pk']})


@login_required
def review_failed_studies_delete(request):
    """AJAX function to replace Delete button with delete form for studies without ubique_equipment_name table

    :param request:
    :return:
    """
    if request.is_ajax() and request.user.groups.filter(name="admingroup"):
        data = request.POST
        template = 'remapp/review_studies_delete_button.html'
        return render(request, template, {'delete_equip': False, 'modality': data['modality'],
                                          'equip_name_pk': 'n/a'})


def reset_dual(pk=None):
    """function to set modality to DX or RF depending on presence of fluoro information.

    :param pk: Unique equipment names table prmary key
    :return: status message
    """

    if not pk:
        logger.error("Reset dual called with no primary key")
        return

    studies = GeneralStudyModuleAttr.objects.filter(generalequipmentmoduleattr__unique_equipment_name__pk=pk)
    not_dx_rf_cr = studies.exclude(modality_type__exact='DX').exclude(
        modality_type__exact='RF').exclude(modality_type__exact='CR')
    message_start = "Reprocessing dual for {0}. Number of studies is {1}, of which {2} are " \
                    "DX, {3} are CR, {4} are RF and {5} are something else before processing,".format(
        studies[0].generalequipmentmoduleattr_set.get().unique_equipment_name.display_name,
        studies.count(),
        studies.filter(modality_type__exact='DX').count(),
        studies.filter(modality_type__exact='CR').count(),
        studies.filter(modality_type__exact='RF').count(),
        not_dx_rf_cr.count(),
    )

    logger.debug(message_start)

    for study in studies:
        try:
            projection_xray_dose = study.projectionxrayradiationdose_set.get()
            if projection_xray_dose.acquisition_device_type_cid:
                device_type = projection_xray_dose.acquisition_device_type_cid.code_meaning
                if 'Fluoroscopy-Guided' in device_type:
                    study.modality_type = 'RF'
                    study.save()
                    continue
                elif any(x in device_type for x in ['Integrated', 'Cassette-based']):
                    study.modality_type = 'DX'
                    study.save()
                    continue
            try:
                accum_xray_dose = projection_xray_dose.accumxraydose_set.order_by('pk')[0]  # consider just first plane
                try:
                    accum_fluoro_proj = accum_xray_dose.accumprojxraydose_set.get()
                    if accum_fluoro_proj.fluoro_dose_area_product_total or accum_fluoro_proj.total_fluoro_time:
                        study.modality_type = 'RF'
                        study.save()
                        continue
                    else:
                        study.modality_type = 'DX'
                        study.save()
                        continue
                except ObjectDoesNotExist:
                    try:
                        if accum_xray_dose.accumintegratedprojradiogdose_set.get():
                            study.modality_type = 'DX'
                            study.save()
                            continue
                    except ObjectDoesNotExist:
                        study.modality_type = 'OT'
                        study.save()
                        logger.debug(
                            "Unable to reprocess study - no device type or accumulated data to go on. "
                            "Modality set to OT.")
                study.modality_type = 'OT'
                study.save()
                logger.debug(
                    "Unable to reprocess study - no device type or accumulated data to go on. Modality set to OT.")
            except ObjectDoesNotExist:
                study.modality_type = 'OT'
                study.save()
                logger.debug(
                    "Unable to reprocess study - no device type or accumulated data to go on. Modality set to OT.")
        except ObjectDoesNotExist:
            study.modality_type = 'OT'
            study.save()
            logger.debug("Unable to reprocess study - no device type or accumulated data to go on. Modality set to OT.")

    not_dx_rf_cr = studies.exclude(modality_type__exact='DX').exclude(
        modality_type__exact='RF').exclude(modality_type__exact='CR')
    message_finish = "and after processing  {0} are DX, {1} are CR, {2} are RF and {3} are something else".format(
                                                        studies.filter(modality_type='DX').count(),
                                                        studies.filter(modality_type='CR').count(),
                                                        studies.filter(modality_type='RF').count(),
                                                        not_dx_rf_cr.count(),
    )
    logger.debug(message_finish)
    return " ".join([message_start, message_finish])


@login_required
def reprocess_dual(request, pk=None):
    """View to reprocess the studies from a modality that produces planar radiography and fluoroscopy to recategorise
    them to DX or RF.

    :param request: Request object
    :return: Redirect back to display names view
    """

    if not request.user.groups.filter(name="admingroup"):
        messages.error(request, "You are not in the administrator group - please contact your administrator")
        return redirect(reverse_lazy('display_names_view'))

    if request.method == 'GET' and pk:
        status_message = reset_dual(pk=pk)
        messages.info(request, status_message)

    return HttpResponseRedirect(reverse_lazy('display_names_view'))


def _get_review_study_data(study):
    """Get study data common to normal review and failed study review

    :param study: GeneralStudyModuleAttr object
    :return: Dict of study data
        """
    study_data = {
        'study_date': study.study_date,
        'study_time': study.study_time,
        'accession_number': study.accession_number,
        'study_description': study.study_description,
    }
    try:
        patient = study.patientmoduleattr_set.get()
        study_data['patientmoduleattr'] = u"Yes"
        if patient.not_patient_indicator:
            study_data['patientmoduleattr'] += u"<br>?not patient"
    except ObjectDoesNotExist:
        study_data['patientmoduleattr'] = u"Missing"
    try:
        patientstudymoduleattr = study.patientstudymoduleattr_set.get()
        age = patientstudymoduleattr.patient_age_decimal
        if age:
            study_data['patientstudymoduleattr'] = u"Yes. Age {0:.1f}".format(
                patientstudymoduleattr.patient_age_decimal)
        else:
            study_data['patientstudymoduleattr'] = u"Yes."
    except ObjectDoesNotExist:
        study_data['patientstudymoduleattr'] = u"Missing"
    try:
        ctradiationdose = study.ctradiationdose_set.get()
        study_data['ctradiationdose'] = u"Yes"
        try:
            ctaccumulateddosedata = ctradiationdose.ctaccumulateddosedata_set.get()
            num_events = ctaccumulateddosedata.total_number_of_irradiation_events
            study_data['ctaccumulateddosedata'] = "Yes, {0} events".format(num_events)
        except ObjectDoesNotExist:
            study_data['ctaccumulateddosedata'] = u""
        try:
            ctirradiationeventdata_set = ctradiationdose.ctirradiationeventdata_set.order_by('pk')

            study_data['cteventdata'] = u"{0} events.<br>".format(
                ctirradiationeventdata_set.count())
            for index, event in enumerate(ctirradiationeventdata_set):
                if event.acquisition_protocol:
                    protocol = event.acquisition_protocol
                else:
                    protocol = u""
                if event.dlp:
                    study_data['cteventdata'] += u"e{0}: {1} {2:.2f}&nbsp;mGycm<br>".format(
                        index,
                        protocol,
                        event.dlp
                    )
                else:
                    study_data['cteventdata'] += u"e{0}: {1}<br>".format(
                        index,
                        protocol
                    )
        except ObjectDoesNotExist:
            study_data['cteventdata'] = u""
    except ObjectDoesNotExist:
        study_data['ctradiationdose'] = u""
        study_data['ctaccumulateddosedata'] = u""
        study_data['cteventdata'] = u""
    try:
        projectionxraydata = study.projectionxrayradiationdose_set.get()
        study_data['projectionxraydata'] = u"Yes"
        try:
            accumxraydose_set = projectionxraydata.accumxraydose_set.order_by('pk')
            accumxraydose_set_count = accumxraydose_set.count()
            if accumxraydose_set_count == 1:
                study_data['accumxraydose'] = u"Yes"
            elif accumxraydose_set_count:
                study_data['accumxraydose'] = u"{0} present".format(accumxraydose_set_count)
            else:
                study_data['accumxraydose'] = u""
            try:
                accumfluoroproj = {}
                study_data['accumfluoroproj'] = u""
                for index, accumxraydose in enumerate(accumxraydose_set):
                    accumfluoroproj[index] = accumxraydose.accumprojxraydose_set.get()
                    study_data['accumfluoroproj'] += u"P{0} ".format(index + 1)
                    if accumfluoroproj[index].fluoro_dose_area_product_total:
                        study_data['accumfluoroproj'] += u"Total fluoro DA: {0:.2f}&nbsp;cGy.cm<sup>2</sup>" \
                                                         u"; ".format(accumfluoroproj[index].fluoro_gym2_to_cgycm2())
                    if accumfluoroproj[index].acquisition_dose_area_product_total:
                        study_data['accumfluoroproj'] += u"Acq: {0:.2f}&nbsp;cGy.cm<sup>2</sup>. ".format(
                            accumfluoroproj[index].acq_gym2_to_cgycm2())
            except ObjectDoesNotExist:
                study_data['accumfluoroproj'] = u""
            try:
                accummammo_set = accumxraydose_set[0].accummammographyxraydose_set.order_by('pk')
                if accummammo_set.count() == 0:
                    study_data['accummammo'] = u""
                else:
                    study_data['accummammo'] = u""
                    for accummammo in accummammo_set:
                        study_data['accummammo'] += u"{0}: {1:.3f}&nbsp;mGy".format(
                            accummammo.laterality, accummammo.accumulated_average_glandular_dose)
            except ObjectDoesNotExist:
                study_data['accummammo'] = u""
            try:
                accumcassproj = {}
                study_data['accumcassproj'] = u""
                for index, accumxraydose in enumerate(accumxraydose_set):
                    accumcassproj[index] = accumxraydose.accumcassettebsdprojradiogdose_set.get()
                    study_data['accumcassproj'] += u"Number of frames {0}".format(
                        accumcassproj[index].total_number_of_radiographic_frames)
            except ObjectDoesNotExist:
                study_data['accumcassproj'] = u""
            try:
                accumproj = {}
                study_data['accumproj'] = u""
                for index, accumxraydose in enumerate(accumxraydose_set):
                    accumproj[index] = accumxraydose.accumintegratedprojradiogdose_set.get()
                    study_data['accumproj'] += u"DAP total {0:.2f}&nbsp;cGy.cm<sup>2</sup> ".format(
                        accumproj[index].convert_gym2_to_cgycm2())
            except ObjectDoesNotExist:
                study_data['accumproj'] = u""
        except ObjectDoesNotExist:
            study_data['accumxraydose'] = u""
            study_data['accumfluoroproj'] = u""
            study_data['accummammo'] = u""
            study_data['accumcassproj'] = u""
            study_data['accumproj'] = u""
        try:
            study_data['eventdetector'] = u""
            study_data['eventsource'] = u""
            study_data['eventmech'] = u""
            irradevent_set = projectionxraydata.irradeventxraydata_set.order_by('pk')
            irradevent_set_count = irradevent_set.count()
            if irradevent_set_count == 1:
                study_data['irradevent'] = u"{0} event. ".format(irradevent_set_count)
            else:
                study_data['irradevent'] = u"{0} events. <br>".format(irradevent_set_count)
            for index, irradevent in enumerate(irradevent_set):
                if index == 4:
                    study_data['irradevent'] += u"...etc"
                    study_data['eventdetector'] += u"...etc"
                    study_data['eventsource'] += u"...etc"
                    study_data['eventmech'] += u"...etc"
                    break
                if irradevent.dose_area_product:
                    study_data['irradevent'] += u"e{0}: {1} {2:.2f}&nbsp;cGy.cm<sup>2</sup> <br>".format(
                        index + 1,
                        irradevent.acquisition_protocol,
                        irradevent.convert_gym2_to_cgycm2())
                elif irradevent.entrance_exposure_at_rp:
                    study_data['irradevent'] += u"RP dose {0}: {1:.2f} mGy  <br>".format(
                        index + 1, irradevent.entrance_exposure_at_rp)
                try:
                    eventdetector = irradevent.irradeventxraydetectordata_set.get()
                    if eventdetector.exposure_index:
                        study_data['eventdetector'] += u"e{0}: EI&nbsp;{1:.1f},<br>".format(
                            index + 1, eventdetector.exposure_index)
                    else:
                        study_data['eventdetector'] += u"e{0} present,<br>".format(index + 1)
                except ObjectDoesNotExist:
                    study_data['eventdetector'] += u""
                try:
                    eventsource = irradevent.irradeventxraysourcedata_set.get()
                    if eventsource.dose_rp:
                        study_data['eventsource'] += u"e{0} RP Dose {1:.3f}&nbsp;mGy,<br>".format(
                            index + 1, eventsource.convert_gy_to_mgy())
                    elif eventsource.average_glandular_dose:
                        study_data['eventsource'] += u"e{0} AGD {1:.2f}&nbsp;mGy,<br>".format(
                            index + 1, eventsource.average_glandular_dose)
                    else:
                        study_data['eventsource'] += u"e{0} present,<br>".format(index + 1)
                except ObjectDoesNotExist:
                    study_data['eventsource'] += u""
                try:
                    eventmech = irradevent.irradeventxraymechanicaldata_set.get()
                    if eventmech.positioner_primary_angle:
                        study_data['eventmech'] += u"e{0} {1:.1f}&deg;<br>".format(
                            index + 1, eventmech.positioner_primary_angle)
                    else:
                        study_data['eventmech'] += u"e{0} present,<br>".format(
                            index + 1)
                except ObjectDoesNotExist:
                    study_data['eventmech'] = u""
        except ObjectDoesNotExist:
            study_data['irradevent'] = u""
    except ObjectDoesNotExist:
        study_data['projectionxraydata'] = u""
        study_data['accumxraydose'] = u""
        study_data['accumfluoroproj'] = u""
        study_data['accummammo'] = u""
        study_data['accumcassproj'] = u""
        study_data['accumproj'] = u""
        study_data['irradevent'] = u""
        study_data['eventdetector'] = u""
        study_data['eventdetector'] = u""
        study_data['eventsource'] = u""
        study_data['eventmech'] = u""
        study_data['eventmech'] = u""
    return study_data


def review_study_details(request):
    """AJAX function to populate row in table with details of study for review

    :param request: Request object containing study pk
    :return: HTML row data
    """

    if request.is_ajax():
        data = request.POST
        study_pk = data.get('study_pk')
        study = GeneralStudyModuleAttr.objects.get(pk__exact=study_pk)
        study_data = _get_review_study_data(study)
        template = 'remapp/review_study.html'
        return render(request, template, study_data)


def review_failed_study_details(request):
    """AJAX function to populate row in table with details of study for review

    :param request: Request object containing study pk
    :return: HTML row data
    """

    if request.is_ajax():
        data = request.POST
        study_pk = data.get('study_pk')
        study = GeneralStudyModuleAttr.objects.get(pk__exact=study_pk)
        study_data = _get_review_study_data(study)

        try:
            equipment = study.generalequipmentmoduleattr_set.get()
            study_data['station_name'] = equipment.station_name
            study_data['manufacturer'] = equipment.manufacturer
            study_data['manufacturer_model_name'] = equipment.manufacturer_model_name
            study_data['institution_name'] = equipment.institution_name
            study_data['institution_department_name'] = equipment.institutional_department_name
            study_data['device_serial_number'] = equipment.device_serial_number
            study_data['equipmentattr'] = True
        except ObjectDoesNotExist:
            study_data['equipmentattr'] = False
            study_data['station_name'] = u""
            study_data['manufacturer'] = u""
            study_data['manufacturer_model_name'] = u""
            study_data['institution_name'] = u""
            study_data['institution_department_name'] = u""
            study_data['device_serial_number'] = u""

        template = 'remapp/review_failed_study.html'
        return render(request, template, study_data)


def _get_broken_studies(modality=None):
    """Filter studies with no unique_equipment_name table entry
    :param modality: modality to filter by
    :return: Query filter of studies
    """
    from django.db.models import Q

    if modality == 'DX':
        all_mod = GeneralStudyModuleAttr.objects.filter(Q(modality_type__exact=u'DX') | Q(modality_type__exact=u'CR'))
    else:
        all_mod = GeneralStudyModuleAttr.objects.filter(modality_type__exact=modality)

    return all_mod.filter(generalequipmentmoduleattr__unique_equipment_name__display_name__isnull=True)


def failed_list_populate(request):
    """View for failed import section of display name view

    :return: render request with modality specific numbers of studies
    """

    if request.is_ajax():
        failed = {}
        for modality in ['CT', 'RF', 'MG', 'DX']:
            failed[modality] = _get_broken_studies(modality).count()
        template = 'remapp/failed_summary_list.html'
        return render(request, template, {'failed': failed})


@login_required
def review_failed_imports(request, modality=None):
    """View to list 'failed import' studies

    :param request:
    :param modality: modality to filter by
    :return:
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    if not modality in [u'CT', u'RF', u'MG', u'DX']:
        logger.error("Attempt to load review_failed_imports without suitable modality")
        messages.error(request,
                       "Failed study imports can only be reviewed with the correct "
                       "link from the display name page")
        return HttpResponseRedirect(reverse_lazy('display_names_view'))

    if not request.user.groups.filter(name="admingroup"):
        messages.error(request, "You are not in the administrator group - please contact your administrator")
        return redirect(reverse_lazy('display_names_view'))

    if request.method == 'GET':
        broken_studies = _get_broken_studies(modality)

        paginator = Paginator(broken_studies, 25)
        page = request.GET.get('page')
        try:
            studies = paginator.page(page)
        except PageNotAnInteger:
            studies = paginator.page(1)
        except EmptyPage:
            studies = paginator.page(paginator.num_pages)

        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

        for group in request.user.groups.all():
            admin[group.name] = True

        template = 'remapp/review_failed_imports.html'
        return render(request, template, {
            'modality': modality, 'studies': studies,
            'studies_count': broken_studies.count(), 'admin': admin})

    if request.method == 'POST' and request.user.groups.filter(name="admingroup") and modality:
        broken_studies = _get_broken_studies(modality)
        broken_studies.delete()
        messages.info(request, "Studies deleted")
        return redirect(reverse_lazy('review_failed_imports', kwargs={'modality': modality}))
    else:
        messages.error(request, "Incorrect attempt to delete studies.")
        return redirect(reverse_lazy('review_failed_imports', kwargs={'modality': modality}))


@login_required
def chart_options_view(request):
    from remapp.forms import GeneralChartOptionsDisplayForm, DXChartOptionsDisplayForm, CTChartOptionsDisplayForm,\
        RFChartOptionsDisplayForm, MGChartOptionsDisplayForm
    from openremproject import settings

    if request.method == 'POST':
        general_form = GeneralChartOptionsDisplayForm(request.POST)
        ct_form = CTChartOptionsDisplayForm(request.POST)
        dx_form = DXChartOptionsDisplayForm(request.POST)
        rf_form = RFChartOptionsDisplayForm(request.POST)
        mg_form = MGChartOptionsDisplayForm(request.POST)
        if general_form.is_valid()\
                and ct_form.is_valid() and dx_form.is_valid()\
                and rf_form.is_valid() and mg_form.is_valid():
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
            user_profile.plotHistograms = general_form.cleaned_data['plotHistograms']
            user_profile.plotCaseInsensitiveCategories = general_form.cleaned_data['plotCaseInsensitiveCategories']

            user_profile.plotCTAcquisitionMeanDLP = ct_form.cleaned_data['plotCTAcquisitionMeanDLP']
            user_profile.plotCTAcquisitionMeanCTDI = ct_form.cleaned_data['plotCTAcquisitionMeanCTDI']
            user_profile.plotCTAcquisitionFreq = ct_form.cleaned_data['plotCTAcquisitionFreq']
            user_profile.plotCTStudyMeanDLP = ct_form.cleaned_data['plotCTStudyMeanDLP']
            user_profile.plotCTStudyMeanCTDI = ct_form.cleaned_data['plotCTStudyMeanCTDI']
            user_profile.plotCTStudyFreq = ct_form.cleaned_data['plotCTStudyFreq']
            user_profile.plotCTStudyNumEvents = ct_form.cleaned_data['plotCTStudyNumEvents']
            user_profile.plotCTRequestMeanDLP = ct_form.cleaned_data['plotCTRequestMeanDLP']
            user_profile.plotCTRequestFreq = ct_form.cleaned_data['plotCTRequestFreq']
            user_profile.plotCTRequestNumEvents = ct_form.cleaned_data['plotCTRequestNumEvents']
            user_profile.plotCTStudyPerDayAndHour = ct_form.cleaned_data['plotCTStudyPerDayAndHour']
            user_profile.plotCTStudyMeanDLPOverTime = ct_form.cleaned_data['plotCTStudyMeanDLPOverTime']
            user_profile.plotCTStudyMeanDLPOverTimePeriod = ct_form.cleaned_data['plotCTStudyMeanDLPOverTimePeriod']
            user_profile.plotCTInitialSortingChoice = ct_form.cleaned_data['plotCTInitialSortingChoice']

            user_profile.plotDXAcquisitionMeanDAP = dx_form.cleaned_data['plotDXAcquisitionMeanDAP']
            user_profile.plotDXAcquisitionFreq = dx_form.cleaned_data['plotDXAcquisitionFreq']
            user_profile.plotDXStudyMeanDAP = dx_form.cleaned_data['plotDXStudyMeanDAP']
            user_profile.plotDXStudyFreq = dx_form.cleaned_data['plotDXStudyFreq']
            user_profile.plotDXRequestMeanDAP = dx_form.cleaned_data['plotDXRequestMeanDAP']
            user_profile.plotDXRequestFreq = dx_form.cleaned_data['plotDXRequestFreq']
            user_profile.plotDXAcquisitionMeankVp = dx_form.cleaned_data['plotDXAcquisitionMeankVp']
            user_profile.plotDXAcquisitionMeanmAs = dx_form.cleaned_data['plotDXAcquisitionMeanmAs']
            user_profile.plotDXStudyPerDayAndHour = dx_form.cleaned_data['plotDXStudyPerDayAndHour']
            user_profile.plotDXAcquisitionMeankVpOverTime = dx_form.cleaned_data['plotDXAcquisitionMeankVpOverTime']
            user_profile.plotDXAcquisitionMeanmAsOverTime = dx_form.cleaned_data['plotDXAcquisitionMeanmAsOverTime']
            user_profile.plotDXAcquisitionMeanDAPOverTime = dx_form.cleaned_data['plotDXAcquisitionMeanDAPOverTime']
            user_profile.plotDXAcquisitionMeanDAPOverTimePeriod = dx_form.cleaned_data[
                'plotDXAcquisitionMeanDAPOverTimePeriod']
            user_profile.plotDXInitialSortingChoice = dx_form.cleaned_data['plotDXInitialSortingChoice']

            user_profile.plotRFStudyPerDayAndHour = rf_form.cleaned_data['plotRFStudyPerDayAndHour']
            user_profile.plotRFStudyFreq = rf_form.cleaned_data['plotRFStudyFreq']
            user_profile.plotRFStudyDAP = rf_form.cleaned_data['plotRFStudyDAP']
            user_profile.plotRFInitialSortingChoice = rf_form.cleaned_data['plotRFInitialSortingChoice']

            user_profile.plotMGStudyPerDayAndHour = mg_form.cleaned_data['plotMGStudyPerDayAndHour']
            user_profile.plotMGAGDvsThickness = mg_form.cleaned_data['plotMGAGDvsThickness']
            user_profile.plotMGkVpvsThickness = mg_form.cleaned_data['plotMGkVpvsThickness']
            user_profile.plotMGmAsvsThickness = mg_form.cleaned_data['plotMGmAsvsThickness']

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
                         'plotHistogramBins': user_profile.plotHistogramBins,
                         'plotHistograms': user_profile.plotHistograms,
                         'plotCaseInsensitiveCategories': user_profile.plotCaseInsensitiveCategories}

    ct_form_data = {'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                    'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                    'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                    'plotCTStudyMeanDLP': user_profile.plotCTStudyMeanDLP,
                    'plotCTStudyMeanCTDI': user_profile.plotCTStudyMeanCTDI,
                    'plotCTStudyFreq': user_profile.plotCTStudyFreq,
                    'plotCTStudyNumEvents': user_profile.plotCTStudyNumEvents,
                    'plotCTRequestMeanDLP': user_profile.plotCTRequestMeanDLP,
                    'plotCTRequestFreq': user_profile.plotCTRequestFreq,
                    'plotCTRequestNumEvents': user_profile.plotCTRequestNumEvents,
                    'plotCTStudyPerDayAndHour': user_profile.plotCTStudyPerDayAndHour,
                    'plotCTStudyMeanDLPOverTime': user_profile.plotCTStudyMeanDLPOverTime,
                    'plotCTStudyMeanDLPOverTimePeriod': user_profile.plotCTStudyMeanDLPOverTimePeriod,
                    'plotCTInitialSortingChoice': user_profile.plotCTInitialSortingChoice}

    dx_form_data = {'plotDXAcquisitionMeanDAP': user_profile.plotDXAcquisitionMeanDAP,
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
                    'plotDXInitialSortingChoice': user_profile.plotDXInitialSortingChoice}

    rf_form_data = {'plotRFStudyPerDayAndHour': user_profile.plotRFStudyPerDayAndHour,
                    'plotRFStudyFreq': user_profile.plotRFStudyFreq,
                    'plotRFStudyDAP': user_profile.plotRFStudyDAP,
                    'plotRFInitialSortingChoice': user_profile.plotRFInitialSortingChoice}

    mg_form_data = {'plotMGStudyPerDayAndHour': user_profile.plotMGStudyPerDayAndHour,
                    'plotMGAGDvsThickness': user_profile.plotMGAGDvsThickness,
                    'plotMGkVpvsThickness': user_profile.plotMGkVpvsThickness,
                    'plotMGmAsvsThickness': user_profile.plotMGmAsvsThickness}

    general_chart_options_form = GeneralChartOptionsDisplayForm(general_form_data)
    ct_chart_options_form = CTChartOptionsDisplayForm(ct_form_data)
    dx_chart_options_form = DXChartOptionsDisplayForm(dx_form_data)
    rf_chart_options_form = RFChartOptionsDisplayForm(rf_form_data)
    mg_chart_options_form = MGChartOptionsDisplayForm(mg_form_data)

    return_structure = {'admin': admin,
                        'GeneralChartOptionsForm': general_chart_options_form,
                        'CTChartOptionsForm': ct_chart_options_form,
                        'DXChartOptionsForm': dx_chart_options_form,
                        'RFChartOptionsForm': rf_chart_options_form,
                        'MGChartOptionsForm': mg_chart_options_form,
                        }

    return render_to_response(
        'remapp/displaychartoptions.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def homepage_options_view(request):
    """View to enable user to see and update home page options

    :param request: request object
    :return: dictionary of home page settings, html template location and request object
    """
    from remapp.forms import HomepageOptionsForm
    from remapp.models import HomePageAdminSettings
    from django.utils.safestring import mark_safe

    try:
        HomePageAdminSettings.objects.get()
    except ObjectDoesNotExist:
        HomePageAdminSettings.objects.create()

    display_workload_stats = HomePageAdminSettings.objects.values_list('enable_workload_stats', flat=True)[0]
    if not display_workload_stats:
        if not request.user.groups.filter(name="admingroup"):
            messages.info(request, mark_safe(u'The display of homepage workload stats is disabled; only a member of the admin group can change this setting')) # nosec

    if request.method == 'POST':
        homepage_options_form = HomepageOptionsForm(request.POST)
        if homepage_options_form.is_valid():
            try:
                # See if the user has a userprofile
                user_profile = request.user.userprofile
            except:
                # Create a default userprofile for the user if one doesn't exist
                create_user_profile(sender=request.user, instance=request.user, created=True)
                user_profile = request.user.userprofile

            user_profile.summaryWorkloadDaysA = homepage_options_form.cleaned_data['dayDeltaA']
            user_profile.summaryWorkloadDaysB = homepage_options_form.cleaned_data['dayDeltaB']

            user_profile.save()

            if request.user.groups.filter(name="admingroup"):
                if homepage_options_form.cleaned_data['enable_workload_stats'] != display_workload_stats:
                    homepage_admin_settings = HomePageAdminSettings.objects.all()[0]
                    homepage_admin_settings.enable_workload_stats = homepage_options_form.cleaned_data['enable_workload_stats']
                    homepage_admin_settings.save()
                    if homepage_options_form.cleaned_data['enable_workload_stats']:
                        messages.info(request, "Display of workload stats enabled")
                    else:
                        messages.info(request, "Display of workload stats disabled")

        messages.success(request, "Home page options have been updated")
        return HttpResponseRedirect(reverse_lazy('homepage_options_view'))

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    try:
        # See if the user has a userprofile
        user_profile = request.user.userprofile
    except:
        # Create a default userprofile for the user if one doesn't exist
        create_user_profile(sender=request.user, instance=request.user, created=True)
        user_profile = request.user.userprofile

    homepage_form_data = {'dayDeltaA': user_profile.summaryWorkloadDaysA,
                          'dayDeltaB': user_profile.summaryWorkloadDaysB,
                          'enable_workload_stats': display_workload_stats}

    homepage_options_form = HomepageOptionsForm(homepage_form_data)

    home_config = {'display_workload_stats': display_workload_stats}

    return_structure = {'admin': admin,
                        'HomepageOptionsForm': homepage_options_form,
                        'home_config': home_config
                        }

    return render_to_response(
        'remapp/displayhomepageoptions.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def not_patient_indicators(request):
    """Displays current not-patient indicators
    """
    from remapp.models import NotPatientIndicatorsID, NotPatientIndicatorsName

    not_patient_ids = NotPatientIndicatorsID.objects.all()
    not_patient_names = NotPatientIndicatorsName.objects.all()

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    # Render list page with the documents and the form
    return render_to_response(
        'remapp/notpatient.html',
        {'ids': not_patient_ids, 'names': not_patient_names, 'admin': admin},
        context_instance=RequestContext(request)
    )


@login_required
def not_patient_indicators_as_074(request):
    """Add patterns to no-patient indicators to replicate 0.7.4 behaviour"""
    from remapp.models import NotPatientIndicatorsID, NotPatientIndicatorsName

    if request.user.groups.filter(name="admingroup"):
        not_patient_ids = NotPatientIndicatorsID.objects.all()
        not_patient_names = NotPatientIndicatorsName.objects.all()

        id_indicators = [u'*phy*', u'*test*', u'*qa*']
        name_indicators = [u'*phys*', u'*test*', u'*qa*']

        for id_indicator in id_indicators:
            if not not_patient_ids.filter(not_patient_id__iexact=id_indicator):
                NotPatientIndicatorsID(not_patient_id=id_indicator).save()

        for name_indicator in name_indicators:
            if not not_patient_names.filter(not_patient_name__iexact=name_indicator):
                NotPatientIndicatorsName(not_patient_name=name_indicator).save()

        messages.success(request, "0.7.4 style not-patient indicators restored")
        return redirect(reverse_lazy('not_patient_indicators'))

    else:
        messages.error(request, "Only members of the admingroup are allowed to modify not-patient indicators")
    return redirect(reverse_lazy('not_patient_indicators'))


@login_required
def admin_questions_hide_not_patient(request):
    """Hides the not-patient revert to 0.7.4 question"""
    from remapp.models import AdminTaskQuestions

    if request.user.groups.filter(name="admingroup"):
        admin_question = AdminTaskQuestions.objects.all()[0]
        admin_question.ask_revert_to_074_question = False
        admin_question.save()
        messages.success(request, u"Identifying not-patient exposure question won't be shown again")
        return redirect(reverse_lazy('home'))
    else:
        messages.error(request, u"Only members of the admingroup are allowed config this question")
    return redirect(reverse_lazy('not_patient_indicators'))


def _create_admin_dict(request):
    """Function to factor out creating admin dict with admin true/false

    :return: dict containing version numbers and admin group membership
    """
    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
    for group in request.user.groups.all():
        admin[group.name] = True
    return admin


@login_required
def rabbitmq_admin(request):
    """View to show RabbitMQ queues. Content generated using AJAX"""

    admin = _create_admin_dict(request)

    template = 'remapp/rabbitmq_admin.html'
    return render_to_response(template, {'admin': admin}, context_instance=RequestContext(request))


def rabbitmq_queues(request):
    """AJAX function to get current queue details"""
    import requests

    if request.is_ajax():
        try:
            queues = requests.get(
                'http://localhost:15672/api/queues', auth=('guest', 'guest')).json()
        except requests.ConnectionError:
            admin = _create_admin_dict(request)
            template = 'remapp/rabbitmq_connection_error.html'
            return render_to_response(template, {'admin': admin}, context_instance=RequestContext(request))
        template = 'remapp/rabbitmq_queues.html'
        return render_to_response(template, {'queues': queues}, context_instance=RequestContext(request))


def rabbitmq_purge(request, queue=None):
    """Function to purge one of the RabbitMQ queues"""
    import requests

    if queue:
        queue_url = 'http://localhost:15672/api/queues/%2f/{0}/contents'.format(queue)
        requests.delete(queue_url, auth=('guest', 'guest'))
        return redirect(reverse_lazy('rabbitmq_admin'))


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

    admin = _create_admin_dict(request)

    # Render list page with the documents and the form
    return render_to_response(
        'remapp/dicomsummary.html',
        {'store': store, 'remoteqr': remoteqr, 'admin': admin, 'del_settings': del_settings},
        context_instance=RequestContext(request)
    )


class DicomStoreCreate(CreateView):  # pylint: disable=unused-variable
    """CreateView to add details of a DICOM Store to the database

    """
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


class DicomStoreUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView to update details of a DICOM store in the database

    """
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


class DicomStoreDelete(DeleteView):  # pylint: disable=unused-variable
    """DeleteView to delete DICOM store information from the database

    """
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


class DicomQRCreate(CreateView):  # pylint: disable=unused-variable
    """CreateView to add details of a DICOM query-retrieve node

    """
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


class DicomQRUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView to update details of a DICOM query-retrieve node

    """
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


class DicomQRDelete(DeleteView):  # pylint: disable=unused-variable
    """DeleteView to delete details of a DICOM query-retrieve node

    """
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


class PatientIDSettingsUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView to update the patient ID settings

    """
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


class DicomDeleteSettingsUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView tp update the settings relating to deleting DICOM after import

    """
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


class RFHighDoseAlertSettings(UpdateView):  # pylint: disable=unused-variable
    """UpdateView for configuring the fluoroscopy high dose alert settings

    """
    from remapp.models import HighDoseMetricAlertSettings
    from remapp.forms import RFHighDoseFluoroAlertsForm
    from django.core.exceptions import ObjectDoesNotExist

    try:
        HighDoseMetricAlertSettings.objects.get()
    except ObjectDoesNotExist:
        HighDoseMetricAlertSettings.objects.create()

    model = HighDoseMetricAlertSettings
    form_class = RFHighDoseFluoroAlertsForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context

    def form_valid(self, form):
        if form.has_changed():
            if 'show_accum_dose_over_delta_weeks' in form.changed_data:
                msg = 'Display of summed total DAP and total dose at RP on summary page '
                if form.cleaned_data['show_accum_dose_over_delta_weeks']:
                    msg += 'enabled'
                else:
                    msg += ' disabled'
                messages.info(self.request, msg)
            if 'calc_accum_dose_over_delta_weeks_on_import' in form.changed_data:
                msg = 'Calculation of summed total DAP and total dose at RP for incoming studies '
                if form.cleaned_data['calc_accum_dose_over_delta_weeks_on_import']:
                    msg += 'enabled'
                else:
                    msg += ' disabled'
                messages.info(self.request, msg)
            if 'send_high_dose_metric_alert_emails' in form.changed_data:
                msg = 'E-mail notification of high doses '
                if form.cleaned_data['send_high_dose_metric_alert_emails']:
                    msg += 'enabled'
                else:
                    msg += ' disabled'
                messages.info(self.request, msg)
            if 'alert_total_dap_rf' in form.changed_data:
                messages.info(self.request, 'Total DAP alert level has been changed to {0}'.format(form.cleaned_data['alert_total_dap_rf']))
            if 'alert_total_rp_dose_rf' in form.changed_data:
                messages.info(self.request, 'Total dose at reference point alert level has been changed to {0}'.format(form.cleaned_data['alert_total_rp_dose_rf']))
            if 'accum_dose_delta_weeks' in form.changed_data:
                messages.warning(self.request, 'The time period used to sum total DAP and total dose at RP has changed. The summed data must be recalculated: click on the "Recalculate all summed data" button below. The recalculation can take several minutes')
            return super(RFHighDoseAlertSettings, self).form_valid(form)
        else:
            messages.info(self.request, "No changes made")
        return super(RFHighDoseAlertSettings, self).form_valid(form)


@login_required
@csrf_exempt
def rf_alert_notifications_view(request):
    """View for display and modification of fluoroscopy high dose alert recipients

    """
    from django.contrib.auth.models import User
    from remapp.models import HighDoseMetricAlertRecipients
    from remapp.tools.send_high_dose_alert_emails import send_rf_high_dose_alert_email
    from tools.get_values import get_keys_by_value

    if request.method == 'POST' and request.user.groups.filter(name="admingroup"):
        # Check to see if we need to send a test message
        if 'Send test' in request.POST.values():
            recipient = get_keys_by_value(request.POST, 'Send test')[0]
            email_response = send_rf_high_dose_alert_email(study_pk=None, test_message=True, test_user=recipient)
            if email_response == None:
                messages.success(request, 'Test e-mail sent to {0}'.format(recipient))
            else:
                messages.error(request, 'Test e-mail failed: {0}'.format(email_response))

        all_users = User.objects.all()
        for user in all_users:
            if str(user.pk) in request.POST.values():
                if not hasattr(user, 'highdosemetricalertrecipients'):
                    new_objects = HighDoseMetricAlertRecipients.objects.create(user=user)
                    new_objects.save()
                user.highdosemetricalertrecipients.receive_high_dose_metric_alerts = True
            else:
                if not hasattr(user, 'highdosemetricalertrecipients'):
                    new_objects = HighDoseMetricAlertRecipients.objects.create(user=user)
                    new_objects.save()
                user.highdosemetricalertrecipients.receive_high_dose_metric_alerts = False
            user.save()

    f = User.objects.order_by('username')

    admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}

    for group in request.user.groups.all():
        admin[group.name] = True

    return_structure = {'user_list': f, 'admin': admin}

    return render_to_response(
        'remapp/rfalertnotificationsview.html',
        return_structure,
        context_instance=RequestContext(request)
    )


@login_required
def rf_recalculate_accum_doses(request):  # pylint: disable=unused-variable
    """View to recalculate the summed total DAP and total dose at RP for all RF studies

    """
    from django.http import JsonResponse

    if not request.user.groups.filter(name="admingroup"):
        # Send the user to the home page
        return HttpResponseRedirect(reverse('home'))
    else:
        # Empty the PKsForSummedRFDoseStudiesInDeltaWeeks table
        from remapp.models import PKsForSummedRFDoseStudiesInDeltaWeeks
        PKsForSummedRFDoseStudiesInDeltaWeeks.objects.all().delete()

        # In the AccumIntegratedProjRadiogDose table delete all dose_area_product_total_over_delta_weeks and dose_rp_total_over_delta_weeks entries
        from remapp.models import AccumIntegratedProjRadiogDose
        AccumIntegratedProjRadiogDose.objects.all().update(dose_area_product_total_over_delta_weeks=None, dose_rp_total_over_delta_weeks=None)

        # For each RF study recalculate dose_area_product_total_over_delta_weeks and dose_rp_total_over_delta_weeks
        from datetime import timedelta
        from django.db.models import Sum
        from remapp.models import HighDoseMetricAlertSettings

        try:
            HighDoseMetricAlertSettings.objects.get()
        except ObjectDoesNotExist:
            HighDoseMetricAlertSettings.objects.create()
        week_delta = HighDoseMetricAlertSettings.objects.values_list('accum_dose_delta_weeks', flat=True)[0]

        all_rf_studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').all()

        for study in all_rf_studies:
            try:
                study.patientmoduleattr_set.get()
                patient_id = study.patientmoduleattr_set.values_list('patient_id', flat=True)[0]
            except ObjectDoesNotExist:
                patient_id = None

            if patient_id:
                study_date = study.study_date
                oldest_date = (study_date - timedelta(weeks=week_delta))

                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # The try and except parts of this code are here because some of the studies in my database didn't have the
                # expected data in the related fields - not sure why. Perhaps an issue with the extractor routine?
                try:
                    study.projectionxrayradiationdose_set.get().accumxraydose_set.all()
                except ObjectDoesNotExist:
                    study.projectionxrayradiationdose_set.get().accumxraydose_set.create()

                for accumxraydose in study.projectionxrayradiationdose_set.get().accumxraydose_set.all():
                    try:
                        accumxraydose.accumintegratedprojradiogdose_set.get()
                    except:
                        accumxraydose.accumintegratedprojradiogdose_set.create()

                for accumxraydose in study.projectionxrayradiationdose_set.get().accumxraydose_set.all():
                    accum_int_proj_pk = accumxraydose.accumintegratedprojradiogdose_set.get().pk

                    accum_int_proj_to_update = AccumIntegratedProjRadiogDose.objects.get(pk=accum_int_proj_pk)

                    included_studies = all_rf_studies.filter(patientmoduleattr__patient_id__exact=patient_id, study_date__range=[oldest_date, study_date])

                    bulk_entries = []
                    for pk in included_studies.values_list('pk', flat=True):
                        new_entry = PKsForSummedRFDoseStudiesInDeltaWeeks()
                        new_entry.general_study_module_attributes_id = study.pk
                        new_entry.study_pk_in_delta_weeks = pk
                        bulk_entries.append(new_entry)

                    if len(bulk_entries):
                        PKsForSummedRFDoseStudiesInDeltaWeeks.objects.bulk_create(bulk_entries)

                    accum_totals = included_studies.aggregate(Sum('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total'),
                                                              Sum('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total'))
                    accum_int_proj_to_update.dose_area_product_total_over_delta_weeks = accum_totals['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__sum']
                    accum_int_proj_to_update.dose_rp_total_over_delta_weeks = accum_totals['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total__sum']
                    accum_int_proj_to_update.save()

        HighDoseMetricAlertSettings.objects.all().update(changed_accum_dose_delta_weeks=False)

        messages.success(request, 'All summed total DAP and total dose at RP doses have been re-calculated')

        django_messages = []
        for message in messages.get_messages(request):
            django_messages.append({
                'level': message.level_tag,
                'message': message.message,
                'extra_tags': message.tags,
            })

        return_structure = {
            'success': True,
            'messages': django_messages
        }

        return JsonResponse(return_structure, safe=False)


class SkinDoseMapCalcSettingsUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView for configuring the skin dose map calculation choices

    """
    from remapp.models import SkinDoseMapCalcSettings
    from remapp.forms import SkinDoseMapCalcSettingsForm
    from django.core.exceptions import ObjectDoesNotExist

    try:
        SkinDoseMapCalcSettings.objects.get()
    except ObjectDoesNotExist:
        SkinDoseMapCalcSettings.objects.create()

    model = SkinDoseMapCalcSettings
    form_class = SkinDoseMapCalcSettingsForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, "Skin dose map settings have been updated")
        else:
            messages.info(self.request, "No changes made")
        return super(SkinDoseMapCalcSettingsUpdate, self).form_valid(form)


class NotPatientNameCreate(CreateView):  # pylint: disable=unused-variable
    """CreateView for configuration of indicators a study might not be a patient study

    """
    from remapp.forms import NotPatientNameForm
    from remapp.models import NotPatientIndicatorsName

    model = NotPatientIndicatorsName
    form_class = NotPatientNameForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class NotPatientNameUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView to update choices regarding not-patient indicators

    """
    from remapp.forms import NotPatientNameForm
    from remapp.models import NotPatientIndicatorsName

    model = NotPatientIndicatorsName
    form_class = NotPatientNameForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class NotPatientNameDelete(DeleteView):  # pylint: disable=unused-variable
    """DeleteView for the not-patient name indicator table

    """
    from remapp.models import NotPatientIndicatorsName

    model = NotPatientIndicatorsName
    success_url = reverse_lazy('not_patient_indicators')

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class NotPatientIDCreate(CreateView):  # pylint: disable=unused-variable
    """CreateView for not-patient ID indicators

    """
    from remapp.forms import NotPatientIDForm
    from remapp.models import NotPatientIndicatorsID

    model = NotPatientIndicatorsID
    form_class = NotPatientIDForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class NotPatientIDUpdate(UpdateView):  # pylint: disable=unused-variable
    """UpdateView for non-patient ID indicators

    """
    from remapp.forms import NotPatientIDForm
    from remapp.models import NotPatientIndicatorsID

    model = NotPatientIndicatorsID
    form_class = NotPatientIDForm

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context


class NotPatientIDDelete(DeleteView):  # pylint: disable=unused-variable
    """DeleteView for non-patient ID indicators

    """
    from remapp.models import NotPatientIndicatorsID

    model = NotPatientIndicatorsID
    success_url = reverse_lazy('not_patient_indicators')

    def get_context_data(self, **context):
        context[self.context_object_name] = self.object
        admin = {'openremversion': remapp.__version__, 'docsversion': remapp.__docs_version__}
        for group in self.request.user.groups.all():
            admin[group.name] = True
        context['admin'] = admin
        return context
