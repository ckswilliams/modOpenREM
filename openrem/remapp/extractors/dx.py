# -*- coding: utf-8 -*-
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
#
#    This file (dx.py) is intended to extract radiation dose related data from
#    DX images. It is based on mam.py.
#    David Platten, 28/3/2014
#
"""
..  module:: dx.
    :synopsis: Module to extract radiation dose related data from DX image objects.

..  moduleauthor:: David Platten, Ed McDonagh

"""

import os
import sys
import django
import logging

logger = logging.getLogger(__name__)

# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

from celery import shared_task


def _xrayfilters(filttype, material, thickmax, thickmin, source):
    from remapp.models import XrayFilters
    from remapp.tools.get_values import get_or_create_cid
    filters = XrayFilters.objects.create(irradiation_event_xray_source_data=source)
    if filttype:
        filter_types = {'STRIP': {"code": '113650', "meaning": "Strip filter"},
                        'WEDGE': {"code": '113651', "meaning": "Wedge filter"},
                        'BUTTERFLY': {"code:": '113652', "meaning": "Butterfly filter"},
                        'NONE': {"code": '111609', "meaning": "No filter"},
                        'FLAT': {"code": '113653', "meaning": "Flat filter"},
                        }
        if filttype in filter_types:
            filters.xray_filter_type = get_or_create_cid(
                filter_types[filttype]["code"], filter_types[filttype]["meaning"]
            )
    if material:
        if material.strip().lower() == 'molybdenum':
            filters.xray_filter_material = get_or_create_cid('C-150F9', 'Molybdenum or Molybdenum compound')
        if material.strip().lower() == 'rhodium':
            filters.xray_filter_material = get_or_create_cid('C-167F9', 'Rhodium or Rhodium compound')
        if material.strip().lower() == 'silver':
            filters.xray_filter_material = get_or_create_cid('C-137F9', 'Silver or Silver compound')
        if material.strip().lower() == 'aluminum':
            filters.xray_filter_material = get_or_create_cid('C-120F9', 'Aluminum or Aluminum compound')
        if material.strip().lower() == 'copper':
            filters.xray_filter_material = get_or_create_cid('C-127F9', 'Copper or Copper compound')
        if material.strip().lower() == 'niobium':
            filters.xray_filter_material = get_or_create_cid('C-1190E', 'Niobium or Niobium compound')
        if material.strip().lower() == 'europium':
            filters.xray_filter_material = get_or_create_cid('C-1190F', 'Europium or Europium compound')
        if material.strip().lower() == 'lead':
            filters.xray_filter_material = get_or_create_cid('C-132F9', 'Lead or Lead compound')
        if material.strip().lower() == 'tantalum':
            filters.xray_filter_material = get_or_create_cid('C-156F9', 'Tantalum or Tantalum compound')
    if thickmax:
        filters.xray_filter_thickness_maximum = thickmax
    if thickmin:
        filters.xray_filter_thickness_minimum = thickmin
    filters.save()


def _xrayfiltersnone(source):
    from remapp.models import XrayFilters
    from remapp.tools.get_values import get_value_kw, get_or_create_cid
    filters = XrayFilters.objects.create(irradiation_event_xray_source_data=source)
    filters.xray_filter_type = get_or_create_cid('111609', "No filter")
    filters.save()


def _xray_filters_multiple(xray_filter_material, xray_filter_thickness_maximum, xray_filter_thickness_minimum, source):
    from dicom.valuerep import MultiValue
    if ',' in xray_filter_material and not isinstance(xray_filter_material, MultiValue):
        xray_filter_material = xray_filter_material.split(',')
    for i, material in enumerate(xray_filter_material):
        try:
            thickmax = None
            thickmin = None
            if isinstance(xray_filter_thickness_maximum, list):
                thickmax = xray_filter_thickness_maximum[i]
            if isinstance(xray_filter_thickness_minimum, list):
                thickmin = xray_filter_thickness_minimum[i]
            _xrayfilters('FLAT', material, thickmax, thickmin, source)
        except IndexError:
            pass


def _kvp(dataset, source):
    from remapp.models import Kvp
    from remapp.tools.get_values import get_value_kw
    kv = Kvp.objects.create(irradiation_event_xray_source_data=source)
    kv.kvp = get_value_kw('KVP', dataset)
    kv.save()


