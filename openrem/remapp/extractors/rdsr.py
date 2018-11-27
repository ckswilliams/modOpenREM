# This Python file uses the following encoding: utf-8
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

import logging
import os
import sys

import django

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from celery import shared_task
from remapp.tools.get_values import test_numeric_value

logger = logging.getLogger('remapp.extractors.rdsr')  # Explicitly named so that it is still handled when using __main__


def _observercontext(dataset, obs, ch):  # TID 1002
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Observer Type':
            obs.observer_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                  cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer UID':
            obs.device_observer_uid = cont.UID
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Name':
            obs.device_observer_name = safe_strings(cont.TextValue, ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Manufacturer':
            obs.device_observer_manufacturer = safe_strings(cont.TextValue, ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Model Name':
            obs.device_observer_model_name = safe_strings(cont.TextValue, ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Serial Number':
            obs.device_observer_serial_number = safe_strings(cont.TextValue, ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer Physical Location during observation':
            obs.device_observer_physical_location_during_observation = safe_strings(cont.TextValue, ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Role in Procedure':
            obs.device_role_in_procedure = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                             cont.ConceptCodeSequence[0].CodeMeaning)
    obs.save()


def _person_participant(dataset, event_data_type, foreign_key):
    """Function to record people involved with study

    :param dataset: DICOM data being parsed
    :param event_data_type: Which function has called this function
    :param foreign_key: object of model this modal will link to
    :return: None
    """
    from remapp.models import PersonParticipant
    from remapp.tools.get_values import get_or_create_cid
    if event_data_type == 'ct_dose_check_alert':
        person = PersonParticipant.objects.create(ct_dose_check_details_alert=foreign_key)
    elif event_data_type == 'ct_dose_check_notification':
        person = PersonParticipant.objects.create(ct_dose_check_details_notification=foreign_key)
    else:
        return
    person.person_name = dataset.PersonName
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person Role in Procedure':
            person.person_role_in_procedure_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person ID':
            person.person_id = cont.TextValue
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person ID Issue':
            person.person_id_issuer = cont.TextValue
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Organization Name':
            person.organization_name = cont.TextValue
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person Role in Organization':
            person.person_role_in_organization_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
    person.save()


def _deviceparticipant(dataset, eventdatatype, foreignkey, ch):
    from remapp.models import DeviceParticipant
    from remapp.tools.get_values import get_or_create_cid, safe_strings
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
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Device Role in Procedure':
            device.device_role_in_procedure = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                cont.ConceptCodeSequence[0].CodeMeaning)
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Name':
                    device.device_name = safe_strings(cont2.TextValue, char_set=ch)
                elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Manufacturer':
                    device.device_manufacturer = safe_strings(cont2.TextValue, char_set=ch)
                elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Model Name':
                    device.device_model_name = safe_strings(cont2.TextValue, char_set=ch)
                elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Serial Number':
                    device.device_serial_number = safe_strings(cont2.TextValue, char_set=ch)
                elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Device Observer UID':
                    device.device_observer_uid = cont2.UID
    device.save()


def _pulsewidth(pulse_width_value, source):
    """Takes pulse width values and populates PulseWidth table

    :param pulse_width_value: Decimal or list of decimals
    :param source: database object in IrradEventXRaySourceData table
    :return: None
    """
    from remapp.models import PulseWidth
    try:
        pulse = PulseWidth.objects.create(irradiation_event_xray_source_data=source)
        pulse.pulse_width = pulse_width_value
        pulse.save()
    except ValueError:
        if not hasattr(pulse_width_value, "strip") and (
                hasattr(pulse_width_value, "__getitem__") or hasattr(pulse_width_value, "__iter__")):
            for per_pulse_pulse_width in pulse_width_value:
                pulse = PulseWidth.objects.create(irradiation_event_xray_source_data=source)
                pulse.pulse_width = per_pulse_pulse_width
                pulse.save()


def _kvptable(kvp_value, source):
    """Takes kVp values and populates kvp table

    :param kvp_value: Decimal or list of decimals
    :param source: database object in IrradEventXRaySourceData table
    :return: None
    """
    from remapp.models import Kvp
    try:
        kvpdata = Kvp.objects.create(irradiation_event_xray_source_data=source)
        kvpdata.kvp = kvp_value
        kvpdata.save()
    except ValueError:
        if not hasattr(kvp_value, "strip") and (
                hasattr(kvp_value, "__getitem__") or hasattr(kvp_value, "__iter__")):
            for per_pulse_kvp in kvp_value:
                kvp = Kvp.objects.create(irradiation_event_xray_source_data=source)
                kvp.kvp = per_pulse_kvp
                kvp.save()


def _xraytubecurrent(current_value, source):
    """Takes X-ray tube current values and populates XrayTubeCurrent table

    :param current_value: Decimal or list of decimals
    :param source: database object in IrradEventXRaySourceData table
    :return: None
    """
    from remapp.models import XrayTubeCurrent
    try:
        tubecurrent = XrayTubeCurrent.objects.create(irradiation_event_xray_source_data=source)
        tubecurrent.xray_tube_current = current_value
        tubecurrent.save()
    except ValueError:
        if not hasattr(current_value, "strip") and (
                hasattr(current_value, "__getitem__") or hasattr(current_value, "__iter__")):
            for per_pulse_current in current_value:
                tubecurrent = XrayTubeCurrent.objects.create(irradiation_event_xray_source_data=source)
                tubecurrent.xray_tube_current = per_pulse_current
                tubecurrent.save()


def _exposure(exposure_value, source):
    """Takes exposure (mAs) values and populates Exposure table

    :param exposure_value: Decimal or list of decimals
    :param source: database object in IrradEventXRaySourceData table
    :return: None
    """
    from remapp.models import Exposure
    try:
        exposure = Exposure.objects.create(irradiation_event_xray_source_data=source)
        exposure.exposure = exposure_value
        exposure.save()
    except ValueError:
        if not hasattr(exposure_value, "strip") and (
                hasattr(exposure_value, "__getitem__") or hasattr(exposure_value, "__iter__")):
            for per_pulse_exposure in exposure_value:
                exposure = Exposure.objects.create(irradiation_event_xray_source_data=source)
                exposure.exposure = per_pulse_exposure
                exposure.save()


def _xrayfilters(content_sequence, source):
    from remapp.models import XrayFilters
    from remapp.tools.get_values import get_or_create_cid
    filters = XrayFilters.objects.create(irradiation_event_xray_source_data=source)
    for cont2 in content_sequence:
        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Type':
            filters.xray_filter_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                         cont2.ConceptCodeSequence[0].CodeMeaning)
        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Material':
            filters.xray_filter_material = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                             cont2.ConceptCodeSequence[0].CodeMeaning)
        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Thickness Minimum':
            filters.xray_filter_thickness_minimum = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filter Thickness Maximum':
            filters.xray_filter_thickness_maximum = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
    filters.save()


def _doserelateddistancemeasurements(dataset, mech):  # CID 10008
    from remapp.models import DoseRelatedDistanceMeasurements
    distance = DoseRelatedDistanceMeasurements.objects.create(irradiation_event_xray_mechanical_data=mech)
    codes = {'Distance Source to Isocenter': 'distance_source_to_isocenter',
             'Distance Source to Reference Point': 'distance_source_to_reference_point',
             'Distance Source to Detector': 'distance_source_to_detector',
             'Table Longitudinal Position': 'table_longitudinal_position',
             'Table Lateral Position': 'table_lateral_position',
             'Table Height Position': 'table_height_position',
             'Distance Source to Table Plane': 'distance_source_to_table_plane'}
    # For Philips Allura XPer systems you get the privately defined 'Table Height Position' with CodingSchemeDesignator
    # '99PHI-IXR-XPER' instead of the DICOM defined 'Table Height Position'.
    # It seems they are defined the same
    for cont in dataset.ContentSequence:
        try:
            setattr(distance, codes[cont.ConceptNameCodeSequence[0].CodeMeaning],
                    cont.MeasuredValueSequence[0].NumericValue)
        except KeyError:
            pass
    distance.save()


def _irradiationeventxraymechanicaldata(dataset, event):  # TID 10003c
    from remapp.models import IrradEventXRayMechanicalData
    from remapp.tools.get_values import get_or_create_cid
    mech = IrradEventXRayMechanicalData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CR/DR Mechanical Configuration':
            mech.crdr_mechanical_configuration = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                   cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Primary Angle':
            mech.positioner_primary_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Secondary Angle':
            mech.positioner_secondary_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Primary End Angle':
            mech.positioner_primary_end_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Positioner Secondary End Angle':
            mech.positioner_secondary_end_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Column Angulation':
            mech.column_angulation = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Head Tilt Angle':
            mech.table_head_tilt_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Horizontal Rotation Angle':
            mech.table_horizontal_rotation_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Table Cradle Tilt Angle':
            mech.table_cradle_tilt_angle = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Compression Thickness':
            mech.compression_thickness = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
    _doserelateddistancemeasurements(dataset, mech)
    mech.save()


def _irradiationeventxraysourcedata(dataset, event, ch):  # TID 10003b
    # TODO: review model to convert to cid where appropriate, and add additional fields
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import Avg
    from remapp.models import IrradEventXRaySourceData
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    from xml.etree import ElementTree as ET
    # Variables below are used if privately defined parameters are available
    private_collimated_field_height = None
    private_collimated_field_width = None
    private_collimated_field_area = None

    source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        try:
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP)':
                source.dose_rp = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
                try:
                    source.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                               cont.ConceptCodeSequence[0].CodeMeaning)
                except AttributeError:
                    source.reference_point_definition = safe_strings(cont.TextValue, char_set=ch)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Average Glandular Dose':
                source.average_glandular_dose = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Mode':
                source.fluoro_mode = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                       cont.ConceptCodeSequence[0].CodeMeaning)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Pulse Rate':
                source.pulse_rate = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Number of Pulses':
                source.number_of_pulses = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif ((cont.ConceptNameCodeSequence[0].CodeMeaning == 'Number of Frames') and
                  (cont.ConceptNameCodeSequence[0].CodingSchemeDesignator == '99PHI-IXR-XPER')):
                # Philips Allura XPer systems: Private coding scheme designator: 99PHI-IXR-XPER; [number of pulses]
                source.number_of_pulses = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
                # should be a derivation thing in here for when the no. pulses is estimated
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Duration':
                source.irradiation_duration = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Average X-Ray Tube Current':
                source.average_xray_tube_current = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time':
                source.exposure_time = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Focal Spot Size':
                source.focal_spot_size = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Anode Target Material':
                source.anode_target_material = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                 cont.ConceptCodeSequence[0].CodeMeaning)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Collimated Field Area':
                source.collimated_field_area = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            # TODO: xray_grid no longer exists in this table - it is a model on its own...
            # See https://bitbucket.org/openrem/openrem/issue/181
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Grid':
                source.xray_grid = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                     cont.ConceptCodeSequence[0].CodeMeaning)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Pulse Width':
                _pulsewidth(cont.MeasuredValueSequence[0].NumericValue, source)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'KVP':
                _kvptable(cont.MeasuredValueSequence[0].NumericValue, source)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Tube Current':
                _xraytubecurrent(cont.MeasuredValueSequence[0].NumericValue, source)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure':
                _exposure(cont.MeasuredValueSequence[0].NumericValue, source)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Filters':
                _xrayfilters(cont.ContentSequence, source)
            # Maybe we have a Philips Xper system and we can use the privately defined information
            elif (cont.ConceptNameCodeSequence[0].CodeMeaning == 'Wedges and Shutters') and \
                    (cont.ConceptNameCodeSequence[0].CodingSchemeDesignator == '99PHI-IXR-XPER'):
                # According to DICOM Conformance statement:
                # http://incenter.medical.philips.com/doclib/enc/fetch/2000/4504/577242/577256/588723/5144873/5144488/
                # 5144772/DICOM_Conformance_Allura_8.2.pdf%3fnodeid%3d10125540%26vernum%3d-2
                # "Actual shutter distance from centerpoint of collimator specified in the plane at 1 meter.
                # Unit: mm. End of run value is used."
                bottom_shutter_pos = None
                left_shutter_pos = None
                right_shutter_pos = None
                top_shutter_pos = None
                try:
                    for cont2 in cont.ContentSequence:
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Bottom Shutter':
                            bottom_shutter_pos = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Left Shutter':
                            left_shutter_pos = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Right Shutter':
                            right_shutter_pos = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Top Shutter':
                            top_shutter_pos = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                    # Get distance_source_to_detector (Sdd) in meters
                    # Philips Allura XPer only notes distance_source_to_detector if it changed
                    try:
                        Sdd = float(event.irradeventxraymechanicaldata_set.get().
                                    doserelateddistancemeasurements_set.get().distance_source_to_detector) / 1000
                    except (ObjectDoesNotExist, TypeError):
                        Sdd = None
                    if bottom_shutter_pos and left_shutter_pos and right_shutter_pos and top_shutter_pos \
                            and Sdd:
                        # calculate collimated field area, collimated Field Height and Collimated Field Width
                        # at image receptor (shutter positions are defined at 1 meter)
                        private_collimated_field_height = (right_shutter_pos + left_shutter_pos) * Sdd  # in mm
                        private_collimated_field_width = (bottom_shutter_pos + top_shutter_pos) * Sdd  # in mm
                        private_collimated_field_area = (private_collimated_field_height *
                                                         private_collimated_field_width) / 1000000  # in m2
                except AttributeError:
                    pass
        except IndexError:
            pass
    _deviceparticipant(dataset, 'source', source, ch)
    try:
        source.ii_field_size = ET.fromstring(source.irradiation_event_xray_data.comment).find('iiDiameter').get(
            'SRData')
    except:
        pass
    if (not source.collimated_field_height) and private_collimated_field_height:
        source.collimated_field_height = private_collimated_field_height
    if (not source.collimated_field_width) and private_collimated_field_width:
        source.collimated_field_width = private_collimated_field_width
    if (not source.collimated_field_area) and private_collimated_field_area:
        source.collimated_field_area = private_collimated_field_area
    source.save()
    if not source.exposure_time and source.number_of_pulses:
        try:
            avg_pulse_width = source.pulsewidth_set.all().aggregate(Avg('pulse_width'))['pulse_width__avg']
            if avg_pulse_width:
                source.exposure_time = avg_pulse_width * source.number_of_pulses
                source.save()
        except ObjectDoesNotExist:
            pass
    if not source.average_xray_tube_current:
        if source.xraytubecurrent_set.all().count() > 0:
            source.average_xray_tube_current = source.xraytubecurrent_set.all().aggregate(
                Avg('xray_tube_current'))['xray_tube_current__avg']
            source.save()


