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
..  module:: mod_filters.
    :synopsis: Module for filtering studies on the summary filter pages.

..  moduleauthor:: Ed McDonagh

"""
from __future__ import division

from builtins import object  # pylint: disable=redefined-builtin
from past.utils import old_div
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
from django.db import models

import logging
import django_filters
from django import forms
from django.db.models import Count
from remapp.models import GeneralStudyModuleAttr
from django.utils.safestring import mark_safe

TEST_CHOICES = ((u'', u'Yes (default)'), (2, u'No (caution)'),)


def custom_name_filter(queryset, value):
    if not value:
        return queryset

    from django.db.models import Q
    from remapp.tools.hash_id import hash_id
    filtered = queryset.filter(
        (
                Q(patientmoduleattr__name_hashed=False) & Q(patientmoduleattr__patient_name__icontains=value)
        ) | (
                Q(patientmoduleattr__name_hashed=True) & Q(patientmoduleattr__patient_name__exact=hash_id(value))
        )
    )
    return filtered


def custom_id_filter(queryset, value):
    if not value:
        return queryset

    from django.db.models import Q
    from remapp.tools.hash_id import hash_id
    filtered = queryset.filter(
        (
                Q(patientmoduleattr__id_hashed=False) & Q(patientmoduleattr__patient_id__icontains=value)
        ) | (
                Q(patientmoduleattr__id_hashed=True) & Q(patientmoduleattr__patient_id__exact=hash_id(value))
        )
    )
    return filtered


def custom_acc_filter(queryset, value):
    if not value:
        return queryset

    from django.db.models import Q
    from remapp.tools.hash_id import hash_id
    filtered = queryset.filter(
        (
                Q(accession_hashed=False) & Q(accession_number__icontains=value)
        ) | (
                Q(accession_hashed=True) & Q(accession_number__exact=hash_id(value))
        )
    )
    return filtered


def dap_min_filter(queryset, value):
    if not value:
        return queryset

    from decimal import Decimal, InvalidOperation
    try:
        value_gy_m2 = old_div(Decimal(value), Decimal(1000000))
    except InvalidOperation:
        return queryset
    filtered = queryset.filter(
        projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__gte=
        value_gy_m2)
    return filtered


def dap_max_filter(queryset, value):
    if not value:
        return queryset

    from decimal import Decimal, InvalidOperation
    try:
        value_gy_m2 = old_div(Decimal(value), Decimal(1000000))
    except InvalidOperation:
        return queryset
    filtered = queryset.filter(
        projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__lte=
        value_gy_m2)
    return filtered


class RFSummaryListFilter(django_filters.FilterSet):
    """Filter for fluoroscopy studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label=u'Date from', name='study_date',
                                           widget=forms.TextInput(attrs={'class': 'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label=u'Date until', name='study_date',
                                            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label=u'Study description')
    procedure_code_meaning = django_filters.CharFilter(lookup_type='icontains', label=u'Procedure',
                                                       name='procedure_code_meaning')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label=u'Requested procedure',
                                                    name='requested_procedure_code_meaning')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label=u'Acquisition protocol',
                                                     name='projectionxrayradiationdose__irradeventxraydata__'
                                                          'acquisition_protocol')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label=u'Min age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label=u'Max age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label=u'Hospital',
                                                 name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label=u'Manufacturer',
                                             name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label=u'Model',
                                           name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label=u'Station name',
                                             name='generalequipmentmoduleattr__station_name')
    performing_physician_name = django_filters.CharFilter(lookup_type='icontains', label=u'Physician')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label=u'Accession number')
    display_name = django_filters.CharFilter(lookup_type='icontains', label=u'Display name',
                                             name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    study_dap_min = django_filters.MethodFilter(action=dap_min_filter,
                                                label=mark_safe(u'Min study DAP (cGy.cm<sup>2</sup>)'))  # nosec
    study_dap_max = django_filters.MethodFilter(action=dap_max_filter,
                                                label=mark_safe(u'Max study DAP (cGy.cm<sup>2</sup>)'))  # nosec
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label=u"Include possible test data",
                                            name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES,
                                            widget=forms.Select)

    class Meta(object):
        """
        Lists fields and order-by information for django-filter filtering
        """
        model = GeneralStudyModuleAttr
        fields = []
        order_by = (
            ('-study_date', mark_safe('Exam date &darr;')),
            ('study_date', mark_safe('Exam date &uarr;')),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('study_description', 'Study description'),
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
             'Total DAP'),
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total',
             'Total RP Dose'),
        )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date', '-study_time']
        return super(RFSummaryListFilter, self).get_order_by(order_value)