def _exposure(dataset, source):
    from remapp.models import Exposure
    exp = Exposure.objects.create(irradiation_event_xray_source_data=source)
    from remapp.tools.get_values import get_value_kw
    exp.exposure = get_value_kw('ExposureInuAs', dataset)  # uAs
    if not exp.exposure:
        exposure = get_value_kw('Exposure', dataset)
        if exposure:
            exp.exposure = exposure * 1000
    exp.save()


def _xraygrid(gridcode, source):
    from remapp.models import XrayGrid
    from remapp.tools.get_values import get_or_create_cid
    grid = XrayGrid.objects.create(irradiation_event_xray_source_data=source)
    if gridcode == '111646':
        grid.xray_grid = get_or_create_cid('111646', 'No grid')
    elif gridcode == '111641':
        grid.xray_grid = get_or_create_cid('111641', 'Fixed grid')
    elif gridcode == '111642':
        grid.xray_grid = get_or_create_cid('111642', 'Focused grid')
    elif gridcode == '111643':
        grid.xray_grid = get_or_create_cid('111643', 'Reciprocating grid')
    elif gridcode == '111644':
        grid.xray_grid = get_or_create_cid('111644', 'Parallel grid')
    elif gridcode == '111645':
        grid.xray_grid = get_or_create_cid('111645', 'Crossed grid')
    grid.save()


def _irradiationeventxraydetectordata(dataset, event):
    from remapp.models import IrradEventXRayDetectorData
    from remapp.tools.get_values import get_value_kw, get_or_create_cid
    detector = IrradEventXRayDetectorData.objects.create(irradiation_event_xray_data=event)
    detector.exposure_index = get_value_kw('ExposureIndex', dataset)
    detector.relative_xray_exposure = get_value_kw('RelativeXRayExposure', dataset)
    manufacturer = \
    detector.irradiation_event_xray_data.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.all()[
        0].manufacturer.lower()
    if 'fuji' in manufacturer:
        detector.relative_exposure_unit = 'S ()'
    elif 'carestream' in manufacturer:
        detector.relative_exposure_unit = 'EI (Mbels)'
    elif 'kodak' in manufacturer:
        detector.relative_exposure_unit = 'EI (Mbels)'
    elif 'agfa' in manufacturer:
        detector.relative_exposure_unit = 'lgM (Bels)'
    elif 'konica' in manufacturer:
        detector.relative_exposure_unit = 'S ()'
    elif 'canon' in manufacturer:
        detector.relative_exposure_unit = 'REX ()'
    elif 'swissray' in manufacturer:
        detector.relative_exposure_unit = 'DI ()'
    elif 'philips' in manufacturer:
        detector.relative_exposure_unit = 'EI ()'
    elif 'siemens' in manufacturer:
        detector.relative_exposure_unit = u'EXI (μGy)'
    detector.sensitivity = get_value_kw('Sensitivity', dataset)
    detector.target_exposure_index = get_value_kw('TargetExposureIndex', dataset)
    detector.deviation_index = get_value_kw('DeviationIndex', dataset)
    detector.save()


