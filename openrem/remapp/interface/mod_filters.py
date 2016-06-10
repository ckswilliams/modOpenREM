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

# Following three lines added so that sphinx autodocumentation works. 
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
from django.db import models

import logging
import django_filters
from django import forms
from remapp.models import GeneralStudyModuleAttr
from django.utils.safestring import mark_safe

TEST_CHOICES = (('', 'Yes (default)'), (2, 'No (caution)'),)

def custom_name_filter(queryset, value):
    if not value:
        return queryset

    from django.db.models import Q
    from remapp.tools.hash_id import hash_id
    filtered = queryset.filter(
        (
            Q(patientmoduleattr__name_hashed = False) & Q(patientmoduleattr__patient_name__icontains = value)
         ) | (
            Q(patientmoduleattr__name_hashed = True) & Q(patientmoduleattr__patient_name__exact = hash_id(value))
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
            Q(patientmoduleattr__id_hashed = False) & Q(patientmoduleattr__patient_id__icontains = value)
         ) | (
            Q(patientmoduleattr__id_hashed = True) & Q(patientmoduleattr__patient_id__exact = hash_id(value))
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
            Q(accession_hashed = False) & Q(accession_number__icontains = value)
         ) | (
            Q(accession_hashed = True) & Q(accession_number__exact = hash_id(value))
        )
    )
    return filtered


def dap_min_filter(queryset, value):
    if not value:
        return queryset

    from decimal import Decimal, InvalidOperation
    try:
        value_gy_m2 = Decimal(value) / Decimal(1000000)
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
        value_gy_m2 = Decimal(value) / Decimal(1000000)
    except InvalidOperation:
        return queryset
    filtered = queryset.filter(
        projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__lte=
        value_gy_m2)
    return filtered


class RFSummaryListFilter(django_filters.FilterSet):
    """Filter for fluoroscopy studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label='Study description')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Manufacturer', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    performing_physician_name = django_filters.CharFilter(lookup_type='icontains', label='Physician')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label='Accession number')
    display_name = django_filters.CharFilter(lookup_type='icontains', label='Display name', name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    study_dap_min = django_filters.MethodFilter(action=dap_min_filter, label=mark_safe('Min study DAP (cGy.cm<sup>2</sup>)'))
    study_dap_max = django_filters.MethodFilter(action=dap_max_filter, label=mark_safe('Max study DAP (cGy.cm<sup>2</sup>)'))
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label="Include possible test data", name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES, widget=forms.Select)

    class Meta:
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
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total','Total DAP'),
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total','Total RP Dose'),
            )
    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(RFSummaryListFilter, self).get_order_by(order_value)


class RFFilterPlusPid(RFSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(RFFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label='Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label='Patient ID')


class CTSummaryListFilter(django_filters.FilterSet):
    """Filter for CT studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label='Study description')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label='Acquisition protocol', name='ctradiationdose__ctirradiationeventdata__acquisition_protocol')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label='Requested procedure', name='requested_procedure_code_meaning')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Make', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label='Accession number')
    study_dlp_min = django_filters.NumberFilter(lookup_type='gte', label='Min study DLP', name='ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')
    study_dlp_max = django_filters.NumberFilter(lookup_type='lte', label='Max study DLP', name='ctradiationdose__ctaccumulateddosedata__ct_dose_length_product_total')
    display_name = django_filters.CharFilter(lookup_type='icontains', label='Display name', name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label="Include possible test data", name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES, widget=forms.Select)

    class Meta:
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
            return ['-study_date','-study_time']
        return super(CTSummaryListFilter, self).get_order_by(order_value)


