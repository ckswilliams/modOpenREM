from remapp.models import (GeneralStudyModuleAttr,
    ProjectionXRayRadiationDose, Observer_context,
    AccumXRayDose, Calibration, IrradEventXRayData,
    ImageViewModifier, Person_participant,
    IrradEventXRayDetectorData, IrradEventXRaySourceData,
    Pulse_width, Kvp, Xray_tube_current, Exposure, Xray_filters, Xray_grid,
    Device_participant, IrradEventXRayMechanicalData,
    Dose_related_distance_measurements, AccumProjectionXRayDose,
    AccumMammographyXRayDose,
    AccumCassetteBsdProjRadiogDose,
    AccumIntegratedProjRadiogDose,
    Patient_module_attributes, General_equipment_module_attributes, 
    Patient_study_module_attributes, ContextID,
    Ct_radiation_dose, Ct_accumulated_dose_data,
    Ct_irradiation_event_data, Scanning_length,
    Ct_dose_check_details, Ct_xray_source_parameters,
    Exports, SizeUpload)

from django.contrib import admin

admin.site.register(GeneralStudyModuleAttr)
admin.site.register(ProjectionXRayRadiationDose)
admin.site.register(Observer_context)
admin.site.register(AccumXRayDose)
admin.site.register(Calibration)
admin.site.register(IrradEventXRayData)
admin.site.register(ImageViewModifier)
admin.site.register(Person_participant)
admin.site.register(IrradEventXRayDetectorData)
admin.site.register(IrradEventXRaySourceData)
admin.site.register(Pulse_width)
admin.site.register(Kvp)
admin.site.register(Xray_tube_current)
admin.site.register(Exposure)
admin.site.register(Xray_filters)
admin.site.register(Xray_grid)
admin.site.register(Device_participant)
admin.site.register(IrradEventXRayMechanicalData)
admin.site.register(Dose_related_distance_measurements)
admin.site.register(AccumProjectionXRayDose)
admin.site.register(AccumMammographyXRayDose)
admin.site.register(AccumCassetteBsdProjRadiogDose)
admin.site.register(AccumIntegratedProjRadiogDose)
admin.site.register(Patient_module_attributes)
admin.site.register(General_equipment_module_attributes)
admin.site.register(Patient_study_module_attributes)
admin.site.register(ContextID)
admin.site.register(Ct_radiation_dose)
admin.site.register(Ct_accumulated_dose_data)
admin.site.register(Ct_irradiation_event_data)
admin.site.register(Scanning_length)
admin.site.register(Ct_dose_check_details)
admin.site.register(Ct_xray_source_parameters)
admin.site.register(Exports)
admin.site.register(SizeUpload)