def _irradiationeventxraydetectordata(dataset, event, ch):  # TID 10003a
    from remapp.models import IrradEventXRayDetectorData
    detector = IrradEventXRayDetectorData.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Index':
            detector.exposure_index = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Target Exposure Index':
            detector.target_exposure_index = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Deviation Index':
            detector.deviation_index = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
    _deviceparticipant(dataset, 'detector', detector, ch)
    detector.save()


def _imageviewmodifier(dataset, event):
    from remapp.models import ImageViewModifier
    from remapp.tools.get_values import get_or_create_cid
    modifier = ImageViewModifier.objects.create(irradiation_event_xray_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Image View Modifier':
            modifier.image_view_modifier = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
            # TODO: Projection Eponymous Name should be in here - needs db change
    modifier.save()


def _irradiationeventxraydata(dataset, proj, ch, fulldataset):  # TID 10003
    # TODO: review model to convert to cid where appropriate, and add additional fields
    from remapp.models import IrradEventXRayData
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    from remapp.tools.dcmdatetime import make_date_time
    from xml.etree import ElementTree as ET
    event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Plane':
            event.acquisition_plane = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event UID':
            event.irradiation_event_uid = cont.UID
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event Label':
            event.irradiation_event_label = safe_strings(cont.TextValue, char_set=ch)
            for cont2 in cont.ContentSequence:
                if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Label Type':
                    event.label_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                         cont2.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'DateTime Started':
            event.date_time_started = make_date_time(cont.DateTime)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event Type':
            event.irradiation_event_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                             cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Protocol':
            try:
                event.acquisition_protocol = safe_strings(cont.TextValue, char_set=ch)
            except AttributeError:
                event.acquisition_protocol = None
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Anatomical structure':
            event.anatomical_structure = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                           cont.ConceptCodeSequence[0].CodeMeaning)
            try:
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Laterality':
                        event.laterality = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                             cont2.ConceptCodeSequence[0].CodeMeaning)
            except AttributeError:
                pass
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Image View':
            event.image_view = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                 cont.ConceptCodeSequence[0].CodeMeaning)
            try:
                _imageviewmodifier(cont, event)
            except AttributeError:
                pass
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Table Relationship':
            event.patient_table_relationship_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Orientation':
            event.patient_orientation_cid = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
            try:
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Patient Orientation Modifier':
                        event.patient_orientation_modifier_cid = get_or_create_cid(
                            cont2.ConceptCodeSequence[0].CodeValue, cont2.ConceptCodeSequence[0].CodeMeaning)
            except AttributeError:
                pass
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Target Region':
            event.target_region = get_or_create_cid(
                cont.ConceptCodeSequence[0].CodeValue, cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product':
            event.dose_area_product = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Half Value Layer':
            event.half_value_layer = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Entrance Exposure at RP':
            event.entrance_exposure_at_rp = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
            try:
                event.reference_point_definition = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                     cont.ConceptCodeSequence[0].CodeMeaning)
            except AttributeError:
                event.reference_point_definition_text = safe_strings(cont.TextValue, char_set=ch)
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Mammography CAD Breast Composition':
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNamesCodes[0].CodeMeaning == 'Breast Composition':
                        event.breast_composition = cont2.CodeValue
                    elif cont2.ConceptNamesCodes[0].CodeMeaning == 'Percent Fibroglandular Tissue':
                        event.percent_fibroglandular_tissue = cont2.NumericValue
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            event.comment = safe_strings(cont.TextValue, char_set=ch)
    for cont3 in fulldataset.ContentSequence:
        if cont3.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            try:
                orientation = ET.fromstring(cont3.TextValue).find('PatientPosition').find('Position').get('SRData')
                if orientation.strip().lower() == 'hfs':
                    event.patient_table_relationship_cid = get_or_create_cid('F-10470', 'headfirst')
                    event.patient_orientation_cid = get_or_create_cid('F-10450', 'recumbent')
                    event.patient_orientation_modifier_cid = get_or_create_cid('F-10340', 'supine')
                elif orientation.strip().lower() == 'hfp':
                    event.patient_table_relationship_cid = get_or_create_cid('F-10470', 'headfirst')
                    event.patient_orientation_cid = get_or_create_cid('F-10450', 'recumbent')
                    event.patient_orientation_modifier_cid = get_or_create_cid('F-10310', 'prone')
                elif orientation.strip().lower() == 'ffs':
                    event.patient_table_relationship_cid = get_or_create_cid('F-10480', 'feet-first')
                    event.patient_orientation_cid = get_or_create_cid('F-10450', 'recumbent')
                    event.patient_orientation_modifier_cid = get_or_create_cid('F-10340', 'supine')
                elif orientation.strip().lower() == 'ffp':
                    event.patient_table_relationship_cid = get_or_create_cid('F-10480', 'feet-first')
                    event.patient_orientation_cid = get_or_create_cid('F-10450', 'recumbent')
                    event.patient_orientation_modifier_cid = get_or_create_cid('F-10310', 'prone')
                else:
                    event.patient_table_relationship_cid = None
                    event.patient_orientation_cid = None
                    event.patient_orientation_modifier_cid = None
            except:
                pass
            event.save()
    # needs include for optional multiple person participant
    _irradiationeventxraydetectordata(dataset, event, ch)
    _irradiationeventxraymechanicaldata(dataset, event)
    # in some cases we need mechanical data before x-ray source data
    _irradiationeventxraysourcedata(dataset, event, ch)

    event.save()