class CTFilterPlusPid(CTSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(CTFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label='Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label='Patient ID')


def ct_acq_filter(filters, pid=False):
    from decimal import Decimal, InvalidOperation
    from remapp.models import GeneralStudyModuleAttr, CtIrradiationEventData
    filteredInclude = []
    if 'acquisition_protocol' in filters and (
                    'acquisition_ctdi_min' in filters or 'acquisition_ctdi_max' in filters or
                        'acquisition_dlp_min' in filters or 'acquisition_dlp_max' in filters
    ):
        if ('studyhist' in filters) and ('study_description' in filters):
            events = CtIrradiationEventData.objects.select_related().filter(ct_radiation_dose_id__general_study_module_attributes__study_description=filters['study_description'])
        else:
            events = CtIrradiationEventData.objects.filter(acquisition_protocol__exact = filters['acquisition_protocol'])
        if 'acquisition_ctdi_min' in filters:
            try:
                Decimal(filters['acquisition_ctdi_min'])
                events = events.filter(mean_ctdivol__gte = filters['acquisition_ctdi_min'])
            except InvalidOperation:
                pass
        if 'acquisition_ctdi_max' in filters:
            try:
                Decimal(filters['acquisition_ctdi_max'])
                events = events.filter(mean_ctdivol__lte = filters['acquisition_ctdi_max'])
            except InvalidOperation:
                pass
        if 'acquisition_dlp_min' in filters:
            try:
                Decimal(filters['acquisition_dlp_min'])
                events = events.filter(dlp__gte = filters['acquisition_dlp_min'])
            except InvalidOperation:
                pass
        if 'acquisition_dlp_max' in filters:
            try:
                Decimal(filters['acquisition_dlp_max'])
                events = events.filter(dlp__lte = filters['acquisition_dlp_max'])
            except InvalidOperation:
                pass
        filteredInclude = list(set(
            [o.ct_radiation_dose.general_study_module_attributes.study_instance_uid for o in events]))

    elif ('study_description' in filters) and ('acquisition_ctdi_min' in filters) and ('acquisition_ctdi_max' in filters):
        events = CtIrradiationEventData.objects.select_related().filter(ct_radiation_dose_id__general_study_module_attributes__study_description=filters['study_description'])
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
        filteredInclude = list(set(
            [o.ct_radiation_dose.general_study_module_attributes.study_instance_uid for o in events]))

    studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact = 'CT')
    if filteredInclude:
        studies = studies.filter(study_instance_uid__in = filteredInclude)
    if pid:
        return CTFilterPlusPid(filters, studies.order_by().distinct())
    return CTSummaryListFilter(filters, studies.order_by().distinct())


class MGSummaryListFilter(django_filters.FilterSet):
    """Filter for mammography studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    procedure_code_meaning = django_filters.CharFilter(lookup_type='icontains', label='Procedure')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Manufacturer', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label='Accession number')
    display_name = django_filters.CharFilter(lookup_type='icontains', label='Display name', name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label="Include possible test data", name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES, widget=forms.Select)

    class Meta:
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
            ('-projectionxrayradiationdose__accumxraydose__accummammographyxraydose__accumulated_average_glandular_dose', 'Accumulated AGD'),
            )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(MGSummaryListFilter, self).get_order_by(order_value)

class MGFilterPlusPid(MGSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(MGFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label='Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label='Patient ID')


class DXSummaryListFilter(django_filters.FilterSet):
    """Filter for DX studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label='Study description')
    acquisition_protocol = django_filters.CharFilter(lookup_type='icontains', label='Acquisition protocol', name='projectionxrayradiationdose__irradeventxraydata__acquisition_protocol')
    requested_procedure = django_filters.CharFilter(lookup_type='icontains', label='Requested procedure', name='requested_procedure_code_meaning')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Make', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.MethodFilter(action=custom_acc_filter, label='Accession number')
    study_dap_min = django_filters.MethodFilter(action=dap_min_filter, label=mark_safe('Min study DAP (cGy.cm<sup>2</sup>)'))
    study_dap_max = django_filters.MethodFilter(action=dap_max_filter, label=mark_safe('Max study DAP (cGy.cm<sup>2</sup>)'))
    # acquisition_dap_max = django_filters.NumberFilter(lookup_type='lte', label=mark_safe('Max acquisition DAP (Gy.m<sup>2</sup>)'), name='projectionxrayradiationdose__irradeventxraydata__dose_area_product')
    # acquisition_dap_min = django_filters.NumberFilter(lookup_type='gte', label=mark_safe('Min acquisition DAP (Gy.m<sup>2</sup>)'), name='projectionxrayradiationdose__irradeventxraydata__dose_area_product')
    display_name = django_filters.CharFilter(lookup_type='icontains', label='Display name', name='generalequipmentmoduleattr__unique_equipment_name__display_name')
    test_data = django_filters.ChoiceFilter(lookup_type='isnull', label="Include possible test data", name='patientmoduleattr__not_patient_indicator', choices=TEST_CHOICES, widget=forms.Select)

    class Meta:
        model = GeneralStudyModuleAttr
        fields = [
            'date_after', 
            'date_before', 
            'institution_name', 
            'study_description',
            'acquisition_protocol',
            'patient_age_min',
            'patient_age_max',
            'manufacturer', 
            'model_name',
            'station_name',
            'display_name',
            'accession_number',
            #'study_dap_min',
            #'study_dap_max',
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
            ('-projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total', 'Total DAP'),
            )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(DXSummaryListFilter, self).get_order_by(order_value)