def _irradiationeventxraysourcedata(dataset, event):
    # TODO: review model to convert to cid where appropriate, and add additional fields such as field height and width
    from remapp.models import IrradEventXRaySourceData
    from remapp.tools.get_values import get_value_kw, get_or_create_cid
    source = IrradEventXRaySourceData.objects.create(irradiation_event_xray_data=event)
    source.average_xray_tube_current = get_value_kw('XRayTubeCurrent', dataset)
    if not source.average_xray_tube_current: source.average_xray_tube_current = get_value_kw('AverageXRayTubeCurrent',
                                                                                             dataset)
    source.exposure_time = get_value_kw('ExposureTime', dataset)
    source.irradiation_duration = get_value_kw('IrradiationDuration', dataset)
    source.focal_spot_size = get_value_kw('FocalSpots', dataset)
    collimated_field_area = get_value_kw('FieldOfViewDimensions', dataset)
    if collimated_field_area:
        source.collimated_field_area = float(collimated_field_area[0]) * float(collimated_field_area[1]) / 1000000
    exp_ctrl_mode = get_value_kw('ExposureControlMode', dataset)
    if exp_ctrl_mode:
        source.exposure_control_mode = exp_ctrl_mode
    xray_grid = get_value_kw('Grid', dataset)
    if xray_grid:
        if xray_grid == 'NONE':
            _xraygrid('111646', source)
        else:
            for gtype in xray_grid:
                if 'FI' in gtype:  # Fixed; abbreviated due to fitting two keywords in 16 characters
                    _xraygrid('111641', source)
                elif 'FO' in gtype:  # Focused
                    _xraygrid('111642', source)
                elif 'RE' in gtype:  # Reciprocating
                    _xraygrid('111643', source)
                elif 'PA' in gtype:  # Parallel
                    _xraygrid('111644', source)
                elif 'CR' in gtype:  # Crossed
                    _xraygrid('111645', source)
    source.grid_absorbing_material = get_value_kw('GridAbsorbingMaterial', dataset)
    source.grid_spacing_material = get_value_kw('GridSpacingMaterial', dataset)
    source.grid_thickness = get_value_kw('GridThickness', dataset)
    source.grid_pitch = get_value_kw('GridPitch', dataset)
    source.grid_aspect_ratio = get_value_kw('GridAspectRatio', dataset)
    source.grid_period = get_value_kw('GridPeriod', dataset)
    source.grid_focal_distance = get_value_kw('GridFocalDistance', dataset)
    source.save()
    xray_filter_type = get_value_kw('FilterType', dataset)
    xray_filter_material = get_value_kw('FilterMaterial', dataset)

    try:  # Black magic pydicom method suggested by Darcy Mason: https://groups.google.com/forum/?hl=en-GB#!topic/pydicom/x_WsC2gCLck
        xray_filter_thickness_minimum = get_value_kw('FilterThicknessMinimum', dataset)
    except ValueError:  # Assumes ValueError will be a comma separated pair of numbers, as per Kodak.
        thick = dict.__getitem__(dataset, 0x187052)  # pydicom black magic as suggested by
        thickval = thick.__getattribute__('value')
        if ',' in thickval:
            thickval = thickval.replace(',', '\\')
            thick2 = thick._replace(value=thickval)
            dict.__setitem__(dataset, 0x187052, thick2)
            xray_filter_thickness_minimum = get_value_kw('FilterThicknessMinimum', dataset)
        else:
            xray_filter_thickness_minimum = None

    try:
        xray_filter_thickness_maximum = get_value_kw('FilterThicknessMaximum', dataset)
    except ValueError:  # Assumes ValueError will be a comma separated pair of numbers, as per Kodak.
        thick = dict.__getitem__(dataset, 0x187054)  # pydicom black magic as suggested by
        thickval = thick.__getattribute__('value')
        if ',' in thickval:
            thickval = thickval.replace(',', '\\')
            thick2 = thick._replace(value=thickval)
            dict.__setitem__(dataset, 0x187054, thick2)
            xray_filter_thickness_maximum = get_value_kw('FilterThicknessMaximum', dataset)
        else:
            xray_filter_thickness_maximum = None

    if xray_filter_type:
        if xray_filter_type == 'NONE':
            _xrayfiltersnone(source)
        elif xray_filter_type == 'MULTIPLE' and xray_filter_material:
            _xray_filters_multiple(
                xray_filter_material, xray_filter_thickness_maximum, xray_filter_thickness_minimum, source)
        else:
            siemens_filters = ("CU_0.1_MM", "CU_0.2_MM", "CU_0.3_MM")
            if xray_filter_type in siemens_filters:
                if xray_filter_type == "CU_0.1_MM":
                    thickmax = 0.1
                    thickmin = 0.1
                elif xray_filter_type == "CU_0.2_MM":
                    thickmax = 0.2
                    thickmin = 0.2
                elif xray_filter_type == "CU_0.3_MM":
                    thickmax = 0.3
                    thickmin = 0.3
                _xrayfilters("FLAT", "COPPER", thickmax, thickmin, source)
            else:
                _xrayfilters(
                    xray_filter_type, xray_filter_material, xray_filter_thickness_maximum,
                    xray_filter_thickness_minimum, source
                )
    _kvp(dataset, source)
    _exposure(dataset, source)