def _calibration(dataset, accum, ch):
    from remapp.models import Calibration
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    from remapp.tools.dcmdatetime import make_date_time
    cal = Calibration.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Measurement Device':
            cal.dose_measurement_device = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                            cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Date':
            cal.calibration_date = make_date_time(cont.DateTime)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Factor':
            cal.calibration_factor = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Uncertainty':
            cal.calibration_uncertainty = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration Responsible Party':
            cal.calibration_responsible_party = safe_strings(cont.TextValue, char_set=ch)
    cal.save()


def _accumulatedmammoxraydose(dataset, accum):  # TID 10005
    from remapp.models import AccumMammographyXRayDose
    from remapp.tools.get_values import get_or_create_cid
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated Average Glandular Dose':
            accummammo = AccumMammographyXRayDose.objects.create(accumulated_xray_dose=accum)
            accummammo.accumulated_average_glandular_dose = test_numeric_value(
                cont.MeasuredValueSequence[0].NumericValue)
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Laterality':
                    accummammo.laterality = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                              cont2.ConceptCodeSequence[0].CodeMeaning)
            accummammo.save()


def _accumulatedfluoroxraydose(dataset, accum):  # TID 10004
    # Name in DICOM standard for TID 10004 is Accumulated Fluoroscopy and Acquisition Projection X-Ray Dose
    from remapp.tools.get_values import get_or_create_cid
    from remapp.models import AccumProjXRayDose
    accumproj = AccumProjXRayDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        try:
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Dose Area Product Total':
                accumproj.fluoro_dose_area_product_total = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Fluoro Dose (RP) Total':
                accumproj.fluoro_dose_rp_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Fluoro Time':
                accumproj.total_fluoro_time = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Dose Area Product Total':
                accumproj.acquisition_dose_area_product_total = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Dose (RP) Total':
                accumproj.acquisition_dose_rp_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Acquisition Time':
                accumproj.total_acquisition_time = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            # TODO: Remove the following four items, as they are also imported (correctly) into
            # _accumulatedtotalprojectionradiographydose
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product Total':
                accumproj.dose_area_product_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP) Total':
                accumproj.dose_rp_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
                accumproj.total_number_of_radiographic_frames = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
                try:
                    accumproj.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                                  cont.ConceptCodeSequence[
                                                                                      0].CodeMeaning)
                except AttributeError:
                    accumproj.reference_point_definition = cont.TextValue
        except IndexError:
            pass
    if accumproj.accumulated_xray_dose.projection_xray_radiation_dose.general_study_module_attributes.modality_type == \
            'RF,DX':
        if accumproj.fluoro_dose_area_product_total or accumproj.total_fluoro_time:
            accumproj.accumulated_xray_dose.projection_xray_radiation_dose.general_study_module_attributes. \
                modality_type = 'RF'
        else:
            accumproj.accumulated_xray_dose.projection_xray_radiation_dose.general_study_module_attributes. \
                modality_type = "DX"
    accumproj.save()


def _accumulatedcassettebasedprojectionradiographydose(dataset, accum):  # TID 10006
    from remapp.models import AccumCassetteBsdProjRadiogDose
    from remapp.tools.get_values import get_or_create_cid
    accumcass = AccumCassetteBsdProjRadiogDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Detector Type':
            accumcass.detector_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
            accumcass.total_number_of_radiographic_frames = test_numeric_value(
                cont.MeasuredValueSequence[0].NumericValue)
    accumcass.save()


