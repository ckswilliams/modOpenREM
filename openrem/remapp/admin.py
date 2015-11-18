from remapp.models import (GeneralStudyModuleAttr,
    ProjectionXRayRadiationDose, ObserverContext,
    AccumXRayDose, Calibration, IrradEventXRayData,
    ImageViewModifier, PersonParticipant,
    IrradEventXRayDetectorData, IrradEventXRaySourceData,
    PulseWidth, Kvp, XrayTubeCurrent, Exposure, XrayFilters, XrayGrid,
    DeviceParticipant, IrradEventXRayMechanicalData,
    DoseRelatedDistanceMeasurements, AccumProjXRayDose,
    AccumMammographyXRayDose,
    AccumCassetteBsdProjRadiogDose,
    AccumIntegratedProjRadiogDose,
    PatientModuleAttr, GeneralEquipmentModuleAttr,
    PatientStudyModuleAttr, ContextID,
    CtRadiationDose, CtAccumulatedDoseData,
    CtIrradiationEventData, ScanningLength,
    CtDoseCheckDetails, CtXRaySourceParameters,
    Exports, SizeUpload,
    UniqueEquipmentNames, DicomStoreSCP, DicomRemoteQR, DicomDeleteSettings,
    DicomQuery, DicomQRRspStudy, DicomQRRspSeries, DicomQRRspImage
)

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from remapp.models import PatientIDSettings

admin.site.register(PatientIDSettings, SingletonModelAdmin)

admin.site.register(GeneralStudyModuleAttr)
admin.site.register(ProjectionXRayRadiationDose)
admin.site.register(ObserverContext)
admin.site.register(AccumXRayDose)
admin.site.register(Calibration)
admin.site.register(IrradEventXRayData)
admin.site.register(ImageViewModifier)
admin.site.register(PersonParticipant)
admin.site.register(IrradEventXRayDetectorData)
admin.site.register(IrradEventXRaySourceData)
admin.site.register(PulseWidth)
admin.site.register(Kvp)
admin.site.register(XrayTubeCurrent)
admin.site.register(Exposure)
admin.site.register(XrayFilters)
admin.site.register(XrayGrid)
admin.site.register(DeviceParticipant)
admin.site.register(IrradEventXRayMechanicalData)
admin.site.register(DoseRelatedDistanceMeasurements)
admin.site.register(AccumProjXRayDose)
admin.site.register(AccumMammographyXRayDose)
admin.site.register(AccumCassetteBsdProjRadiogDose)
admin.site.register(AccumIntegratedProjRadiogDose)
admin.site.register(PatientModuleAttr)
admin.site.register(GeneralEquipmentModuleAttr)
admin.site.register(PatientStudyModuleAttr)
admin.site.register(ContextID)
admin.site.register(CtRadiationDose)
admin.site.register(CtAccumulatedDoseData)
admin.site.register(CtIrradiationEventData)
admin.site.register(ScanningLength)
admin.site.register(CtDoseCheckDetails)
admin.site.register(CtXRaySourceParameters)
admin.site.register(Exports)
admin.site.register(SizeUpload)
admin.site.register(UniqueEquipmentNames)
admin.site.register(DicomStoreSCP)
admin.site.register(DicomRemoteQR)
admin.site.register(DicomDeleteSettings)
admin.site.register(DicomQuery)
admin.site.register(DicomQRRspStudy)
admin.site.register(DicomQRRspSeries)
admin.site.register(DicomQRRspImage)

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from remapp.models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.site_url = "/openrem/"