def _doserelateddistancemeasurements(dataset, mech):
    from remapp.models import DoseRelatedDistanceMeasurements
    from remapp.tools.get_values import get_value_kw, get_value_num
    dist = DoseRelatedDistanceMeasurements.objects.create(irradiation_event_xray_mechanical_data=mech)
    manufacturer = \
    dist.irradiation_event_xray_mechanical_data.irradiation_event_xray_data.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.all()[
        0].manufacturer
    model_name = \
    dist.irradiation_event_xray_mechanical_data.irradiation_event_xray_data.projection_xray_radiation_dose.general_study_module_attributes.generalequipmentmoduleattr_set.all()[
        0].manufacturer_model_name
    dist.distance_source_to_detector = get_value_kw('DistanceSourceToDetector', dataset)
    if dist.distance_source_to_detector and manufacturer and model_name and "kodak" in manufacturer.lower() and "dr 7500" in model_name.lower():
        dist.distance_source_to_detector = dist.distance_source_to_detector * 100  # convert dm to mm
    dist.distance_source_to_entrance_surface = get_value_kw('DistanceSourceToPatient', dataset)
    dist.distance_source_to_isocenter = get_value_kw('DistanceSourceToIsocenter', dataset)
    # DistanceSourceToReferencePoint isn't a DICOM tag. Same as DistanceSourceToPatient?
    #    dist.distance_source_to_reference_point = get_value_kw('DistanceSourceToReferencePoint',dataset)
    # Table longitudinal and lateral positions not DICOM elements.
    #    dist.table_longitudinal_position = get_value_kw('TableLongitudinalPosition',dataset)
    #    dist.table_lateral_position = get_value_kw('TableLateralPosition',dataset)
    dist.table_height_position = get_value_kw('TableHeight', dataset)
    # DistanceSourceToTablePlane not a DICOM tag.
    #    dist.distance_source_to_table_plane = get_value_kw('DistanceSourceToTablePlane',dataset)
    dist.radiological_thickness = get_value_num(0x00451049, dataset)
    dist.save()


def _irradiationeventxraymechanicaldata(dataset, event):
    from remapp.models import IrradEventXRayMechanicalData
    from remapp.tools.get_values import get_value_kw
    mech = IrradEventXRayMechanicalData.objects.create(irradiation_event_xray_data=event)
    mech.magnification_factor = get_value_kw('EstimatedRadiographicMagnificationFactor', dataset)
    mech.dxdr_mechanical_configuration = get_value_kw('DX/DRMechanicalConfiguration', dataset)
    mech.primary_angle = get_value_kw('PositionerPrimaryAngle', dataset)
    mech.secondary_angle = get_value_kw('PositionerSecondaryAngle', dataset)
    mech.primary_end_angle = get_value_kw('PositionerPrimaryEndAngle', dataset)
    mech.secondary_angle = get_value_kw('PositionerSecondaryEndAngle', dataset)
    mech.column_angulation = get_value_kw('ColumnAngulation', dataset)
    mech.table_head_tilt_angle = get_value_kw('TableHeadTiltAngle', dataset)
    mech.table_horizontal_rotation_angle = get_value_kw('TableHorizontalRotationAngle', dataset)
    mech.table_cradle_tilt_angle = get_value_kw('TableCradleTiltAngle', dataset)
    mech.save()
    _doserelateddistancemeasurements(dataset, mech)