def _accumulatedtotalprojectionradiographydose(dataset, accum):  # TID 10007
    # Name in DICOM standard for TID 10007 is Accumulated Total Projection Radiography Dose
    from remapp.models import AccumIntegratedProjRadiogDose
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    accumint = AccumIntegratedProjRadiogDose.objects.create(accumulated_xray_dose=accum)
    for cont in dataset.ContentSequence:
        try:
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Area Product Total':
                accumint.dose_area_product_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Dose (RP) Total':
                accumint.dose_rp_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Radiographic Frames':
                accumint.total_number_of_radiographic_frames = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reference Point Definition':
                try:
                    accumint.reference_point_definition_code = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                                 cont.ConceptCodeSequence[
                                                                                     0].CodeMeaning)
                except AttributeError:
                    accumint.reference_point_definition = safe_strings(cont.TextValue)
        except IndexError:
            pass
    accumint.save()


def _accumulatedxraydose(dataset, proj, ch):  # TID 10002
    from remapp.models import AccumXRayDose
    from remapp.tools.get_values import get_or_create_cid
    accum = AccumXRayDose.objects.create(projection_xray_radiation_dose=proj)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Plane':
            accum.acquisition_plane = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Calibration':
                _calibration(cont, accum, ch)
    if proj.acquisition_device_type_cid:
        if 'Fluoroscopy-Guided' in proj.acquisition_device_type_cid.code_meaning or u"Azurion" in \
                proj.general_study_module_attributes.generalequipmentmoduleattr_set.get().manufacturer_model_name:
            _accumulatedfluoroxraydose(dataset, accum)
    elif proj.procedure_reported and ('Projection X-Ray' in proj.procedure_reported.code_meaning):
        _accumulatedfluoroxraydose(dataset, accum)
    if proj.procedure_reported and (proj.procedure_reported.code_meaning == 'Mammography'):
        _accumulatedmammoxraydose(dataset, accum)
    if proj.acquisition_device_type_cid:
        if 'Integrated' in proj.acquisition_device_type_cid.code_meaning or \
                'Fluoroscopy-Guided' in proj.acquisition_device_type_cid.code_meaning:
            _accumulatedtotalprojectionradiographydose(dataset, accum)
    elif proj.procedure_reported and ('Projection X-Ray' in proj.procedure_reported.code_meaning):
        _accumulatedtotalprojectionradiographydose(dataset, accum)
    if proj.acquisition_device_type_cid:
        if 'Cassette-based' in proj.acquisition_device_type_cid.code_meaning:
            _accumulatedcassettebasedprojectionradiographydose(dataset, accum)
    accum.save()


def _scanninglength(dataset, event):  # TID 10014
    from remapp.models import ScanningLength
    scanlen = ScanningLength.objects.create(ct_irradiation_event_data=event)
    try:
        for cont in dataset.ContentSequence:
            if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'scanning length':
                scanlen.scanning_length = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'length of reconstructable volume':
                scanlen.length_of_reconstructable_volume = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'exposed range':
                scanlen.exposed_range = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'top z location of reconstructable volume':
                scanlen.top_z_location_of_reconstructable_volume = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'bottom z location of reconstructable volume':
                scanlen.bottom_z_location_of_reconstructable_volume = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'top z location of scanning length':
                scanlen.top_z_location_of_scanning_length = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'bottom z location of scanning length':
                scanlen.bottom_z_location_of_scanning_length = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'irradiation event uid':
                scanlen.irradiation_event_uid = cont.UID
        scanlen.save()
    except AttributeError:
        pass


def _ctxraysourceparameters(dataset, event):
    from remapp.models import CtXRaySourceParameters
    param = CtXRaySourceParameters.objects.create(ct_irradiation_event_data=event)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'identification of the x-ray source' or \
                cont.ConceptNameCodeSequence[
                    0].CodeMeaning.lower() == 'identification number of the x-ray source':
            param.identification_of_the_xray_source = cont.TextValue
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'KVP':
            param.kvp = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'maximum x-ray tube current':
            param.maximum_xray_tube_current = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray tube current':
            param.xray_tube_current = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeValue == '113734':
            # Additional check as code meaning is wrong for Siemens Intevo see
            # https://bitbucket.org/openrem/openrem/issues/380/siemens-intevo-rdsr-have-wrong-code
            param.xray_tube_current = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time per Rotation':
            param.exposure_time_per_rotation = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray filter aluminum equivalent':
            param.xray_filter_aluminum_equivalent = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
    param.save()


def _ctdosecheckdetails(dataset, dosecheckdetails, ch, isalertdetails):  # TID 10015
    # PARTLY TESTED CODE (no DSR available that has Reason For Proceeding and/or Forward Estimate)
    from remapp.tools.get_values import safe_strings

    if isalertdetails:
        for cont in dataset.ContentSequence:
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DLP Alert Value Configured':
                dosecheckdetails.dlp_alert_value_configured = (cont.ConceptCodeSequence[0].CodeMeaning == 'Yes')
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DLP Alert Value':
                dosecheckdetails.dlp_alert_value = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIvol Alert Value Configured':
                dosecheckdetails.ctdivol_alert_value_configured = (cont.ConceptCodeSequence[0].CodeMeaning == 'Yes')
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIvol Alert Value':
                dosecheckdetails.ctdivol_alert_value = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated DLP Forward Estimate':
                dosecheckdetails.accumulated_dlp_forward_estimate = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated CTDIvol Forward Estimate':
                dosecheckdetails.accumulated_ctdivol_forward_estimate = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reason For Proceeding':
                dosecheckdetails.alert_reason_for_proceeding = safe_strings(cont.TextValue, ch)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person Name':
                _person_participant(cont, 'ct_dose_check_alert', dosecheckdetails)
    else:
        for cont in dataset.ContentSequence:
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DLP Notification Value Configured':
                dosecheckdetails.dlp_notification_value_configured = (cont.ConceptCodeSequence[0].CodeMeaning == 'Yes')
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DLP Notification Value':
                dosecheckdetails.dlp_notification_value = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIvol Notification Value Configured':
                dosecheckdetails.ctdivol_notification_value_configured = (
                            cont.ConceptCodeSequence[0].CodeMeaning == 'Yes')
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIvol Notification Value':
                dosecheckdetails.ctdivol_notification_value = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'DLP Forward Estimate':
                dosecheckdetails.dlp_forward_estimate = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIvol Forward Estimate':
                dosecheckdetails.ctdivol_forward_estimate = test_numeric_value(
                    cont.MeasuredValueSequence[0].NumericValue)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Reason For Proceeding':
                dosecheckdetails.notification_reason_for_proceeding = safe_strings(cont.TextValue, ch)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Person Name':
                _person_participant(cont, 'ct_dose_check_notification', dosecheckdetails)
    dosecheckdetails.save()


