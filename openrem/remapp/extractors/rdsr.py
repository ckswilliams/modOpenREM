
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
..  module:: rdsr.
    :synopsis: Module to extract radiation dose related data from DICOM Radiation SR objects.

..  moduleauthor:: Ed McDonagh

"""

import os
import sys
import logging
import django
import logging

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1,projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from celery import shared_task

def _observercontext(dataset,obs): # TID 1002
    from remapp.tools.get_values import get_or_create_cid
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Observer Type':
            obs.observer_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer UID':
            obs.device_observer_uid = cont.UID
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Name':
            obs.device_observer_name = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Manufacturer':
            obs.device_observer_manufacturer = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Model Name':
            obs.device_observer_model_name = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Serial Number':
            obs.device_observer_serial_number = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Physical Location during observation':
            obs.device_observer_physical_location_during_observation = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Role in Procedure':
            obs.device_role_in_procedure = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
    obs.save()
    
def _deviceparticipant(dataset,eventdatatype,foreignkey):
    from remapp.models import DeviceParticipant
    from remapp.tools.get_values import get_or_create_cid
    if eventdatatype == 'detector':
        device = DeviceParticipant.objects.create(irradiation_event_xray_detector_data=foreignkey)
    elif eventdatatype == 'source':
        device = DeviceParticipant.objects.create(irradiation_event_xray_source_data=foreignkey)
    elif eventdatatype == 'accumulated':
        device = DeviceParticipant.objects.create(accumulated_xray_dose=foreignkey)
    elif eventdatatype == 'ct_accumulated':
        device = DeviceParticipant.objects.create(ct_accumulated_dose_data=foreignkey)
    elif eventdatatype == 'ct_event':
        device = DeviceParticipant.objects.create(ct_irradiation_event_data=foreignkey)
    else:
        print "Doh"
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Role in Procedure':
            device.device_role_in_procedure = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Name':
                    device.device_name = cont2.TextValue
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Manufacturer':
                    device.device_manufacturer = cont2.TextValue
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Model Name':
                    device.device_model_name = cont2.TextValue
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Serial Number':
                    device.device_serial_number = cont2.TextValue
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer UID':
                    device.device_observer_uid = cont2.UID
    device.save()

def _pulsewidth(dataset,source):
    from remapp.models import PulseWidth
    pulse = PulseWidth.objects.create(irradiation_event_xray_source_data=source)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Pulse Width':
            pulse.pulse_width = cont.MeasuredValueSequence[0].NumericValue
    pulse.save()

def _kvptable(dataset,source):
    from remapp.models import Kvp
    kvpdata = Kvp.objects.create(irradiation_event_xray_source_data=source)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'KVP':
            kvpdata.kvp = cont.MeasuredValueSequence[0].NumericValue
    kvpdata.save()

def _xraytubecurrent(dataset,source):
    from remapp.models import XrayTubeCurrent
    tubecurrent = XrayTubeCurrent.objects.create(irradiation_event_xray_source_data=source)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Tube Current':
            tubecurrent.xray_tube_current = cont.MeasuredValueSequence[0].NumericValue
    tubecurrent.save()

def _exposure(dataset,source):
    from remapp.models import Exposure
    exposure = Exposure.objects.create(irradiation_event_xray_source_data=source)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure':
            exposure.exposure = cont.MeasuredValueSequence[0].NumericValue
    exposure.save()

def _xrayfilters(dataset,source):
    from remapp.models import XrayFilters
    from remapp.tools.get_values import get_or_create_cid
    filters = XrayFilters.objects.create(irradiation_event_xray_source_data=source)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filters':
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Type':
                    filters.xray_filter_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Material':
                    filters.xray_filter_material = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Thickness Minimum':
                    filters.xray_filter_thickness_minimum = cont2.MeasuredValueSequence[0].NumericValue
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Thickness Maximum':
                    filters.xray_filter_thickness_maximum = cont2.MeasuredValueSequence[0].NumericValue
    filters.save()


def _doserelateddistancemeasurements(dataset,mech): #CID 10008
    from remapp.models import DoseRelatedDistanceMeasurements
    distance = DoseRelatedDistanceMeasurements.objects.create(irradiation_event_xray_mechanical_data=mech)
    codes = {   'Distance Source to Isocenter'      :'distance_source_to_isocenter',
                'Distance Source to Reference Point':'distance_source_to_reference_point',
                'Distance Source to Detector'       :'distance_source_to_detector',
                'Table Longitudinal Position'       :'table_longitudinal_position',
                'Table Lateral Position'            :'table_lateral_position',
                'Table Height Position'             :'table_height_position',
                'Distance Source to Table Plane'    :'distance_source_to_table_plane'}
    for cont in dataset.ContentSequence:
        try:
            setattr(distance,codes[cont.ConceptNameCodeSequence[0].CodeMeaning],cont.MeasuredValueSequence[0].NumericValue)
        except KeyError:
            pass
    distance.save()

def _irradiationeventxraymechanicaldata(dataset,event): #TID 10003c
    from remapp.models import IrradEventXRayMechanicalData
    from remapp.tools.get_values import get_or_create_cid
    mech = IrradEventXRayMechanicalData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CR/DR Mechanical Configuration':
            mech.crdr_mechanical_configuration = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Primary Angle':
            mech.positioner_primary_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Secondary Angle':
            mech.positioner_secondary_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Primary End Angle':
            mech.positioner_primary_end_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Secondary End Angle':
            mech.positioner_secondary_end_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Column Angulation':
            mech.column_angulation = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Head Tilt Angle':
            mech.table_head_tilt_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Horizontal Rotation Angle':
            mech.table_horizontal_rotation_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Cradle Tilt Angle':
            mech.table_cradle_tilt_angle = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Compression Thickness':
            mech.compression_thickness = cont.MeasuredValueSequence[0].NumericValue
    _doserelateddistancemeasurements(dataset,mech)
    mech.save()

def _irradiationeventxraysourcedata(dataset,event): #TID 10003b
    # TODO: review model to convert to cid where appropriate, and add additional fields
    from remapp.models import IrradEventXRaySourceData
    from remapp.tools.get_values import get_or_create_cid
    from xml.etree import ElementTree as ET
    source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP)':
            source.dose_rp = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
            # this will fail if the text value is present instead of the code
            source.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Average Glandular Dose':
            source.average_glandular_dose = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Mode':
            source.fluoro_mode = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Pulse Rate':
            source.pulse_rate = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Number of Pulses':
            source.number_of_pulses = cont.MeasuredValueSequence[0].NumericValue
            # should be a derivation thing in here for when the no. pulses is estimated
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Duration':
            source.irradiation_duration = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Average X-Ray Tube Current':
            source.average_xray_tube_current = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time':
            source.exposure_time = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Focal Spot Size':
            source.focal_spot_size = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Anode Target Material':
            source.anode_target_material = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Collimated Field Area':
            source.collimated_field_area = cont.MeasuredValueSequence[0].NumericValue
        # TODO: xray_grid no longer exists in this table - it is a model on its own... See https://bitbucket.org/openrem/openrem/issue/181
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Grid':
            source.xray_grid = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
    _pulsewidth(dataset,source)
    _kvptable(dataset,source)
    _xraytubecurrent(dataset,source)
    _exposure(dataset,source)
    _xrayfilters(dataset,source)
    _deviceparticipant(dataset,'source',source)
    try:
        source.ii_field_size = ET.fromstring(source.irradiation_event_xray_data.comment).find('iiDiameter').get('SRData')
    except:
        pass
    source.save()

def _irradiationeventxraydetectordata(dataset,event): #TID 10003a
    from remapp.models import IrradEventXRayDetectorData
    detector = IrradEventXRayDetectorData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Index':
            detector.exposure_index = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Target Exposure Index':
            detector.target_exposure_index = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Deviation Index':
            detector.deviation_index = cont.MeasuredValueSequence[0].NumericValue
    _deviceparticipant(dataset,'detector',detector)
    detector.save()
        
def _imageviewmodifier(dataset,event):
    from remapp.models import ImageViewModifier
    from remapp.tools.get_values import get_or_create_cid
    modifier = ImageViewModifier.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Image View Modifier':
            modifier.image_view_modifier = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        # TODO: Projection Eponymous Name should be in here - needs db change
    modifier.save()


def _irradiationeventxraydata(dataset,proj):  # TID 10003
    # TODO: review model to convert to cid where appropriate, and add additional fields
    from remapp.models import IrradEventXRayData
    from remapp.tools.get_values import get_or_create_cid
    from remapp.tools.dcmdatetime import make_date_time
    event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Plane':
            event.acquisition_plane = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event UID':
            event.irradiation_event_uid = cont.UID
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event Label':
            event.irradiation_event_label = cont.TextValue
            for cont2 in cont.ContentSequence:
                if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Label Type':
                    event.label_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DateTime Started':
            event.date_time_started = make_date_time(cont.DateTime)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event Type':
            event.irradiation_event_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Protocol':
            event.acquisition_protocol = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Anatomical structure':
            event.anatomical_structure = cont.CodeValue
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Laterality':
                    event.laterality = cont2.ConceptCodeSequence[0].CodeValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Image View':
            event.image_view = cont.CodeValue
            _imageviewmodifier(cont,event)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Table Relationship':
            event.patient_table_relationship_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Orientation':
            event.patient_orientation_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Orientation Modifier':
            event.patient_orientation_modifier_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Target Region':
            event.target_region = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product':
            event.dose_area_product = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Half Value Layer':
            event.half_value_layer = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Entrance Exposure at RP':
            event.entrance_exposure_at_rp = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
            event.reference_point_definition = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Mammography CAD Breast Composition':
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNamesCodes[0].CodeMeaning == 'Breast Composition':
                        event.breast_composition = cont2.CodeValue
                    if cont2.ConceptNamesCodes[0].CodeMeaning == 'Percent Fibroglandular Tissue':
                        event.percent_fibroglandular_tissue = cont2.NumericValue 
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            event.comment = cont.TextValue
    
    # needs include for optional multiple person participant
    _irradiationeventxraydetectordata(dataset,event)
    _irradiationeventxraysourcedata(dataset,event)
    _irradiationeventxraymechanicaldata(dataset,event)

    event.save()

def _calibration(dataset,accum): 
    from remapp.models import Calibration
    from remapp.tools.get_values import get_or_create_cid
    from remapp.tools.dcmdatetime import make_date_time
    cal = Calibration.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Measurement Device':
            cal.dose_measurement_device = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Date':
            cal.calibration_date = make_date_time(cont.DateTime)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Factor':
            cal.calibration_factor = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Uncertainty':
            cal.calibration_uncertainty = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Responsible Party':
            cal.calibration_responsible_party = cont.TextValue
    cal.save()

def _accumulatedmammoxraydose(dataset,accum): # TID 10005
    from remapp.models import AccumMammographyXRayDose
    from remapp.tools.get_values import get_or_create_cid
    accummammo = AccumMammographyXRayDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated Average Glandular Dose':
            accummammo.accumulated_average_glandular_dose = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Laterality':
            accummammo.laterality = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
    accummammo.save()

def _accumulatedprojectionxraydose(dataset,accum): # TID 10004
    from remapp.tools.get_values import get_or_create_cid
    from remapp.models import AccumProjXRayDose
    accumproj = AccumProjXRayDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Dose Area Product Total':
            accumproj.fluoro_dose_area_product_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Dose (RP) Total':
            accumproj.fluoro_dose_rp_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Fluoro Time':
            accumproj.total_fluoro_time = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Dose Area Product Total':
            accumproj.acquisition_dose_area_product_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Dose (RP) Total':
            accumproj.acquisition_dose_rp_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Acquisition Time':
            accumproj.total_acquisition_time = cont.MeasuredValueSequence[0].NumericValue
        # TODO: Remove the following four items, as they are also imported (correctly) into _accumulatedintegratedprojectionradiographydose
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product Total':
            accumproj.dose_area_product_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP) Total':
            accumproj.dose_rp_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
            accumproj.total_number_of_radiographic_frames = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
            # will break if text instead of code?
            accumproj.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
    if (accumproj.fluoro_dose_area_product_total != "" or
        accumproj.total_fluoro_time != "" or
        accumproj.acquisition_dose_area_product_total != "" or
        accumproj.total_acquisition_time != ""):
            accumproj.accumulated_xray_dose.projection_xray_radiation_dose.general_study_module_attributes.modality_type = 'RF'
    elif accumproj.total_number_of_radiographic_frames != "":
        accumproj.accumulated_xray_dose.projection_xray_radiation_dose.general_study_module_attributes.modality_type = "DX"
    accumproj.save()


def _accumulatedcassettebasedprojectionradiographydose(dataset,accum): # TID 10006
    from remapp.models import AccumCassetteBsdProjRadiogDose
    from remapp.tools.get_values import get_or_create_cid
    accumcass = AccumCassetteBsdProjRadiogDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Detector Type':
            accumcass.detector_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
            accumcass.total_number_of_radiographic_frames = cont.MeasuredValueSequence[0].NumericValue
    accumcass.save()

def _accumulatedintegratedprojectionradiographydose(dataset,accum): # TID 10007
    from remapp.models import AccumIntegratedProjRadiogDose
    from remapp.tools.get_values import get_or_create_cid
    accumint = AccumIntegratedProjRadiogDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product Total':
            accumint.dose_area_product_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP) Total':
            accumint.dose_rp_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
            accumint.total_number_of_radiographic_frames = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
            accumint.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning) # will fail if text
    accumint.save()

def _accumulatedxraydose(dataset,proj): # TID 10002
    from remapp.models import AccumXRayDose, ContextID
    from remapp.tools.get_values import get_or_create_cid
    accum = AccumXRayDose.objects.create(projection_xray_radiation_dose=proj)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Plane':
            accum.acquisition_plane = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration':
                _calibration(cont,accum)
    _accumulatedprojectionxraydose(dataset,accum)
    if accum.projection_xray_radiation_dose.procedure_reported == 'P5-40010':
        _accumulatedmammoxraydose(dataset,accum)
    _accumulatedcassettebasedprojectionradiographydose(dataset,accum)
    _accumulatedintegratedprojectionradiographydose(dataset,accum)
    accum.save()

def _scanninglength(dataset,event): # TID 10014
    from remapp.models import ScanningLength
    scanlen = ScanningLength.objects.create(ct_irradiation_event_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'scanning length':
            scanlen.scanning_length = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'length of reconstructable volume':
            scanlen.length_of_reconstructable_volume = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'exposed range':
            scanlen.exposed_range = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'top z location of reconstructable volume':
            scanlen.top_z_location_of_reconstructable_volume = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'bottom z location of reconstructable volume':
            scanlen.bottom_z_location_of_reconstructable_volume = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'top z location of scanning length':
            scanlen.top_z_location_of_scanning_length = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'bottom z location of scanning length':
            scanlen.bottom_z_location_of_scanning_length = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'irradiation event uid':
            scanlen.irradiation_event_uid = cont.UID
    scanlen.save()

def _ctxraysourceparameters(dataset,event):
    from remapp.models import CtXRaySourceParameters
    param = CtXRaySourceParameters.objects.create(ct_irradiation_event_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'identification of the x-ray source' or cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'identification number of the x-ray source':
            param.identification_of_the_xray_source = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'KVP':
            param.kvp = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'maximum x-ray tube current':
            param.maximum_xray_tube_current = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray tube current':
            param.xray_tube_current = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time per Rotation':
            param.exposure_time_per_rotation = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray filter aluminum equivalent':
            param.xray_filter_aluminum_equivalent = cont.MeasuredValueSequence[0].NumericValue
    param.save()


def _ctirradiationeventdata(dataset,ct): # TID 10013
    from remapp.models import CtIrradiationEventData
    from remapp.tools.get_values import get_or_create_cid
    event = CtIrradiationEventData.objects.create(ct_radiation_dose=ct)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Protocol':
            event.acquisition_protocol = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'TargetRegion':
            event.target_region = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Type':
            event.ct_acquisition_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'ProcedureContext':
            event.procedure_context = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event UID':
            event.irradiation_event_uid = cont.UID
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                _scanninglength(cont,event)
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time':
                        event.exposure_time = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Nominal Single Collimation Width':
                        event.nominal_single_collimation_width = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Nominal Total Collimation Width':
                        event.nominal_total_collimation_width = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Pitch Factor':
                        event.pitch_factor = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'number of x-ray sources':
                        event.number_of_xray_sources = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ValueType == 'CONTAINER':
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'ct x-ray source parameters':
                            _ctxraysourceparameters(cont2,event)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose':
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIvol':
                        event.mean_ctdivol = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIw Phantom Type':
                        event.ctdiw_phantom_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIfreeair Calculation Factor':
                        event.ctdifreeair_calculation_factor = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIfreeair':
                        event.mean_ctdifreeair = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'DLP':
                        event.dlp = cont2.MeasuredValueSequence[0].NumericValue
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Effective Dose':
                        event.effective_dose = cont2.MeasuredValueSequence[0].NumericValue
                    ## Effective dose measurement method and conversion factor
                    ## CT Dose Check details here
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray modulation type':
            event.xray_modulation_type = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            event.comment = cont.TextValue
    if not event.xray_modulation_type and event.comment:
        comments = event.comment.split(",")
        for comm in comments:
            if comm.lstrip().startswith("X-ray Modulation Type"):
                modulationtype = comm[(comm.find('=')+2):]
                event.xray_modulation_type = modulationtype
        
    ## personparticipant here
    _deviceparticipant(dataset,'ct_event',event)
    event.save()
                        

def _ctaccumulateddosedata(dataset,ct): # TID 10012
    from remapp.models import CtAccumulatedDoseData, ContextID
    ctacc = CtAccumulatedDoseData.objects.create(ct_radiation_dose=ct)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Irradiation Events':
            ctacc.total_number_of_irradiation_events = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose Length Product Total':
            ctacc.ct_dose_length_product_total = cont.MeasuredValueSequence[0].NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Effective Dose Total':
            ctacc.ct_effective_dose_total = cont.MeasuredValueSequence[0].NumericValue
        #
        # Reference authority code or name belongs here, followed by the effective dose details
        #
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            ctacc.comment = cont.TextValue
    _deviceparticipant(dataset,'ct_accumulated',ctacc)

    ctacc.save()


def _projectionxrayradiationdose(dataset,g,reporttype):
    from remapp.models import ProjectionXRayRadiationDose, CtRadiationDose, ObserverContext
    from remapp.tools.get_values import get_or_create_cid
    from remapp.tools.dcmdatetime import make_date_time
    if reporttype == 'projection':
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
    elif reporttype == 'ct':
        proj = CtRadiationDose.objects.create(general_study_module_attributes=g)
    else: pass
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Procedure reported':
            proj.procedure_reported = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
            if ('ContentSequence' in cont): # Extra if statement to allow for non-conformant GE RDSR that don't have this mandatory field.
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Has Intent':
                        proj.has_intent = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'start of x-ray irradiation':
            proj.start_of_xray_irradiation = make_date_time(cont.DateTime)
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'end of x-ray irradiation':
            proj.end_of_xray_irradiation = make_date_time(cont.DateTime) 
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Scope of Accumulation':
            proj.scope_of_accumulation = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            proj.comment = cont.TextValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Source of Dose Information':
            proj.source_of_dose_information = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        proj.save()
        
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Observer Type':
            if reporttype == 'projection':
                obs = ObserverContext.objects.create(projection_xray_radiation_dose=proj)
            elif reporttype == 'ct':
                obs = ObserverContext.objects.create(ct_radiation_dose=proj)
            _observercontext(dataset,obs)

        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated X-Ray Dose Data':
                proj.general_study_module_attributes.modality_type = 'RF,DX'
                _accumulatedxraydose(cont,proj)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event X-Ray Data':
                _irradiationeventxraydata(cont,proj)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Accumulated Dose Data':
                proj.general_study_module_attributes.modality_type = 'CT'
                _ctaccumulateddosedata(cont,proj)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition':
                _ctirradiationeventdata(cont,proj)

def _generalequipmentmoduleattributes(dataset,study):
    from remapp.models import GeneralEquipmentModuleAttr, UniqueEquipmentNames
    from remapp.tools.dcmdatetime import get_date, get_time
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.hash_id import hash_id
    equip = GeneralEquipmentModuleAttr.objects.create(general_study_module_attributes=study)
    equip.manufacturer = get_value_kw("Manufacturer",dataset)
    equip.institution_name = get_value_kw("InstitutionName",dataset)
    equip.institution_address = get_value_kw("InstitutionAddress",dataset)
    equip.station_name = get_value_kw("StationName",dataset)
    equip.institutional_department_name = get_value_kw("InstitutionalDepartmentName",dataset)
    equip.manufacturer_model_name = get_value_kw("ManufacturerModelName",dataset)
    equip.device_serial_number = get_value_kw("DeviceSerialNumber",dataset)
    equip.software_versions = get_value_kw("SoftwareVersions",dataset)
    equip.gantry_id = get_value_kw("GantryID",dataset)
    equip.spatial_resolution = get_value_kw("SpatialResolution",dataset)
    equip.date_of_last_calibration = get_date("DateOfLastCalibration",dataset)
    equip.time_of_last_calibration = get_time("TimeOfLastCalibration",dataset)

    equip_display_name, created = UniqueEquipmentNames.objects.get_or_create(manufacturer=equip.manufacturer,
                                                                             manufacturer_hash=hash_id(equip.manufacturer),
                                                                             institution_name=equip.institution_name,
                                                                             institution_name_hash = hash_id(equip.institution_name),
                                                                             station_name=equip.station_name,
                                                                             station_name_hash=hash_id(equip.station_name),
                                                                             institutional_department_name=equip.institutional_department_name,
                                                                             institutional_department_name_hash=hash_id(equip.institutional_department_name),
                                                                             manufacturer_model_name=equip.manufacturer_model_name,
                                                                             manufacturer_model_name_hash=hash_id(equip.manufacturer_model_name),
                                                                             device_serial_number=equip.device_serial_number,
                                                                             device_serial_number_hash=hash_id(equip.device_serial_number),
                                                                             software_versions=equip.software_versions,
                                                                             software_versions_hash=hash_id(equip.software_versions),
                                                                             gantry_id=equip.gantry_id,
                                                                             gantry_id_hash=hash_id(equip.gantry_id),
                                                                             hash_generated=True
                                                                             )
    if created:
        if equip.institution_name and equip.station_name:
            equip_display_name.display_name = equip.institution_name + ' ' + equip.station_name
        elif equip.institution_name:
            equip_display_name.display_name = equip.institution_name
        elif equip.station_name:
            equip_display_name.display_name = equip.station_name
        else:
            equip_display_name.display_name = 'Blank'
        equip_display_name.save()

    equip.unique_equipment_name = UniqueEquipmentNames(pk=equip_display_name.pk)

    equip.save()

def _patientstudymoduleattributes(dataset,g): # C.7.2.2
    from remapp.models import PatientStudyModuleAttr
    from remapp.tools.get_values import get_value_kw
    patientatt = PatientStudyModuleAttr.objects.create(general_study_module_attributes=g)
    patientatt.patient_age = get_value_kw("PatientAge",dataset)
    patientatt.patient_weight = get_value_kw("PatientWeight",dataset)
    patientatt.patient_size = get_value_kw("PatientSize", dataset)
    patientatt.save()

def _patientmoduleattributes(dataset,g): # C.7.1.1
    from decimal import Decimal
    import hashlib
    from remapp.models import PatientModuleAttr, PatientStudyModuleAttr
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import get_date
    from remapp.tools.not_patient_indicators import get_not_pt
    from remapp.models import PatientIDSettings

    pat = PatientModuleAttr.objects.create(general_study_module_attributes=g)

    patient_birth_date = get_date("PatientBirthDate",dataset)
    pat.patient_sex = get_value_kw("PatientSex",dataset)
    pat.not_patient_indicator = get_not_pt(dataset)
    patientatt = PatientStudyModuleAttr.objects.get(general_study_module_attributes=g)
    if patient_birth_date:
        patientatt.patient_age_decimal = Decimal((g.study_date.date() - patient_birth_date.date()).days)/Decimal('365.25')
    elif patientatt.patient_age:
        if patientatt.patient_age[-1:]=='Y':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1])
        elif patientatt.patient_age[-1:]=='M':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1])/Decimal('12')
        elif patientatt.patient_age[-1:]=='D':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1])/Decimal('365.25') 
    if patientatt.patient_age_decimal:
        patientatt.patient_age_decimal = patientatt.patient_age_decimal.quantize(Decimal('.1'))
    patientatt.save()

    patient_id_settings = PatientIDSettings.objects.get()
    if patient_id_settings.name_stored:
        name = get_value_kw("PatientName", dataset)
        if name and patient_id_settings.name_hashed:
            name = hashlib.sha256(name).hexdigest()
            pat.name_hashed = True
        pat.patient_name = name
    if patient_id_settings.id_stored:
        patid = get_value_kw("PatientID", dataset)
        if patid and patient_id_settings.id_hashed:
            patid = hashlib.sha256(patid).hexdigest()
            pat.id_hashed = True
        pat.patient_id = patid
    if patient_id_settings.dob_stored and patient_birth_date:
        pat.patient_birth_date = patient_birth_date
    pat.save()

def _generalstudymoduleattributes(dataset,g):
    from datetime import datetime
    from remapp.models import PatientIDSettings
    from remapp.tools.get_values import get_value_kw, get_seq_code_value, get_seq_code_meaning
    from remapp.tools.dcmdatetime import get_date, get_time
    from remapp.tools.hash_id import hash_id

    g.study_instance_uid = get_value_kw('StudyInstanceUID',dataset)
    g.study_date = get_date('StudyDate',dataset)
    g.study_time = get_time('StudyTime',dataset)
    g.study_workload_chart_time = datetime.combine(datetime.date(datetime(1900,1,1)), datetime.time(g.study_time))
    g.referring_physician_name = get_value_kw('ReferringPhysicianName',dataset)
    g.referring_physician_identification = get_value_kw('ReferringPhysicianIdentification',dataset)
    g.study_id = get_value_kw('StudyID',dataset)
    accession_number = get_value_kw('AccessionNumber',dataset)
    patient_id_settings = PatientIDSettings.objects.get()
    if accession_number and patient_id_settings.accession_hashed:
        accession_number = hash_id(accession_number)
        g.accession_hashed = True
    g.accession_number = accession_number
    g.study_description = get_value_kw('StudyDescription',dataset)
    g.physician_of_record = get_value_kw('PhysicianOfRecord',dataset)
    g.name_of_physician_reading_study = get_value_kw('NameOfPhysicianReadingStudy',dataset)
    g.performing_physician_name = get_value_kw('PerformingPhysicianName',dataset)
    g.operator_name = get_value_kw('OperatorsName',dataset)
    g.procedure_code_value = get_seq_code_value('ProcedureCodeSequence',dataset)
    g.procedure_code_meaning = get_seq_code_meaning('ProcedureCodeSequence',dataset)
    g.requested_procedure_code_value = get_seq_code_value('RequestedProcedureCodeSequence',dataset)
    g.requested_procedure_code_meaning = get_seq_code_meaning('RequestedProcedureCodeSequence',dataset)
    if dataset.ContentTemplateSequence[0].TemplateIdentifier == '10001':
        _projectionxrayradiationdose(dataset,g,'projection')
    elif dataset.ContentTemplateSequence[0].TemplateIdentifier == '10011':
        _projectionxrayradiationdose(dataset,g,'ct')
    g.save()
    if not g.requested_procedure_code_meaning:
        if (('RequestAttributesSequence' in dataset) and dataset[0x40,0x275].VM): # Ulgy hack to prevent issues with zero length LS16 sequence
            req = dataset.RequestAttributesSequence
            g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription',req[0])
            if not g.requested_procedure_code_meaning: # Sometimes the above is true, but there is no RequestedProcedureDescription in that sequence, but there is a basic field as below.
                g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription',dataset)
            g.save()
        else:
            g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription',dataset)
            g.save()
        

def _rsdr2db(dataset):
    import os, sys
    import openrem_settings

    os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.openremproject.settings'
    from django.db import models

    openrem_settings.add_project_to_path()
    from remapp.models import GeneralStudyModuleAttr

    if 'StudyInstanceUID' in dataset:
        uid = dataset.StudyInstanceUID
        existing = GeneralStudyModuleAttr.objects.filter(study_instance_uid__exact = uid)
        if existing:
            return

    g = GeneralStudyModuleAttr.objects.create()
    _generalstudymoduleattributes(dataset,g)
    _generalequipmentmoduleattributes(dataset,g)
    _patientstudymoduleattributes(dataset,g)
    _patientmoduleattributes(dataset,g)


@shared_task
def rdsr(rdsr_file):
    """Extract radiation dose related data from DICOM Radiation SR objects.

    :param filename: relative or absolute path to Radiation Dose Structured Report.
    :type filename: str.
    
    Tested with:
        * CT: Siemens, Philips and GE RDSR, GE Enhanced SR.
        * Fluoro: Siemens Artis Zee RDSR
    """

    import dicom
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.models import DicomDeleteSettings
    try:
        del_settings = DicomDeleteSettings.objects.get()
        del_rdsr = del_settings.del_rdsr
    except ObjectDoesNotExist:
        del_rdsr = False


    dataset = dicom.read_file(rdsr_file)

    if dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.22':
        # print '{0}{1}'.format(rdsr_file," is not an RDSR, but it is an enhanced structured report, so we'll attempt to use it")
        pass
    elif dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.88.67':
        return ('{0}{1}'.format(rdsr_file," is not a Radiation Dose Structured Report"))
    elif dataset.ConceptNameCodeSequence[0].CodeValue != '113701':
        return ('{0}{1}'.format(rdsr_file," doesn't seem to have a report in it :-("))

    _rsdr2db(dataset)

    if del_rdsr:
        os.remove(rdsr_file)

    return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit('Error: Supply exactly one argument - the DICOM RDSR file')

    sys.exit(rdsr(sys.argv[1]))