def _irradiationeventxraydata(dataset, proj):  # TID 10003
    # TODO: review model to convert to cid where appropriate, and add additional fields
    from remapp.models import IrradEventXRayData
    from remapp.tools.get_values import get_value_kw, get_or_create_cid, get_seq_code_value, get_seq_code_meaning
    from remapp.tools.dcmdatetime import make_date_time
    event = IrradEventXRayData.objects.create(projection_xray_radiation_dose=proj)
    event.acquisition_plane = get_or_create_cid('113622', 'Single Plane')
    event.irradiation_event_uid = get_value_kw('SOPInstanceUID', dataset)
    event_time = get_value_kw('AcquisitionTime', dataset)
    if not event_time: event_time = get_value_kw('ContentTime', dataset)
    if not event_time: event_time = get_value_kw('StudyTime', dataset)
    event_date = get_value_kw('AcquisitionDate', dataset)
    if not event_date: event_date = get_value_kw('ContentDate', dataset)
    if not event_date: event_date = get_value_kw('StudyDate', dataset)
    event.date_time_started = make_date_time('{0}{1}'.format(event_date, event_time))
    event.irradiation_event_type = get_or_create_cid('113611', 'Stationary Acquisition')
    event.acquisition_protocol = get_value_kw('ProtocolName', dataset)
    if not event.acquisition_protocol: event.acquisition_protocol = get_value_kw('SeriesDescription', dataset)
    acquisition_protocol = get_value_kw('ProtocolName', dataset)
    series_description = get_value_kw('SeriesDescription', dataset)
    if series_description:
        event.comment = series_description
    event.anatomical_structure = get_or_create_cid(get_seq_code_value('AnatomicRegionSequence', dataset),
                                                   get_seq_code_meaning('AnatomicRegionSequence', dataset))
    laterality = get_value_kw('ImageLaterality', dataset)
    if laterality:
        if laterality.strip() == 'R':
            event.laterality = get_or_create_cid('G-A100', 'Right')
        if laterality.strip() == 'L':
            event.laterality = get_or_create_cid('G-A101', 'Left')

    event.image_view = get_or_create_cid(get_seq_code_value('ViewCodeSequence', dataset),
                                         get_seq_code_meaning('ViewCodeSequence', dataset))
    if not event.image_view:
        projection = get_value_kw('ViewPosition', dataset)
        if projection == 'AP':
            event.image_view = get_or_create_cid('R-10206', 'antero-posterior')
        elif projection == 'PA':
            event.image_view = get_or_create_cid('R-10214', 'postero-anterior')
        elif projection == 'LL':
            event.image_view = get_or_create_cid('R-10236', 'left lateral')
        elif projection == 'RL':
            event.image_view = get_or_create_cid('R-10232', 'right lateral')
        # http://dicomlookup.com/lookup.asp?sw=Tnumber&q=(0018,5101) lists four other views: RLD (Right Lateral Decubitus),
        # LLD (Left Lateral Decubitus), RLO (Right Lateral Oblique) and LLO (Left Lateral Oblique). There isn't an exact
        # match for these views in the CID 4010 DX View (http://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_CID_4010.html)

    # image view modifier?
    if event.anatomical_structure:
        event.target_region = event.anatomical_structure
    event.entrance_exposure_at_rp = get_value_kw('EntranceDoseInmGy', dataset)
    # reference point definition?
    pc_fibroglandular = get_value_kw('CommentsOnRadiationDose', dataset)
    if pc_fibroglandular:
        if '%' in pc_fibroglandular:
            event.percent_fibroglandular_tissue = pc_fibroglandular.replace('%', '').strip()
    exposure_control = get_value_kw('ExposureControlModeDescription', dataset)

    if event.comment and exposure_control:
        event.comment = event.comment + ', ' + exposure_control

    dap = get_value_kw('ImageAndFluoroscopyAreaDoseProduct', dataset)
    if dap: event.dose_area_product = dap / 100000  # Value of DICOM tag (0018,115e) in dGy.cm2, converted to Gy.m2
    event.save()

    _irradiationeventxraydetectordata(dataset, event)
    _irradiationeventxraysourcedata(dataset, event)
    _irradiationeventxraymechanicaldata(dataset, event)
    _accumulatedxraydose_update(event)


def _accumulatedxraydose(proj):
    from remapp.models import AccumXRayDose, AccumIntegratedProjRadiogDose
    from remapp.tools.get_values import get_or_create_cid
    accum = AccumXRayDose.objects.create(projection_xray_radiation_dose=proj)
    accum.acquisition_plane = get_or_create_cid('113622', 'Single Plane')
    accum.save()
    accumint = AccumIntegratedProjRadiogDose.objects.create(accumulated_xray_dose=accum)
    accumint.dose_area_product_total = 0.0
    accumint.total_number_of_radiographic_frames = 0
    accumint.save()