def _ctirradiationeventdata(dataset, ct, ch):  # TID 10013
    from remapp.models import CtIrradiationEventData, CtDoseCheckDetails
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    event = CtIrradiationEventData.objects.create(ct_radiation_dose=ct)
    ctdosecheckdetails = None
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Acquisition Protocol':
            event.acquisition_protocol = safe_strings(cont.TextValue, char_set=ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Target Region':
            try:
                event.target_region = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
            except AttributeError:
                logger.info(u'Target Region ConceptNameCodeSequence exists, but no content. Study UID {0} from {1}, '
                            u'{2}, {3}'.format(
                    event.ct_radiation_dose.general_study_module_attributes.study_instance_uid,
                    event.ct_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(
                    ).manufacturer,
                    event.ct_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(
                    ).manufacturer_model_name,
                    event.ct_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.get(
                    ).station_name))
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Type':
            event.ct_acquisition_type = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                          cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Procedure Context':
            event.procedure_context = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event UID':
            event.irradiation_event_uid = cont.UID
            event.save()
        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition Parameters':
                _scanninglength(cont, event)
                try:
                    for cont2 in cont.ContentSequence:
                        if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Exposure Time':
                            event.exposure_time = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Nominal Single Collimation Width':
                            event.nominal_single_collimation_width = test_numeric_value(
                                cont2.MeasuredValueSequence[0].NumericValue)
                        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Nominal Total Collimation Width':
                            event.nominal_total_collimation_width = test_numeric_value(
                                cont2.MeasuredValueSequence[0].NumericValue)
                        elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Pitch Factor':
                            event.pitch_factor = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        elif cont2.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'number of x-ray sources':
                            event.number_of_xray_sources = test_numeric_value(
                                cont2.MeasuredValueSequence[0].NumericValue)
                        if cont2.ValueType == 'CONTAINER':
                            if cont2.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'ct x-ray source parameters':
                                _ctxraysourceparameters(cont2, event)
                except AttributeError:
                    pass
            elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose':
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIvol':
                        event.mean_ctdivol = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIw Phantom Type':
                        event.ctdiw_phantom_type = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                                     cont2.ConceptCodeSequence[0].CodeMeaning)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'CTDIfreeair Calculation Factor':
                        event.ctdifreeair_calculation_factor = test_numeric_value(
                            cont2.MeasuredValueSequence[0].NumericValue)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Mean CTDIfreeair':
                        event.mean_ctdifreeair = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'DLP':
                        event.dlp = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Effective Dose':
                        event.effective_dose = test_numeric_value(cont2.MeasuredValueSequence[0].NumericValue)
                        ## Effective dose measurement method and conversion factor
                    ## CT Dose Check Details
                    ## Dose Check Alert Details and Notifications Details can appear indepently
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Check Alert Details':
                        if ctdosecheckdetails is None:
                            ctdosecheckdetails = CtDoseCheckDetails.objects.create(ct_irradiation_event_data=event)
                        _ctdosecheckdetails(cont2, ctdosecheckdetails, ch, True)
                    elif cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Dose Check Notification Details':
                        if ctdosecheckdetails is None:
                            ctdosecheckdetails = CtDoseCheckDetails.objects.create(ct_irradiation_event_data=event)
                        _ctdosecheckdetails(cont2, ctdosecheckdetails, ch, False)
        if cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'x-ray modulation type':
            event.xray_modulation_type = safe_strings(cont.TextValue)
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            event.comment = safe_strings(cont.TextValue, char_set=ch)
    if not event.xray_modulation_type and event.comment:
        comments = event.comment.split(",")
        for comm in comments:
            if comm.lstrip().startswith("X-ray Modulation Type"):
                modulationtype = comm[(comm.find('=') + 2):]
                event.xray_modulation_type = modulationtype

    ## personparticipant here
    _deviceparticipant(dataset, 'ct_event', event, ch)
    if ctdosecheckdetails is not None:
        ctdosecheckdetails.save()
    event.save()


def _ctaccumulateddosedata(dataset, ct, ch):  # TID 10012
    from remapp.models import CtAccumulatedDoseData
    from remapp.tools.get_values import safe_strings
    ctacc = CtAccumulatedDoseData.objects.create(ct_radiation_dose=ct)
    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Total Number of Irradiation Events':
            ctacc.total_number_of_irradiation_events = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Dose Length Product Total':
            ctacc.ct_dose_length_product_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Effective Dose Total':
            ctacc.ct_effective_dose_total = test_numeric_value(cont.MeasuredValueSequence[0].NumericValue)
        #
        # Reference authority code or name belongs here, followed by the effective dose details
        #
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            ctacc.comment = safe_strings(cont.TextValue, char_set=ch)
    _deviceparticipant(dataset, 'ct_accumulated', ctacc, ch)

    ctacc.save()


def _projectionxrayradiationdose(dataset, g, reporttype, ch):
    from remapp.models import ProjectionXRayRadiationDose, CtRadiationDose, ObserverContext, GeneralEquipmentModuleAttr
    from remapp.tools.get_values import get_or_create_cid, safe_strings
    from remapp.tools.dcmdatetime import make_date_time
    if reporttype == 'projection':
        proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
    elif reporttype == 'ct':
        proj = CtRadiationDose.objects.create(general_study_module_attributes=g)
    else:
        logger.error("Attempt to create ProjectionXRayRadiationDose failed as report type incorrect")
        return
    equip = GeneralEquipmentModuleAttr.objects.get(general_study_module_attributes=g)
    proj.general_study_module_attributes.modality_type = equip.unique_equipment_name.user_defined_modality
    if proj.general_study_module_attributes.modality_type == u'dual':
        proj.general_study_module_attributes.modality_type = None

    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Procedure reported':
            proj.procedure_reported = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                        cont.ConceptCodeSequence[0].CodeMeaning)
            if (
                    'ContentSequence' in cont):  # Extra if statement to allow for non-conformant GE RDSR that don't have this mandatory field.
                for cont2 in cont.ContentSequence:
                    if cont2.ConceptNameCodeSequence[0].CodeMeaning == 'Has Intent':
                        proj.has_intent = get_or_create_cid(cont2.ConceptCodeSequence[0].CodeValue,
                                                            cont2.ConceptCodeSequence[0].CodeMeaning)
            if 'Mammography' in proj.procedure_reported.code_meaning:
                proj.general_study_module_attributes.modality_type = 'MG'
            elif (not proj.general_study_module_attributes.modality_type) and (
                    'Projection X-Ray' in proj.procedure_reported.code_meaning):
                proj.general_study_module_attributes.modality_type = 'RF,DX'
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'acquisition device type':
            proj.acquisition_device_type_cid = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                 cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'start of x-ray irradiation':
            proj.start_of_xray_irradiation = make_date_time(cont.DateTime)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning.lower() == 'end of x-ray irradiation':
            proj.end_of_xray_irradiation = make_date_time(cont.DateTime)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Scope of Accumulation':
            proj.scope_of_accumulation = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                           cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Detector Data Available':
            proj.xray_detector_data_available = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                  cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Source Data Available':
            proj.xray_source_data_available = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'X-Ray Mechanical Data Available':
            proj.xray_mechanical_data_available = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                    cont.ConceptCodeSequence[0].CodeMeaning)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Comment':
            proj.comment = safe_strings(cont.TextValue, char_set=ch)
        elif cont.ConceptNameCodeSequence[0].CodeMeaning == 'Source of Dose Information':
            proj.source_of_dose_information = get_or_create_cid(cont.ConceptCodeSequence[0].CodeValue,
                                                                cont.ConceptCodeSequence[0].CodeMeaning)
        if (not equip.unique_equipment_name.user_defined_modality) and (
                reporttype == 'projection') and proj.acquisition_device_type_cid:
            if 'Fluoroscopy-Guided' in proj.acquisition_device_type_cid.code_meaning or \
                    u"Azurion" in proj.general_study_module_attributes.generalequipmentmoduleattr_set.get(
                    ).manufacturer_model_name:
                proj.general_study_module_attributes.modality_type = 'RF'
            elif any(x in proj.acquisition_device_type_cid.code_meaning for x in ['Integrated', 'Cassette-based']):
                proj.general_study_module_attributes.modality_type = 'DX'
            else:
                logging.error(u"Acquisition device type code exists, but the value wasn't matched. Study UID: {0}, "
                              u"Station name: {1}, Study date, time: {2}, {3}, device type: {4} ".format(
                    proj.general_study_module_attributes.study_instance_uid,
                    proj.general_study_module_attributes.generalequipmentmoduleattr_set.get().station_name,
                    proj.general_study_module_attributes.study_date,
                    proj.general_study_module_attributes.study_time,
                    proj.acquisition_device_type_cid.code_meaning
                ))

        proj.save()

        if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Observer Type':
            if reporttype == 'projection':
                obs = ObserverContext.objects.create(projection_xray_radiation_dose=proj)
            else:
                obs = ObserverContext.objects.create(ct_radiation_dose=proj)
            _observercontext(dataset, obs, ch)

        if cont.ValueType == 'CONTAINER':
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Accumulated X-Ray Dose Data':
                _accumulatedxraydose(cont, proj, ch)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event X-Ray Data':
                _irradiationeventxraydata(cont, proj, ch, dataset)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Accumulated Dose Data':
                proj.general_study_module_attributes.modality_type = 'CT'
                _ctaccumulateddosedata(cont, proj, ch)
            if cont.ConceptNameCodeSequence[0].CodeMeaning == 'CT Acquisition':
                _ctirradiationeventdata(cont, proj, ch)