class RFFilterPlusPid(RFSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(RFFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label=u'Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label=u'Patient ID')


# Values from DICOM CID 10013 CT Acquisition Type
CT_ACQ_TYPE_CHOICES = (
    ('Spiral Acquisition', 'Spiral'),
    ('Sequenced Acquisition', 'Axial'),
    ('Constant Angle Acquisition', 'Localiser'),
    ('Stationary Acquisition', 'Stationary acquisition'),
    ('Free Acquisition', 'Free acquisition'),
)


EVENT_NUMBER_CHOICES = (
    (None, 'Any'),
    (0, 'None'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
)


def _specify_event_numbers_spiral(queryset, value):
    """Method filter for specifying number of spiral (helical) events in each study

    :param queryset: Study list
    :param value: number of events
    :return: filtered queryset
    """
    try:
        value = int(value)
    except ValueError:
        return queryset
    if value == 0:
        filtered = queryset.exclude(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Spiral Acquisition')
    else:
        study_uids = queryset.values_list('study_instance_uid')
        filtered = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=study_uids).filter(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Spiral Acquisition'
        ).annotate(
            spiral_count=Count('ctradiationdose__ctirradiationeventdata', distinct=True)
        ).filter(spiral_count=value)
    return filtered


def _specify_event_numbers_axial(queryset, value):
    """Method filter for specifying number of axial events in each study

    :param queryset: Study list
    :param value: number of events
    :return: filtered queryset
    """
    try:
        value = int(value)
    except ValueError:
        return queryset
    if value == 0:
        filtered = queryset.exclude(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Sequenced Acquisition')
    else:
        study_uids = queryset.values_list('study_instance_uid')
        filtered = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=study_uids).filter(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Sequenced Acquisition'
        ).annotate(
            axial_count=Count('ctradiationdose__ctirradiationeventdata', distinct=True)
        ).filter(axial_count=value)
    return filtered


def _specify_event_numbers_spr(queryset, value):
    """Method filter for specifying number of scan projection radiograph events in each study

    :param queryset: Study list
    :param value: number of events
    :return: filtered queryset
    """
    try:
        value = int(value)
    except ValueError:
        return queryset
    if value == 0:
        filtered = queryset.exclude(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition')
    else:
        study_uids = queryset.values_list('study_instance_uid')
        filtered = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=study_uids).filter(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Constant Angle Acquisition'
        ).annotate(
            spr_count=Count('ctradiationdose__ctirradiationeventdata', distinct=True)
        ).filter(spr_count=value)
    return filtered


def _specify_event_numbers_stationary(queryset, value):
    """Method filter for specifying number of scan projection radiograph events in each study

    :param queryset: Study list
    :param value: number of events
    :return: filtered queryset
    """
    try:
        value = int(value)
    except ValueError:
        return queryset
    if value == 0:
        filtered = queryset.exclude(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Stationary Acquisition')
    else:
        study_uids = queryset.values_list('study_instance_uid')
        filtered = GeneralStudyModuleAttr.objects.filter(study_instance_uid__in=study_uids).filter(
            ctradiationdose__ctirradiationeventdata__ct_acquisition_type__code_meaning__exact='Stationary Acquisition'
        ).annotate(
            stationary_count=Count('ctradiationdose__ctirradiationeventdata', distinct=True)
        ).filter(stationary_count=value)
    return filtered


class CTSummaryListFilter(django_filters.FilterSet):
    """Filter for CT studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label=u'Date from', name='study_date',
                                           widget=forms.TextInput(attrs={'class': 'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label=u'Date until', name='study_date',
                                            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label=u'Study description')
    procedure_code_meaning = django_filters.CharFilter(lookup_type='icontains', label=u'Procedure',
                                                       name='procedure_code_meaning')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label=u'Requested procedure',
                                                    name='requested_procedure_code_meaning')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label=u'Acquisition protocol',
                                                     name='ctradiationdose__ctirradiationeventdata__acquisition'
                                                          '_protocol')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label=u'Min age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label=u'Max age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label=u'Hospital',
                                                 name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label=u'Make',
                                             name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label=u'Model',
                                           name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label=u'Station name',
                                             name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label=u'Accession number')
    study_dlp_min = django_filters.NumberFilter(lookup_type='gte', label=u'Min study DLP',
                                                name='ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_'
                                                     'total')
    study_dlp_max = django_filters.NumberFilter(lookup_type='lte', label=u'Max study DLP',
                                                name='ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_'
                                                     'total')
    display_name = django_filters.CharFilter(lookup_type='icontains', label=u'Display name',
                                             name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label=u"Include possible test data",
                                            name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES,
                                            widget=forms.Select)
    ct_acquisition_type = django_filters.MultipleChoiceFilter(lookup_type='iexact',
                                                              label=u'Acquisition type restriction',
                                                              name='ctradiationdose__ctirradiationeventdata__ct_'
                                                                   'acquisition_type__code_meaning',
                                                              choices=CT_ACQ_TYPE_CHOICES,
                                                              widget=forms.CheckboxSelectMultiple)
    num_spiral_events = django_filters.ChoiceFilter(action=_specify_event_numbers_spiral, label=u'Num. spiral events',
                                                    choices=EVENT_NUMBER_CHOICES, widget=forms.Select)
    num_axial_events = django_filters.ChoiceFilter(action=_specify_event_numbers_axial, label=u'Num. axial events',
                                                   choices=EVENT_NUMBER_CHOICES, widget=forms.Select)
    num_spr_events = django_filters.ChoiceFilter(action=_specify_event_numbers_spr, label=u'Num. localisers',
                                                 choices=EVENT_NUMBER_CHOICES, widget=forms.Select)
    num_stationary_events = django_filters.ChoiceFilter(action=_specify_event_numbers_stationary,
                                                        label=u'Num. stationary events', choices=EVENT_NUMBER_CHOICES,
                                                        widget=forms.Select)

    class Meta(object):
        """
        Lists fields and order-by information for django-filter filtering
        """
        model = GeneralStudyModuleAttr
        fields = []
        order_by = (
            ('-study_date', mark_safe('Exam date &darr;')),
            ('study_date', mark_safe('Exam date &uarr;')),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('study_description', 'Study description'),
            ('-ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total', 'Total DLP'),
        )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date', '-study_time']
        return super(CTSummaryListFilter, self).get_order_by(order_value)


class CTFilterPlusPid(CTSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(CTFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label=u'Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label=u'Patient ID')


def ct_acq_filter(filters, pid=False):
    from decimal import Decimal, InvalidOperation
    from remapp.models import GeneralStudyModuleAttr, CtIrradiationEventData
    filteredInclude = []
    if 'acquisition_protocol' in filters and (
            'acquisition_ctdi_min' in filters or 'acquisition_ctdi_max' in filters or
            'acquisition_dlp_min' in filters or 'acquisition_dlp_max' in filters
    ):
        if ('studyhist' in filters) and ('study_description' in filters):
            events = CtIrradiationEventData.objects.select_related().filter(
                ct_radiation_dose_id__general_study_module_attributes__study_description=filters['study_description'])
        else:
            events = CtIrradiationEventData.objects.filter(acquisition_protocol__iexact=filters['acquisition_protocol'])
        if 'acquisition_ctdi_min' in filters:
            try:
                Decimal(filters['acquisition_ctdi_min'])
                events = events.filter(mean_ctdivol__gte=filters['acquisition_ctdi_min'])
            except InvalidOperation:
                pass
        if 'acquisition_ctdi_max' in filters:
            try:
                Decimal(filters['acquisition_ctdi_max'])
                events = events.filter(mean_ctdivol__lte=filters['acquisition_ctdi_max'])
            except InvalidOperation:
                pass
        if 'acquisition_dlp_min' in filters:
            try:
                Decimal(filters['acquisition_dlp_min'])
                events = events.filter(dlp__gte=filters['acquisition_dlp_min'])
            except InvalidOperation:
                pass
        if 'acquisition_dlp_max' in filters:
            try:
                Decimal(filters['acquisition_dlp_max'])
                events = events.filter(dlp__lte=filters['acquisition_dlp_max'])
            except InvalidOperation:
                pass
        if 'ct_acquisition_type' in filters:
            try:
                events = events.filter(ct_acquisition_type__code_meaning__iexact=filters['ct_acquisition_type'])
            except InvalidOperation:
                pass
        filteredInclude = events.values_list(
            'ct_radiation_dose__general_study_module_attributes__study_instance_uid').distinct()

    elif ('study_description' in filters) and ('acquisition_ctdi_min' in filters) and (
            'acquisition_ctdi_max' in filters):
        events = CtIrradiationEventData.objects.select_related().filter(
            ct_radiation_dose_id__general_study_module_attributes__study_description=filters['study_description'])
        if 'acquisition_ctdi_min' in filters:
            try:
                Decimal(filters['acquisition_ctdi_min'])
                events = events.filter(mean_ctdivol__gte=filters['acquisition_ctdi_min'])
            except InvalidOperation:
                pass
        if 'acquisition_ctdi_max' in filters:
            try:
                Decimal(filters['acquisition_ctdi_max'])
                events = events.filter(mean_ctdivol__lte=filters['acquisition_ctdi_max'])
            except InvalidOperation:
                pass
        if 'ct_acquisition_type' in filters:
            try:
                events = events.filter(ct_acquisition_type__code_meaning__iexact=filters['ct_acquisition_type'])
            except InvalidOperation:
                pass
        filteredInclude = events.values_list(
            'ct_radiation_dose__general_study_module_attributes__study_instance_uid').distinct()

    studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='CT')
    if filteredInclude:
        studies = studies.filter(study_instance_uid__in=filteredInclude)
    if pid:
        return CTFilterPlusPid(filters, studies.order_by().distinct())
    return CTSummaryListFilter(filters, studies.order_by().distinct())


class MGSummaryListFilter(django_filters.FilterSet):
    """Filter for mammography studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label=u'Date from', name='study_date',
                                           widget=forms.TextInput(attrs={'class': 'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label=u'Date until', name='study_date',
                                            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label=u'Study description')
    procedure_code_meaning = django_filters.CharFilter(lookup_type='icontains', label=u'Procedure',
                                                       name='procedure_code_meaning')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label=u'Requested procedure',
                                                    name='requested_procedure_code_meaning')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label=u'Acquisition protocol',
                                                     name='projectionxrayradiationdose__irradeventxraydata__'
                                                          'acquisition_protocol')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label=u'Min age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label=u'Max age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label=u'Hospital',
                                                 name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label=u'Manufacturer',
                                             name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label=u'Model',
                                           name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label=u'Station name',
                                             name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label=u'Accession number')
    display_name = django_filters.CharFilter(lookup_type='icontains', label=u'Display name',
                                             name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label=u"Include possible test data",
                                            name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES,
                                            widget=forms.Select)

    class Meta(object):
        """
        Lists fields and order-by information for django-filter filtering
        """

        model = GeneralStudyModuleAttr
        fields = [
        ]

        order_by = (
            ('-study_date', mark_safe('Exam date &darr;')),
            ('study_date', mark_safe('Exam date &uarr;')),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('procedure_code_meaning', 'Procedure'),
            ('-projectionxrayradiationdose__accumxraydose__accummammographyxraydose__accumulated_average_glandular_'
             'dose', 'Accumulated AGD'),
        )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date', '-study_time']
        return super(MGSummaryListFilter, self).get_order_by(order_value)


class MGFilterPlusPid(MGSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(MGFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label=u'Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label=u'Patient ID')


class DXSummaryListFilter(django_filters.FilterSet):
    """Filter for DX studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label=u'Date from', name='study_date',
                                           widget=forms.TextInput(attrs={'class': 'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label=u'Date until', name='study_date',
                                            widget=forms.TextInput(attrs={'class': 'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label=u'Study description')
    procedure_code_meaning = django_filters.CharFilter(lookup_type='icontains', label=u'Procedure',
                                                       name='procedure_code_meaning')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label=u'Requested procedure',
                                                    name='requested_procedure_code_meaning')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label=u'Acquisition protocol',
                                                     name='projectionxrayradiationdose__irradeventxraydata__'
                                                          'acquisition_protocol')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label=u'Min age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label=u'Max age (yrs)',
                                                  name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label=u'Hospital',
                                                 name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label=u'Make',
                                             name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label=u'Model',
                                           name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label=u'Station name',
                                             name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label=u'Accession number')
    study_dap_min = django_filters.MethodFilter(action=dap_min_filter,
                                                label=mark_safe(u'Min study DAP (cGy.cm<sup>2</sup>)'))  # nosec
    study_dap_max = django_filters.MethodFilter(action=dap_max_filter,
                                                label=mark_safe(u'Max study DAP (cGy.cm<sup>2</sup>)'))  # nosec
    # acquisition_dap_max = django_filters.NumberFilter(lookup_type='lte', label=mark_safe('Max acquisition DAP (Gy.m<sup>2</sup>)'), name='projectionxrayradiationdose__irradeventxraydata__dose_area_product') # nosec
    # acquisition_dap_min = django_filters.NumberFilter(lookup_type='gte', label=mark_safe('Min acquisition DAP (Gy.m<sup>2</sup>)'), name='projectionxrayradiationdose__irradeventxraydata__dose_area_product') # nosec
    display_name = django_filters.CharFilter(lookup_type='icontains', label=u'Display name',
                                             name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label=u"Include possible test data",
                                            name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES,
                                            widget=forms.Select)

    class Meta(object):
        """
        Lists fields and order-by information for django-filter filtering
        """
        model = GeneralStudyModuleAttr
        fields = [
            'date_after',
            'date_before',
            'institution_name',
            'study_description',
            'procedure_code_meaning',
            'requested_procedure',
            'acquisition_protocol',
            'patient_age_min',
            'patient_age_max',
            'manufacturer',
            'model_name',
            'station_name',
            'display_name',
            'accession_number',
            # 'study_dap_min',
            # 'study_dap_max',
            'test_data',
        ]
        order_by = (
            ('-study_date', mark_safe('Exam date &darr;')),
            ('study_date', mark_safe('Exam date &uarr;')),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('study_description', 'Study description'),
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
             'Total DAP'),
        )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date', '-study_time']
        return super(DXSummaryListFilter, self).get_order_by(order_value)


class DXFilterPlusPid(DXSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(DXFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label=u'Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label=u'Patient ID')


def dx_acq_filter(filters, pid=False):
    from decimal import Decimal, InvalidOperation
    from django.db.models import Q
    from remapp.models import GeneralStudyModuleAttr, IrradEventXRayData
    filteredInclude = []
    if 'acquisition_protocol' in filters and (
            'acquisition_dap_min' in filters or 'acquisition_dap_max' in filters or
            'acquisition_kvp_min' in filters or 'acquisition_kvp_max' in filters or
            'acquisition_mas_min' in filters or 'acquisition_mas_max' in filters
    ):
        events = IrradEventXRayData.objects.filter(acquisition_protocol__iexact=filters['acquisition_protocol'])
        if 'acquisition_dap_min' in filters:
            try:
                Decimal(filters['acquisition_dap_min'])
                events = events.filter(dose_area_product__gte=filters['acquisition_dap_min'])
            except InvalidOperation:
                pass
        if 'acquisition_dap_max' in filters:
            try:
                Decimal(filters['acquisition_dap_max'])
                events = events.filter(dose_area_product__lte=filters['acquisition_dap_max'])
            except InvalidOperation:
                pass
        if 'acquisition_kvp_min' in filters:
            try:
                Decimal(filters['acquisition_kvp_min'])
                events = events.filter(irradeventxraysourcedata__kvp__kvp__gte=filters['acquisition_kvp_min'])
            except InvalidOperation:
                pass
        if 'acquisition_kvp_max' in filters:
            try:
                Decimal(filters['acquisition_kvp_max'])
                events = events.filter(irradeventxraysourcedata__kvp__kvp__lte=filters['acquisition_kvp_max'])
            except InvalidOperation:
                pass
        if 'acquisition_mas_min' in filters:
            try:
                Decimal(filters['acquisition_mas_min'])
                events = events.filter(irradeventxraysourcedata__exposure__exposure__gte=filters['acquisition_mas_min'])
            except InvalidOperation:
                pass
        if 'acquisition_mas_max' in filters:
            try:
                Decimal(filters['acquisition_mas_max'])
                events = events.filter(irradeventxraysourcedata__exposure__exposure__lte=filters['acquisition_mas_max'])
            except InvalidOperation:
                pass
        filteredInclude = events.values_list(
            'projection_xray_radiation_dose__general_study_module_attributes__study_instance_uid').distinct()

    studies = GeneralStudyModuleAttr.objects.filter(
        Q(modality_type__exact='DX') | Q(modality_type__exact='CR'))
    if filteredInclude:
        studies = studies.filter(study_instance_uid__in=filteredInclude)
    if pid:
        return DXFilterPlusPid(filters, studies.order_by().distinct())
    return DXSummaryListFilter(filters, studies.order_by().distinct())