def _accumulatedxraydose_update(event):
    from decimal import Decimal
    accumint = event.projection_xray_radiation_dose.accumxraydose_set.get().accumintegratedprojradiogdose_set.get()
    accumint.total_number_of_radiographic_frames = accumint.total_number_of_radiographic_frames + 1
    if event.dose_area_product:
        accumint.dose_area_product_total += Decimal(event.dose_area_product)
    accumint.save()


def _projectionxrayradiationdose(dataset, g):
    from remapp.models import ProjectionXRayRadiationDose
    from remapp.tools.get_values import get_or_create_cid
    proj = ProjectionXRayRadiationDose.objects.create(general_study_module_attributes=g)
    proj.procedure_reported = get_or_create_cid('113704', 'Projection X-Ray')
    proj.has_intent = get_or_create_cid('R-408C3', 'Diagnostic Intent')
    proj.scope_of_accumulation = get_or_create_cid('113014', 'Study')
    proj.source_of_dose_information = get_or_create_cid('113866', 'Copied From Image Attributes')
    proj.xray_detector_data_available = get_or_create_cid('R-00339', 'No')
    proj.xray_source_data_available = get_or_create_cid('R-0038D', 'Yes')
    proj.xray_mechanical_data_available = get_or_create_cid('R-0038D', 'Yes')
    proj.save()
    _accumulatedxraydose(proj)
    _irradiationeventxraydata(dataset, proj)


def _generalequipmentmoduleattributes(dataset, study):
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
            equip_display_name.display_name = 'Blank'
        equip_display_name.save()

    equip.unique_equipment_name = UniqueEquipmentNames(pk=equip_display_name.pk)

    equip.save()


def _patientstudymoduleattributes(dataset, g):  # C.7.2.2
    from remapp.models import PatientStudyModuleAttr
    from remapp.tools.get_values import get_value_kw
    patientatt = PatientStudyModuleAttr.objects.create(general_study_module_attributes=g)
    patientatt.patient_age = get_value_kw('PatientAge', dataset)
    patientatt.patient_weight = get_value_kw("PatientWeight", dataset)
    patientatt.patient_size = get_value_kw("PatientSize", dataset)
    patientatt.save()


def _patientmoduleattributes(dataset, g):  # C.7.1.1
    from decimal import Decimal
    from remapp.models import PatientModuleAttr, PatientStudyModuleAttr
    from remapp.models import PatientIDSettings
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import get_date
    from remapp.tools.not_patient_indicators import get_not_pt
    from remapp.tools.hash_id import hash_id

    pat = PatientModuleAttr.objects.create(general_study_module_attributes=g)
    pat.patient_sex = get_value_kw('PatientSex', dataset)
    patient_birth_date = get_date('PatientBirthDate', dataset)
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