def _generalequipmentmoduleattributes(dataset, study, ch):
    from remapp.models import GeneralEquipmentModuleAttr, UniqueEquipmentNames
    from remapp.tools.dcmdatetime import get_date, get_time
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.hash_id import hash_id
    equip = GeneralEquipmentModuleAttr.objects.create(general_study_module_attributes=study)
    equip.manufacturer = get_value_kw("Manufacturer", dataset)
    equip.institution_name = get_value_kw("InstitutionName", dataset)
    equip.institution_address = get_value_kw("InstitutionAddress", dataset)
    equip.station_name = get_value_kw("StationName", dataset)
    equip.institutional_department_name = get_value_kw("InstitutionalDepartmentName", dataset)
    equip.manufacturer_model_name = get_value_kw("ManufacturerModelName", dataset)
    equip.device_serial_number = get_value_kw("DeviceSerialNumber", dataset)
    equip.software_versions = get_value_kw("SoftwareVersions", dataset)
    equip.gantry_id = get_value_kw("GantryID", dataset)
    equip.spatial_resolution = get_value_kw("SpatialResolution", dataset)
    equip.date_of_last_calibration = get_date("DateOfLastCalibration", dataset)
    equip.time_of_last_calibration = get_time("TimeOfLastCalibration", dataset)

    equip_display_name, created = UniqueEquipmentNames.objects.get_or_create(manufacturer=equip.manufacturer,
                                                                             manufacturer_hash=hash_id(
                                                                                 equip.manufacturer),
                                                                             institution_name=equip.institution_name,
                                                                             institution_name_hash=hash_id(
                                                                                 equip.institution_name),
                                                                             station_name=equip.station_name,
                                                                             station_name_hash=hash_id(
                                                                                 equip.station_name),
                                                                             institutional_department_name=equip.institutional_department_name,
                                                                             institutional_department_name_hash=hash_id(
                                                                                 equip.institutional_department_name),
                                                                             manufacturer_model_name=equip.manufacturer_model_name,
                                                                             manufacturer_model_name_hash=hash_id(
                                                                                 equip.manufacturer_model_name),
                                                                             device_serial_number=equip.device_serial_number,
                                                                             device_serial_number_hash=hash_id(
                                                                                 equip.device_serial_number),
                                                                             software_versions=equip.software_versions,
                                                                             software_versions_hash=hash_id(
                                                                                 equip.software_versions),
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
            equip_display_name.display_name = u'Blank'
        equip_display_name.save()

    equip.unique_equipment_name = UniqueEquipmentNames(pk=equip_display_name.pk)

    equip.save()


def _patientstudymoduleattributes(dataset, g):  # C.7.2.2
    from remapp.models import PatientStudyModuleAttr
    from remapp.tools.get_values import get_value_kw
    patientatt = PatientStudyModuleAttr.objects.create(general_study_module_attributes=g)
    patientatt.patient_age = get_value_kw("PatientAge", dataset)
    patientatt.patient_weight = get_value_kw("PatientWeight", dataset)
    patientatt.patient_size = get_value_kw("PatientSize", dataset)
    patientatt.save()


def _patientmoduleattributes(dataset, g, ch):  # C.7.1.1
    from decimal import Decimal
    from remapp.models import PatientModuleAttr, PatientStudyModuleAttr
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import get_date
    from remapp.tools.not_patient_indicators import get_not_pt
    from remapp.models import PatientIDSettings
    from remapp.tools.hash_id import hash_id

    pat = PatientModuleAttr.objects.create(general_study_module_attributes=g)

    patient_birth_date = get_date("PatientBirthDate", dataset)
    pat.patient_sex = get_value_kw("PatientSex", dataset)
    pat.not_patient_indicator = get_not_pt(dataset)
    patientatt = PatientStudyModuleAttr.objects.get(general_study_module_attributes=g)
    if patient_birth_date:
        patientatt.patient_age_decimal = Decimal((g.study_date.date() - patient_birth_date.date()).days) / Decimal(
            '365.25')
    elif patientatt.patient_age:
        if patientatt.patient_age[-1:] == 'Y':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1])
        elif patientatt.patient_age[-1:] == 'M':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1]) / Decimal('12')
        elif patientatt.patient_age[-1:] == 'D':
            patientatt.patient_age_decimal = Decimal(patientatt.patient_age[:-1]) / Decimal('365.25')
    if patientatt.patient_age_decimal:
        patientatt.patient_age_decimal = patientatt.patient_age_decimal.quantize(Decimal('.1'))
    patientatt.save()

    patient_id_settings = PatientIDSettings.objects.get()
    if patient_id_settings.name_stored:
        name = get_value_kw("PatientName", dataset)
        if name and patient_id_settings.name_hashed:
            name = hash_id(name)
            pat.name_hashed = True
        pat.patient_name = name
    if patient_id_settings.id_stored:
        patid = get_value_kw("PatientID", dataset)
        if patid and patient_id_settings.id_hashed:
            patid = hash_id(patid)
            pat.id_hashed = True
        pat.patient_id = patid
    if patient_id_settings.dob_stored and patient_birth_date:
        pat.patient_birth_date = patient_birth_date
    pat.save()


def _generalstudymoduleattributes(dataset, g, ch):
    from datetime import datetime
    from remapp.models import PatientIDSettings
    from remapp.tools.get_values import get_value_kw, get_seq_code_value, get_seq_code_meaning, list_to_string
    from remapp.tools.dcmdatetime import get_date, get_time, make_date, make_time
    from remapp.tools.hash_id import hash_id

    g.study_instance_uid = get_value_kw('StudyInstanceUID', dataset)
    g.series_instance_uid = get_value_kw('SeriesInstanceUID', dataset)
    g.study_date = get_date('StudyDate', dataset)
    if not g.study_date:
        g.study_date = get_date('ContentDate', dataset)
    if not g.study_date:
        g.study_date = get_date('SeriesDate', dataset)
    if not g.study_date:
        logger.error(u"Study UID {0} of modality {1} has no date information which is needed in the interface - "
                     u"date has been set to 1900!".format(
            g.study_instance_uid, get_value_kw("ManufacturerModelName", dataset)))
        g.study_date = make_date("19000101")
    g.study_time = get_time('StudyTime', dataset)
    g.series_time = get_time('SeriesTime', dataset)
    g.content_time = get_time('ContentTime', dataset)
    if not g.study_time:
        if g.content_time:
            g.study_time = g.content_time
        elif g.series_time:
            g.study_time = g.series_time
        else:
            logger.warning(u"Study UID {0} of modality {1} has no time information which is needed in the interface - "
                         u"time has been set to midnight.".format(
                g.study_instance_uid, get_value_kw("ManufacturerModelName", dataset)))
            g.study_time = make_time(000000)
    g.study_workload_chart_time = datetime.combine(datetime.date(datetime(1900, 1, 1)), datetime.time(g.study_time))
    g.referring_physician_name = list_to_string(get_value_kw('ReferringPhysicianName', dataset))
    g.referring_physician_identification = list_to_string(get_value_kw('ReferringPhysicianIdentification', dataset))
    g.study_id = get_value_kw('StudyID', dataset)
    accession_number = get_value_kw('AccessionNumber', dataset)
    patient_id_settings = PatientIDSettings.objects.get()
    if accession_number and patient_id_settings.accession_hashed:
        accession_number = hash_id(accession_number)
        g.accession_hashed = True
    g.accession_number = accession_number
    g.study_description = get_value_kw('StudyDescription', dataset)
    g.physician_of_record = list_to_string(get_value_kw('PhysicianOfRecord', dataset))
    g.name_of_physician_reading_study = list_to_string(get_value_kw('NameOfPhysiciansReadingStudy', dataset))
    g.performing_physician_name = list_to_string(get_value_kw('PerformingPhysicianName', dataset))
    g.operator_name = list_to_string(get_value_kw('OperatorsName', dataset))
    g.procedure_code_value = get_seq_code_value('ProcedureCodeSequence', dataset)
    g.procedure_code_meaning = get_seq_code_meaning('ProcedureCodeSequence', dataset)
    g.requested_procedure_code_value = get_seq_code_value('RequestedProcedureCodeSequence', dataset)
    g.requested_procedure_code_meaning = get_seq_code_meaning('RequestedProcedureCodeSequence', dataset)
    g.save()

    try:
        template_identifier = dataset.ContentTemplateSequence[0].TemplateIdentifier
    except AttributeError:
        logger.error(u"Study UID {0} of modality {1} has no template sequence - incomplete RDSR. Aborting.".format(
            g.study_instance_uid, get_value_kw("ManufacturerModelName", dataset)))
        g.delete()
        return
    if template_identifier == '10001':
        _projectionxrayradiationdose(dataset, g, 'projection', ch)
    elif template_identifier == '10011':
        _projectionxrayradiationdose(dataset, g, 'ct', ch)
    g.save()
    if not g.requested_procedure_code_meaning:
        if 'RequestAttributesSequence' in dataset and dataset[0x40, 0x275].VM:
            # Ugly hack to prevent issues with zero length LS16 sequence
            req = dataset.RequestAttributesSequence
            g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription', req[0])
            # Sometimes the above is true, but there is no RequestedProcedureDescription in that sequence, but
            # there is a basic field as below.
            if not g.requested_procedure_code_meaning:
                g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription', dataset)
            g.save()
        else:
            g.requested_procedure_code_meaning = get_value_kw('RequestedProcedureDescription', dataset)
            g.save()


