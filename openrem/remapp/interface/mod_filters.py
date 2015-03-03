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

import django_filters
from django import forms
from remapp.models import GeneralStudyModuleAttr


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
    accession_number = django_filters.CharFilter(lookup_type='icontains', label='Accession number')
    class Meta:
        model = GeneralStudyModuleAttr
        fields = [
            'date_after', 
            'date_before', 
            'institution_name', 
            'study_description',
            'patient_age_min',
            'patient_age_max',
            'manufacturer', 
            'model_name',
            'station_name',
            'performing_physician_name',
            'accession_number',
            ]
        order_by = (
            ('-study_date', 'Date of exam (newest first)'),
            ('study_date', 'Date of exam (oldest first)'),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('study_description', 'Study description'),
            ('-projectionxrayradiationdose__accumxraydose__accumprojxraydose__dose_area_product_total','Total DAP'),
            ('-projectionxrayradiationdose__accumxraydose__accumprojxraydose__dose_rp_total','Total RP Dose'),
            )
    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(CTSummaryListFilter, self).get_order_by(order_value)


class CTSummaryListFilter(django_filters.FilterSet):
    """Filter for CT studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label='Study description')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Make', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.CharFilter(lookup_type='icontains', label='Accession number')
    class Meta:
        model = GeneralStudyModuleAttr
        fields = [
            'date_after', 
            'date_before', 
            'institution_name', 
            'study_description',
            'patient_age_min',
            'patient_age_max',
            'manufacturer', 
            'model_name',
            'station_name',
            'accession_number',
            ]
        order_by = (
            ('-study_date', 'Date of exam (newest first)'),
            ('study_date', 'Date of exam (oldest first)'),
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
    accession_number = django_filters.CharFilter(lookup_type='icontains', label='Accession number')
    class Meta:
        model = GeneralStudyModuleAttr
        fields = [
            'date_after', 
            'date_before', 
            'institution_name', 
            'procedure_code_meaning',
            'patient_age_min',
            'patient_age_max',
            'manufacturer', 
            'model_name',
            'station_name',
            'accession_number',
            ]
        order_by = (
            ('-study_date', 'Date of exam (newest first)'),
            ('study_date', 'Date of exam (oldest first)'),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('procedure_code_meaning', 'Procedure'),
            )
    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(CTSummaryListFilter, self).get_order_by(order_value)

class DXSummaryListFilter(django_filters.FilterSet):
    """Filter for DX studies to display in web interface.

    """
    date_after = django_filters.DateFilter(lookup_type='gte', label='Date from', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    date_before = django_filters.DateFilter(lookup_type='lte', label='Date until', name='study_date', widget=forms.TextInput(attrs={'class':'datepicker'}))
    study_description = django_filters.CharFilter(lookup_type='icontains', label='Study description')
    patient_age_min = django_filters.NumberFilter(lookup_type='gt', label='Min age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    patient_age_max = django_filters.NumberFilter(lookup_type='lt', label='Max age (yrs)', name='patientstudymoduleattr__patient_age_decimal')
    institution_name = django_filters.CharFilter(lookup_type='icontains', label='Hospital', name='generalequipmentmoduleattr__institution_name')
    manufacturer = django_filters.CharFilter(lookup_type='icontains', label='Make', name='generalequipmentmoduleattr__manufacturer')
    model_name = django_filters.CharFilter(lookup_type='icontains', label='Model', name='generalequipmentmoduleattr__manufacturer_model_name')
    station_name = django_filters.CharFilter(lookup_type='icontains', label='Station name', name='generalequipmentmoduleattr__station_name')
    accession_number = django_filters.CharFilter(lookup_type='icontains', label='Accession number')
    class Meta:
        model = GeneralStudyModuleAttr
        fields = [
            'date_after', 
            'date_before', 
            'institution_name', 
            'study_description',
            'patient_age_min',
            'patient_age_max',
            'manufacturer', 
            'model_name',
            'station_name',
            'accession_number',
            ]
        order_by = (
            ('-study_date', 'Date of exam (newest first)'),
            ('study_date', 'Date of exam (oldest first)'),
            ('generalequipmentmoduleattr__institution_name', 'Hospital'),
            ('generalequipmentmoduleattr__manufacturer', 'Make'),
            ('generalequipmentmoduleattr__manufacturer_model_name', 'Model name'),
            ('generalequipmentmoduleattr__station_name', 'Station name'),
            ('study_description', 'Study description'),
            ('-projectionxrayradiationdose__accumxraydose__accumprojxraydose__dose_area_product_total','Total DAP'),
            )

    def get_order_by(self, order_value):
        if order_value == 'study_date':
            return ['study_date', 'study_time']
        elif order_value == '-study_date':
            return ['-study_date','-study_time']
        return super(DXSummaryListFilter, self).get_order_by(order_value)