def _generalstudymoduleattributes(dataset, g):
    from datetime import datetime
    from remapp.models import PatientIDSettings
    from remapp.tools.get_values import get_value_kw, get_seq_code_meaning, get_seq_code_value, get_value_num
    from remapp.tools.dcmdatetime import get_date, get_time
    from remapp.tools.hash_id import hash_id

    g.study_date = get_date('StudyDate', dataset)
    g.study_time = get_time('StudyTime', dataset)
    g.study_workload_chart_time = datetime.combine(datetime.date(datetime(1900, 1, 1)), datetime.time(g.study_time))
    g.referring_physician_name = get_value_kw('ReferringPhysicianName', dataset)
    g.referring_physician_identification = get_value_kw('ReferringPhysicianIdentification', dataset)
    g.study_id = get_value_kw('StudyID', dataset)
    accession_number = get_value_kw('AccessionNumber', dataset)
    patient_id_settings = PatientIDSettings.objects.get()
    if accession_number and patient_id_settings.accession_hashed:
        accession_number = hash_id(accession_number)
        g.accession_hashed = True
    g.accession_number = accession_number
    g.study_description = get_value_kw('StudyDescription', dataset)
    if not g.study_description: g.study_description = get_value_kw('SeriesDescription', dataset)
    g.modality_type = get_value_kw('Modality', dataset)
    g.physician_of_record = get_value_kw('PhysicianOfRecord', dataset)
    g.name_of_physician_reading_study = get_value_kw('NameOfPhysicianReadingStudy', dataset)
    g.performing_physician_name = get_value_kw('PerformingPhysicianName', dataset)
    g.operator_name = get_value_kw('OperatorsName', dataset)
    g.procedure_code_meaning = get_value_kw('ProtocolName', dataset)  # Being used to summarise protocol for study
    if not g.procedure_code_meaning: g.procedure_code_meaning = get_value_kw('StudyDescription', dataset)
    if not g.procedure_code_meaning: g.procedure_code_meaning = get_value_kw('SeriesDescription', dataset)
    g.requested_procedure_code_value = get_seq_code_value('RequestedProcedureCodeSequence', dataset)
    g.requested_procedure_code_meaning = get_seq_code_meaning('RequestedProcedureCodeSequence', dataset)
    if not g.requested_procedure_code_value: g.requested_procedure_code_value = get_seq_code_value(
        'RequestAttributesSequence', dataset)
    if not g.requested_procedure_code_value: g.requested_procedure_code_value = get_seq_code_value(
        'PerformedProtocolCodeSequence', dataset)
    if not g.requested_procedure_code_meaning: g.requested_procedure_code_meaning = get_seq_code_meaning(
        'RequestAttributesSequence', dataset)
    if not g.requested_procedure_code_meaning: g.requested_procedure_code_meaning = get_value_num(0x00321060, dataset)
    if not g.requested_procedure_code_meaning: g.requested_procedure_code_meaning = get_seq_code_meaning(
        'PerformedProtocolCodeSequence', dataset)
    if not g.requested_procedure_code_meaning:
        manufacturer = get_value_kw("Manufacturer", dataset)
        model = get_value_kw("ManufacturerModelName", dataset)
        if manufacturer and model and 'canon' in manufacturer.lower() and 'cxdi' in model.lower():
            g.requested_procedure_code_meaning = get_value_num(0x00081030, dataset)
    g.save()

    _generalequipmentmoduleattributes(dataset, g)
    _projectionxrayradiationdose(dataset, g)
    _patientstudymoduleattributes(dataset, g)
    _patientmoduleattributes(dataset, g)


# The routine will accept three types of image:
# CR image storage                               (SOP UID = '1.2.840.10008.5.1.4.1.1.1')
# Digital x-ray image storage - for presentation (SOP UID = '1.2.840.10008.5.1.4.1.1.1.1')
# Digital x-ray image storage - for processing   (SOP UID = '1.2.840.10008.5.1.4.1.1.1.1.1')
# These SOP UIDs were taken from http://www.dicomlibrary.com/dicom/sop/
def _test_if_dx(dataset):
    """ Test if dicom object passed is a DX or CR radiographic file by looking at SOP Class UID"""
    if dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.1' and dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.1.1' and dataset.SOPClassUID != '1.2.840.10008.5.1.4.1.1.1.1.1':
        return 0
    return 1


def _create_event(dataset):
    """
    If study exists, create new event
    :param dataset: DICOM object
    :return: Nothing
    """
    from remapp.models import GeneralStudyModuleAttr
    from remapp.tools import check_uid
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import make_date_time

    study_uid = get_value_kw('StudyInstanceUID', dataset)
    event_uid = get_value_kw('SOPInstanceUID', dataset)
    inst_in_db = check_uid.check_uid(event_uid, 'Event')
    if inst_in_db:
        return 0
    same_study_uid = GeneralStudyModuleAttr.objects.filter(study_instance_uid__exact=study_uid)
    if same_study_uid.count() != 1:
        print "Duplicate study UIDs in database! Could be a problem."
        for dup in same_study_uid:
            if dup.modality_type:
                same_study_uid = dup
                continue
    # further check required to ensure 'for processing' and 'for presentation'
    # versions of the same irradiation event don't get imported twice
    event_time = get_value_kw('AcquisitionTime', dataset)
    if not event_time:
        event_time = get_value_kw('ContentTime', dataset)
    event_date = get_value_kw('AcquisitionDate', dataset)
    if not event_date:
        event_date = get_value_kw('ContentDate', dataset)
    event_date_time = make_date_time('{0}{1}'.format(event_date, event_time))
    try:
        for events in same_study_uid.get().projectionxrayradiationdose_set.get().irradeventxraydata_set.all():
            if event_date_time == events.date_time_started:
                return 0
    except Exception as e:
        logger.warning("DX study UID %s, event UID %s failed at check for identical event. Error %s",
                       study_uid, event_uid, e)
    # study exists, but event doesn't
    _irradiationeventxraydata(dataset, same_study_uid.get().projectionxrayradiationdose_set.get())
    # update the accumulated tables
    return 0


