from remapp.models import (GeneralStudyModuleAttr,
    ProjectionXRayRadiationDose, Observer_context,
    AccumXRayDose, Calibration, IrradEventXRayData,
    ImageViewModifier, PersonParticipant,
    IrradEventXRayDetectorData, IrradEventXRaySourceData,
    Pulse_width, Kvp, Xray_tube_current, Exposure, Xray_filters, Xray_grid,
    DeviceParticipant, IrradEventXRayMechanicalData,
    Dose_related_distance_measurements, AccumProjectionXRayDose,
    AccumMammographyXRayDose,
    AccumCassetteBsdProjRadiogDose,
    AccumIntegratedProjRadiogDose,
    Patient_module_attributes, General_equipment_module_attributes, 
    Patient_study_module_attributes, ContextID,
    CtRadiationDose, CtAccumulatedDoseData,
    CtIrradiationEventData, Scanning_length,
    CtDoseCheckDetails, CtXRaySourceParameters,
    Exports, SizeUpload)

from django.contrib import admin

admin.site.register(GeneralStudyModuleAttr)
admin.site.register(ProjectionXRayRadiationDose)
admin.site.register(Observer_context)
admin.site.register(AccumXRayDose)
admin.site.register(Calibration)
admin.site.register(IrradEventXRayData)
admin.site.register(ImageViewModifier)
admin.site.register(PersonParticipant)
admin.site.register(IrradEventXRayDetectorData)
admin.site.register(IrradEventXRaySourceData)
admin.site.register(Pulse_width)
admin.site.register(Kvp)
admin.site.register(Xray_tube_current)
admin.site.register(Exposure)
admin.site.register(Xray_filters)
admin.site.register(Xray_grid)
admin.site.register(DeviceParticipant)
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
admin.site.register(CtRadiationDose)
admin.site.register(CtAccumulatedDoseData)
admin.site.register(CtIrradiationEventData)
admin.site.register(Scanning_length)
admin.site.register(CtDoseCheckDetails)
admin.site.register(CtXRaySourceParameters)
admin.site.register(Exports)
admin.site.register(SizeUpload)