def _rsdr2db(dataset):
    import openrem_settings

    os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.openremproject.settings'

    openrem_settings.add_project_to_path()
    from collections import OrderedDict
    from django.db.models import ObjectDoesNotExist
    from time import sleep
    from remapp.models import GeneralStudyModuleAttr, SkinDoseMapCalcSettings
    from remapp.tools.check_uid import record_sop_instance_uid
    from remapp.tools.get_values import get_value_kw

    existing_sop_instance_uids = set()
    keep_existing_sop_instance_uids = False
    if 'StudyInstanceUID' in dataset:
        study_uid = dataset.StudyInstanceUID
        existing_study_uid_match = GeneralStudyModuleAttr.objects.filter(study_instance_uid__exact=study_uid)
        if existing_study_uid_match:
            new_sop_instance_uid = dataset.SOPInstanceUID
            for existing_study in existing_study_uid_match.order_by('pk'):
                for processed_object in existing_study.objectuidsprocessed_set.all():
                    existing_sop_instance_uids.add(processed_object.sop_instance_uid)
            if new_sop_instance_uid in existing_sop_instance_uids:
                # We've dealt with this object before...
                logger.debug(u"Import match on Study Instance UID {0} and object SOP Instance UID {1}. "
                             u"Will not import.".format(study_uid, new_sop_instance_uid))
                return
            # Either we've not seen it before, or it wasn't recorded when we did.
            # Next find the event UIDs in the RDSR being imported
            new_event_uids = set()
            for content in dataset.ContentSequence:
                if content.ValueType and content.ValueType == 'CONTAINER':
                    if content.ConceptNameCodeSequence[0].CodeMeaning in (
                            'CT Acquisition', 'Irradiation Event X-Ray Data'):
                        for item in content.ContentSequence:
                            if item.ConceptNameCodeSequence[0].CodeMeaning == 'Irradiation Event UID':
                                new_event_uids.add(u"{0}".format(item.UID))
            logger.debug(u"Import match on StudyInstUID {0}. New RDSR event UIDs {1}".format(study_uid, new_event_uids))

            # Now check which event UIDs are in the database already
            existing_event_uids = OrderedDict()
            for i, existing_study in enumerate(existing_study_uid_match.order_by('pk')):
                existing_event_uids[i] = set()
                try:
                    for event in existing_study.ctradiationdose_set.get().ctirradiationeventdata_set.all():
                        existing_event_uids[i].add(event.irradiation_event_uid)
                except ObjectDoesNotExist:
                    for event in existing_study.projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
                        existing_event_uids[i].add(event.irradiation_event_uid)
            logger.debug(u"Import match on StudyInstUID {0}. Existing event UIDs {1}".format(
                study_uid, existing_event_uids))

            # Now compare the two
            for study_index, uid_list in existing_event_uids.items():
                if uid_list == new_event_uids:
                    # New RDSR is the same as the existing one
                    logger.debug(u"Import match on StudyInstUID {0}. Event level match, will not import.".format(
                        study_uid))
                    record_sop_instance_uid(existing_study_uid_match[study_index], new_sop_instance_uid)
                    return
                elif new_event_uids.issubset(uid_list):
                    # New RDSR has the same but fewer events than existing one
                    logger.debug(u"Import match on StudyInstUID {0}. New RDSR events are subset of existing events. "
                                 u"Will not import.".format(study_uid))
                    record_sop_instance_uid(existing_study_uid_match[study_index], new_sop_instance_uid)
                    return
                elif uid_list.issubset(new_event_uids):
                    # New RDSR has the existing events and more
                    # Check existing one had finished importing
                    try:
                        existing_study_uid_match[study_index].patientmoduleattr_set.get()
                        # probably had, so
                        existing_study_uid_match[study_index].delete()
                        keep_existing_sop_instance_uids = True
                        logger.debug(u"Import match on StudyInstUID {0}. Existing events are subset of new events. Will"
                                     u" import.".format(study_uid))
                    except ObjectDoesNotExist:
                        # Give existing one time to complete
                        sleep_time = 20.
                        logger.debug(u"Import match on StudyInstUID {0}. Existing events are subset of new events. "
                                     u"However, existing study appears not to have finished importing. Waiting {1} s"
                                     u"before trying again.".format(study_uid, sleep_time))
                        sleep(sleep_time)
                        existing_event_uids_post_delay = set()
                        try:
                            for event in existing_study_uid_match.order_by(
                                    'pk')[study_index].ctradiationdose_set.get().ctirradiationeventdata_set.all():
                                existing_event_uids_post_delay.add(event.irradiation_event_uid)
                        except ObjectDoesNotExist:
                            for event in existing_study_uid_match.order_by(
                                    'pk')[study_index].projectionxrayradiationdose_set.get(
                            ).irradeventxraydata_set.all():
                                existing_event_uids_post_delay.add(event.irradiation_event_uid)

                        logger.debug(u"Import match on StudyInstUID {0}. After {1} s, existing event UIDs are {2}."
                                     u"".format(study_uid, sleep_time, existing_event_uids_post_delay))
                        if existing_event_uids_post_delay == new_event_uids:
                            # Now they are the same
                            logger.debug(u"Import match on StudyInstUID {0}. Event level match after delay, will not "
                                         u"import.".format(study_uid))
                            record_sop_instance_uid(existing_study_uid_match[study_index], new_sop_instance_uid)
                            return
                        elif new_event_uids.issubset(existing_event_uids_post_delay):
                            # Existing now has more events including those in the new RDSR
                            logger.debug(u"Import match on StudyInstUID {0}. Existing has more events than the new RDSR"
                                         u"after the delay, including the new ones, so will not import")
                            record_sop_instance_uid(existing_study_uid_match[study_index], new_sop_instance_uid)
                            return
                        # Can't be fewer in new RDSR at this point, so new must still have more, so use new one
                        existing_study_uid_match[study_index].delete()
                        keep_existing_sop_instance_uids = True
                        logger.debug(u"Import match on StudyInstUID {0}. After delay, new RDSR has more events than "
                                     u"existing. Not certain that existing had finished importing. Existing will be"
                                     u"deleted and replaced.".format(study_uid))

    g = GeneralStudyModuleAttr.objects.create()
    if not g:  # Allows import to be aborted if no template found
        return
    new_sop_instance_uid = dataset.SOPInstanceUID
    record_sop_instance_uid(g, new_sop_instance_uid)
    if keep_existing_sop_instance_uids:
        for sop_instance_uid in existing_sop_instance_uids:
            record_sop_instance_uid(g, sop_instance_uid)
    ch = get_value_kw('SpecificCharacterSet', dataset)
    _generalequipmentmoduleattributes(dataset, g, ch)
    _generalstudymoduleattributes(dataset, g, ch)
    _patientstudymoduleattributes(dataset, g)
    _patientmoduleattributes(dataset, g, ch)

    try:
        SkinDoseMapCalcSettings.objects.get()
    except ObjectDoesNotExist:
        SkinDoseMapCalcSettings.objects.create()

    enable_skin_dose_maps = SkinDoseMapCalcSettings.objects.values_list('enable_skin_dose_maps', flat=True)[0]
    calc_on_import = SkinDoseMapCalcSettings.objects.values_list('calc_on_import', flat=True)[0]
    if g.modality_type == 'RF' and enable_skin_dose_maps and calc_on_import:
        from remapp.tools.make_skin_map import make_skin_map
        make_skin_map.delay(g.pk)

    # Calculate summed total DAP and dose at RP for studies that have this study's patient ID, going back week_delta
    # weeks in time from this study date. Only do this if activated in the fluoro alert settings (check whether
    # HighDoseMetricAlertSettings.calc_accum_dose_over_delta_weeks_on_import is True).
    if g.modality_type == 'RF':
        from remapp.models import HighDoseMetricAlertSettings, AccumIntegratedProjRadiogDose
        try:
            HighDoseMetricAlertSettings.objects.get()
        except ObjectDoesNotExist:
            HighDoseMetricAlertSettings.objects.create()

        week_delta = HighDoseMetricAlertSettings.objects.values_list('accum_dose_delta_weeks', flat=True)[0]
        calc_accum_dose_over_delta_weeks_on_import = HighDoseMetricAlertSettings.objects.values_list('calc_accum_dose_over_delta_weeks_on_import', flat=True)[0]
        if calc_accum_dose_over_delta_weeks_on_import:
            from datetime import timedelta
            from django.db.models import Sum
            from remapp.models import PKsForSummedRFDoseStudiesInDeltaWeeks

            all_rf_studies = GeneralStudyModuleAttr.objects.filter(modality_type__exact='RF').all()

            patient_id = g.patientmoduleattr_set.values_list('patient_id', flat=True)[0]
            if patient_id:
                study_date = g.study_date
                oldest_date = (study_date - timedelta(weeks=week_delta))

                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # The try and except parts of this code are here because some of the studies in my database didn't have the
                # expected data in the related fields - not sure why. Perhaps an issue with the extractor routine?
                try:
                    g.projectionxrayradiationdose_set.get().accumxraydose_set.all()
                except ObjectDoesNotExist:
                    g.projectionxrayradiationdose_set.get().accumxraydose_set.create()

                for accumxraydose in g.projectionxrayradiationdose_set.get().accumxraydose_set.all():
                    try:
                        accumxraydose.accumintegratedprojradiogdose_set.get()
                    except:
                        accumxraydose.accumintegratedprojradiogdose_set.create()
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                for accumxraydose in g.projectionxrayradiationdose_set.get().accumxraydose_set.all():
                    accum_int_proj_pk = accumxraydose.accumintegratedprojradiogdose_set.get().pk

                    accum_int_proj_to_update = AccumIntegratedProjRadiogDose.objects.get(pk=accum_int_proj_pk)

                    included_studies = all_rf_studies.filter(patientmoduleattr__patient_id__exact=patient_id, study_date__range=[oldest_date, study_date])

                    bulk_entries = []
                    for pk in included_studies.values_list('pk', flat=True):
                        new_entry = PKsForSummedRFDoseStudiesInDeltaWeeks()
                        new_entry.general_study_module_attributes_id = g.pk
                        new_entry.study_pk_in_delta_weeks = pk
                        bulk_entries.append(new_entry)

                    if len(bulk_entries):
                        PKsForSummedRFDoseStudiesInDeltaWeeks.objects.bulk_create(bulk_entries)

                    accum_totals = included_studies.aggregate(Sum('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total'),
                                                              Sum('projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total'))
                    accum_int_proj_to_update.dose_area_product_total_over_delta_weeks = accum_totals['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total__sum']
                    accum_int_proj_to_update.dose_rp_total_over_delta_weeks = accum_totals['projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_rp_total__sum']
                    accum_int_proj_to_update.save()

        # Send an e-mail to all high dose alert recipients if this study is at or above threshold levels
        send_alert_emails = HighDoseMetricAlertSettings.objects.values_list('send_high_dose_metric_alert_emails', flat=True)[0]
        if send_alert_emails:
            from remapp.tools.send_high_dose_alert_emails import send_rf_high_dose_alert_email
            send_rf_high_dose_alert_email(g.pk)