def _dx2db(dataset):
    import os, sys
    import openrem_settings
    from time import sleep
    from random import random

    os.environ['DJANGO_SETTINGS_MODULE'] = 'openrem.openremproject.settings'
    from django.db import models

    openrem_settings.add_project_to_path()
    from remapp.models import GeneralStudyModuleAttr
    from remapp.tools import check_uid
    from remapp.tools.get_values import get_value_kw
    from remapp.tools.dcmdatetime import make_date_time

    study_uid = get_value_kw('StudyInstanceUID', dataset)
    if not study_uid:
        sys.exit('No UID returned')
    study_in_db = check_uid.check_uid(study_uid)

    if study_in_db == 1:
        sleep(2.)  # Give initial event a chance to get to save on _projectionxrayradiationdose
        _create_event(dataset)

    if not study_in_db:
        # study doesn't exist, start from scratch
        g = GeneralStudyModuleAttr.objects.create()
        g.study_instance_uid = get_value_kw('StudyInstanceUID', dataset)
        g.save()
        # check again
        study_in_db = check_uid.check_uid(study_uid)
        if study_in_db == 1:
            _generalstudymoduleattributes(dataset, g)
        elif not study_in_db:
            sys.exit("Something went wrong, GeneralStudyModuleAttr wasn't created")
        elif study_in_db > 1:
            sleep(random())
            # Check if other instance(s) has deleted the study yet
            study_in_db = check_uid.check_uid(study_uid)
            if study_in_db == 1:
                _generalstudymoduleattributes(dataset, g)
            elif study_in_db > 1:
                g.delete()
                study_in_db = check_uid.check_uid(study_uid)
                if not study_in_db:
                    # both must have been deleted simultaneously!
                    sleep(random())
                    # Check if other instance has created the study again yet
                    study_in_db = check_uid.check_uid(study_uid)
                    if study_in_db == 1:
                        sleep(2.)  # Give initial event a chance to get to save on _projectionxrayradiationdose
                        _create_event(dataset)
                    while not study_in_db:
                        g = GeneralStudyModuleAttr.objects.create()
                        g.study_instance_uid = get_value_kw('StudyInstanceUID', dataset)
                        g.save()
                        # check again
                        study_in_db = check_uid.check_uid(study_uid)
                        if study_in_db == 1:
                            _generalstudymoduleattributes(dataset, g)
                        elif study_in_db > 1:
                            g.delete()
                            sleep(random())
                            study_in_db = check_uid.check_uid(study_uid)
                            if study_in_db == 1:
                                sleep(2.)  # Give initial event a chance to get to save on _projectionxrayradiationdose
                                _create_event(dataset)
                elif study_in_db == 1:
                    sleep(2.)  # Give initial event a chance to get to save on _projectionxrayradiationdose
                    _create_event(dataset)


@shared_task
def dx(dig_file):
    """Extract radiation dose structured report related data from DX radiographic images

    :param filename: relative or absolute path to DICOM DX radiographic image file.
    :type filename: str.

    Tested with:
        Nothing yet

    """

    import dicom
    from django.core.exceptions import ObjectDoesNotExist
    from remapp.models import DicomDeleteSettings
    try:
        del_settings = DicomDeleteSettings.objects.get()
        del_dx_im = del_settings.del_dx_im
    except ObjectDoesNotExist:
        del_dx_im = False

    dataset = dicom.read_file(dig_file)
    isdx = _test_if_dx(dataset)
    if not isdx:
        return '{0} is not a DICOM DX radiographic image'.format(dig_file)

    _dx2db(dataset)

    if del_dx_im:
        os.remove(dig_file)

    return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit('Error: Supply exactly one argument - the DICOM DX radiographic image file')

    sys.exit(dx(sys.argv[1]))