class DXFilterPlusPid(DXSummaryListFilter):
    def __init__(self, *args, **kwargs):
        super(DXFilterPlusPid, self).__init__(*args, **kwargs)
        self.filters['patient_name'] = django_filters.MethodFilter(action=custom_name_filter, label='Patient name')
        self.filters['patient_id'] = django_filters.MethodFilter(action=custom_id_filter, label='Patient ID')


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
        events = IrradEventXRayData.objects.filter(acquisition_protocol__exact = filters['acquisition_protocol'])
        if 'acquisition_dap_min' in filters:
            try:
                Decimal(filters['acquisition_dap_min'])
                events = events.filter(dose_area_product__gte = filters['acquisition_dap_min'])
            except InvalidOperation:
                pass
        if 'acquisition_dap_max' in filters:
            try:
                Decimal(filters['acquisition_dap_max'])
                events = events.filter(dose_area_product__lte = filters['acquisition_dap_max'])
            except InvalidOperation:
                pass
        if 'acquisition_kvp_min' in filters:
            try:
                Decimal(filters['acquisition_kvp_min'])
                events = events.filter(irradeventxraysourcedata__kvp__kvp__gte = filters['acquisition_kvp_min'])
            except InvalidOperation:
                pass
        if 'acquisition_kvp_max' in filters:
            try:
                Decimal(filters['acquisition_kvp_max'])
                events = events.filter(irradeventxraysourcedata__kvp__kvp__lte = filters['acquisition_kvp_max'])
            except InvalidOperation:
                pass
        if 'acquisition_mas_min' in filters:
            try:
                Decimal(filters['acquisition_mas_min'])
                events = events.filter(irradeventxraysourcedata__exposure__exposure__gte = filters['acquisition_mas_min'])
            except InvalidOperation:
                pass
        if 'acquisition_mas_max' in filters:
            try:
                Decimal(filters['acquisition_mas_max'])
                events = events.filter(irradeventxraysourcedata__exposure__exposure__lte = filters['acquisition_mas_max'])
            except InvalidOperation:
                pass
        filteredInclude = list(set(
            [o.projection_xray_radiation_dose.general_study_module_attributes.study_instance_uid for o in events]
        ))
    studies = GeneralStudyModuleAttr.objects.filter(
        Q(modality_type__exact='DX') | Q(modality_type__exact='CR'))
    if filteredInclude:
        studies = studies.filter(study_instance_uid__in = filteredInclude)
    if pid:
        return DXFilterPlusPid(filters, studies.order_by().distinct())
    return DXSummaryListFilter(filters, studies.order_by().distinct())