def _fix_toshiba_vhp(dataset):
    """
    Replace forward slash in multi-value decimal string VR with back slash
    :param dataset: DICOM dataset
    :return: Repaired DICOM dataset
    """

    for cont in dataset.ContentSequence:
        if cont.ConceptNameCodeSequence[0].CodeMeaning == "CT Acquisition":
            for cont2 in cont.ContentSequence:
                if cont2.ConceptNameCodeSequence[0].CodeMeaning == "Dose Reduce Parameters" and \
                        cont2.ConceptNameCodeSequence[0].CodingSchemeDesignator == "99TOSHIBA-TMSC":
                    for cont3 in cont2.ContentSequence:
                        if cont3.ConceptNameCodeSequence[0].CodeMeaning == "Standard deviation of population":
                            try:
                                cont3.MeasuredValueSequence[0].NumericValue
                            except ValueError:
                                vhp_sd = dict.__getitem__(cont3.MeasuredValueSequence[0], 0x40a30a)
                                vhp_sd_value = vhp_sd.__getattribute__('value')
                                if '/' in vhp_sd_value:
                                    vhp_sd_value = vhp_sd_value.replace('/', '\\')
                                    new_vhp_sd = vhp_sd._replace(value=vhp_sd_value)
                                    dict.__setitem__(cont3.MeasuredValueSequence[0], 0x40a30a, new_vhp_sd)


@shared_task(name='remapp.extractors.rdsr.rdsr')
def rdsr(rdsr_file):
    """Extract radiation dose related data from DICOM Radiation SR objects.

    :param filename: relative or absolute path to Radiation Dose Structured Report.
    :type filename: str.
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
    try:
        dataset.decode()
    except ValueError as e:
        if "Invalid tag (0040, a30a): invalid literal for float()" in e.message:
            _fix_toshiba_vhp(dataset)
            dataset.decode()

    if dataset.SOPClassUID in ('1.2.840.10008.5.1.4.1.1.88.67', '1.2.840.10008.5.1.4.1.1.88.22') and \
            dataset.ConceptNameCodeSequence[0].CodeValue == '113701':
        logger.debug(u'rdsr.py extracting from {0}'.format(rdsr_file))
        _rsdr2db(dataset)
    else:
        logger.warning(u'rdsr.py not attempting to extract from {0}, not a radiation dose structured report'.format(
            rdsr_file))

    if del_rdsr:
        os.remove(rdsr_file)

    return 0


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit(u'Error: Supply exactly one argument - the DICOM RDSR file')

    sys.exit(rdsr(sys.argv[1]))
