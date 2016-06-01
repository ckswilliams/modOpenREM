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
..  module:: models.
    :synopsis: Models to create the database tables and relationships.

..  moduleauthor:: Ed McDonagh

"""

# Following two lines added so that sphinx autodocumentation works. 
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
import json
from django.db import models
from django.core.urlresolvers import reverse
from solo.models import SingletonModel


class SkinDoseMapCalcSettings(SingletonModel):
    enable_skin_dose_maps = models.BooleanField(default=False, verbose_name="Enable skin dose maps?")
    calc_on_import = models.BooleanField(default=True, verbose_name="Calculate skin dose map on import?")

    def get_absolute_url(self):
        return '/admin/skindosemapsettings/1/'


class DicomDeleteSettings(SingletonModel):
    del_no_match = models.BooleanField(default=False,
                    verbose_name="delete objects that don't match any import functions?")
    del_rdsr = models.BooleanField(default=False,
                   verbose_name="delete radiation dose structured reports after processing?")
    del_mg_im = models.BooleanField(default=False,
                    verbose_name="delete mammography images after processing?")
    del_dx_im = models.BooleanField(default=False,
                    verbose_name="delete radiography images after processing?")
    del_ct_phil = models.BooleanField(default=False,
                    verbose_name="delete Philips CT dose info images after processing?")

    def __unicode__(self):
        return u"Delete DICOM objects settings"

    class Meta:
        verbose_name = "Delete DICOM objects settings"

    def get_absolute_url(self):
        return reverse('dicom_summary')

class PatientIDSettings(SingletonModel):
    name_stored = models.BooleanField(default=False)
    name_hashed = models.BooleanField(default=True)
    id_stored = models.BooleanField(default=False)
    id_hashed = models.BooleanField(default=True)
    accession_hashed = models.BooleanField(default=False)
    dob_stored = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Patient ID Settings"

    class Meta:
        verbose_name = "Patient ID Settings"

    def get_absolute_url(self):
        return reverse('home')


class DicomStoreSCP(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name="Name of local store node - fewer than 64 characters, spaces allowed")
    aetitle = models.CharField(max_length=16, blank=True, null=True,
                               verbose_name="AE Title of this node - 16 or fewer letters and numbers, no spaces")
    port = models.IntegerField(blank=True, null=True, verbose_name="Port: 104 is standard for DICOM but over 1024 requires fewer admin rights")
    task_id = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)
    run = models.BooleanField(default=False)
    keep_alive = models.BooleanField(default=False, verbose_name="Should this server be kept auto-started and kept alive (using celery beat)")
    controlled = models.BooleanField(default=False, verbose_name="Is this server controlled by OpenREM")

    def get_absolute_url(self):
        return reverse('dicom_summary')


class DicomRemoteQR(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name="Name of QR node - fewer than 64 characters, spaces allowed")
    aetitle = models.CharField(max_length=16, blank=True, null=True,
                               verbose_name="AE Title of the remote node - 16 or fewer letters and numbers, no spaces")
    port = models.IntegerField(blank=True, null=True, verbose_name="Remote port")
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="Remote IP address")
    hostname = models.CharField(max_length=32, blank=True, null=True, verbose_name="Or remote hostname")
    callingaet = models.CharField(max_length=16, blank=True, null=True,
                                  verbose_name="AE Title of this OpenREM server - 16 or fewer letters and numbers, no spaces")
    enabled = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('dicom_summary')

    def __unicode__(self):
        return self.name


class DicomQuery(models.Model):
    complete = models.BooleanField(default=False)
    query_id = models.CharField(max_length=64)
    failed = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    stage = models.TextField(blank=True, null=True)
    qr_scp_fk = models.ForeignKey(DicomRemoteQR, blank=True, null=True)
    store_scp_fk = models.ForeignKey(DicomStoreSCP, blank=True, null=True)
    move_complete = models.BooleanField(default=False)


class DicomQRRspStudy(models.Model):
    dicom_query = models.ForeignKey(DicomQuery)
    query_id = models.CharField(max_length=64)
    study_instance_uid = models.TextField(blank=True, null=True)
    modality = models.CharField(max_length=16, blank=True, null=True)
    modalities_in_study = models.CharField(max_length=100, blank=True, null=True)
    study_description = models.TextField(blank=True, null=True)
    number_of_study_related_series = models.IntegerField(blank=True, null=True)

    def set_modalities_in_study(self, x):
        self.modalities_in_study = json.dumps(x)

    def get_modalities_in_study(self):
        return json.loads(self.modalities_in_study)


class DicomQRRspSeries(models.Model):
    dicom_qr_rsp_study = models.ForeignKey(DicomQRRspStudy)
    query_id = models.CharField(max_length=64)
    series_instance_uid = models.TextField(blank=True, null=True)
    series_number = models.IntegerField(blank=True, null=True)
    modality = models.CharField(max_length=16, blank=True, null=True)
    series_description = models.TextField(blank=True, null=True)
    number_of_series_related_instances = models.IntegerField(blank=True, null=True)


class DicomQRRspImage(models.Model):
    dicom_qr_rsp_series = models.ForeignKey(DicomQRRspSeries)
    query_id = models.CharField(max_length=64)
    sop_instance_uid = models.TextField(blank=True, null=True)
    instance_number = models.IntegerField(blank=True, null=True)
    sop_class_uid = models.TextField(blank=True, null=True)


from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    YEARS = 'years'
    TIME_PERIOD = (
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
        (MONTHS, 'Months'),
        (YEARS, 'Years'),
    )

    MEAN = 'mean'
    MEDIAN = 'median'
    BOTH = 'both'
    AVERAGES = (
        (MEAN, 'mean'),
        (MEDIAN, 'median'),
        (BOTH, 'both'),
    )

    DLP = 'dlp'
    CTDI = 'ctdi'
    FREQ = 'freq'
    NAME = 'name'
    SORTING_CHOICES_CT = (
        (DLP, 'DLP'),
        (CTDI, 'CTDI'),
        (FREQ, 'Frequency'),
        (NAME, 'Name'),
    )

    DAP = 'dap'
    SORTING_CHOICES_DX = (
        (DAP, 'DAP'),
        (FREQ, 'Frequency'),
        (NAME, 'Name'),
    )

    ASCENDING = 1
    DESCENDING = -1
    SORTING_DIRECTION = (
        (ASCENDING, 'Ascending'),
        (DESCENDING, 'Descending'),
    )

    # This field is required.
    user = models.OneToOneField(User)

    # Flag to set whether median calculations can be carried out
    median_available = models.BooleanField(default=False,
                                           editable=False)

    plotAverageChoice = models.CharField(max_length=6,
                                         choices=AVERAGES,
                                         default=MEAN)

    plotInitialSortingDirection = models.IntegerField(null=True,
                                                      choices=SORTING_DIRECTION,
                                                      default=DESCENDING)

    # Plotting controls
    plotCharts = models.BooleanField(default=False)
    plotDXAcquisitionMeanDAP = models.BooleanField(default=True)
    plotDXAcquisitionFreq = models.BooleanField(default=False)
    plotDXStudyMeanDAP = models.BooleanField(default=True)
    plotDXStudyFreq = models.BooleanField(default=True)
    plotDXRequestMeanDAP = models.BooleanField(default=True)
    plotDXRequestFreq = models.BooleanField(default=True)
    plotDXAcquisitionMeankVp = models.BooleanField(default=False)
    plotDXAcquisitionMeanmAs = models.BooleanField(default=False)
    plotDXStudyPerDayAndHour = models.BooleanField(default=False)
    plotDXAcquisitionMeankVpOverTime = models.BooleanField(default=False)
    plotDXAcquisitionMeanmAsOverTime = models.BooleanField(default=False)
    plotDXAcquisitionMeanDAPOverTime = models.BooleanField(default=False)
    plotDXAcquisitionMeanDAPOverTimePeriod = models.CharField(max_length=6,
                                                              choices=TIME_PERIOD,
                                                              default=MONTHS)
    plotDXInitialSortingChoice = models.CharField(max_length=4,
                                                  choices=SORTING_CHOICES_DX,
                                                  default=FREQ)

    plotCTAcquisitionMeanDLP = models.BooleanField(default=True)
    plotCTAcquisitionMeanCTDI = models.BooleanField(default=True)
    plotCTAcquisitionFreq = models.BooleanField(default=False)
    plotCTStudyMeanDLP = models.BooleanField(default=True)
    plotCTStudyMeanCTDI = models.BooleanField(default=True)
    plotCTStudyFreq = models.BooleanField(default=False)
    plotCTRequestMeanDLP = models.BooleanField(default=False)
    plotCTRequestFreq = models.BooleanField(default=False)
    plotCTStudyPerDayAndHour = models.BooleanField(default=False)
    plotCTStudyMeanDLPOverTime = models.BooleanField(default=False)
    plotCTStudyMeanDLPOverTimePeriod = models.CharField(max_length=6,
                                                        choices=TIME_PERIOD,
                                                        default=MONTHS)
    plotCTInitialSortingChoice = models.CharField(max_length=4,
                                                  choices=SORTING_CHOICES_CT,
                                                  default=FREQ)

    plotRFStudyPerDayAndHour = models.BooleanField(default=False)
    plotRFStudyFreq = models.BooleanField(default=False)
    plotRFStudyDAP = models.BooleanField(default=True)
    plotRFInitialSortingChoice = models.CharField(max_length=4,
                                                  choices=SORTING_CHOICES_DX,
                                                  default=FREQ)

    plotMGStudyPerDayAndHour = models.BooleanField(default=False)
    plotMGAGDvsThickness = models.BooleanField(default=False)

    displayCT = models.BooleanField(default=True)
    displayRF = models.BooleanField(default=True)
    displayMG = models.BooleanField(default=True)
    displayDX = models.BooleanField(default=True)

    plotSeriesPerSystem = models.BooleanField(default=False)

    plotHistogramBins = models.PositiveSmallIntegerField(default=20)

    plotHistograms = models.BooleanField(default=False)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class UniqueEquipmentNames(models.Model):
    manufacturer = models.TextField(blank=True, null=True)
    manufacturer_hash = models.CharField(max_length=64, blank=True, null=True)
    institution_name = models.TextField(blank=True, null=True)
    institution_name_hash = models.CharField(max_length=64, blank=True, null=True)
    station_name = models.CharField(max_length=32, blank=True, null=True)
    station_name_hash = models.CharField(max_length=64, blank=True, null=True)
    institutional_department_name = models.TextField(blank=True, null=True)
    institutional_department_name_hash = models.CharField(max_length=64, blank=True, null=True)
    manufacturer_model_name = models.TextField(blank=True, null=True)
    manufacturer_model_name_hash = models.CharField(max_length=64, blank=True, null=True)
    device_serial_number = models.TextField(blank=True, null=True)
    device_serial_number_hash = models.CharField(max_length=64, blank=True, null=True)
    software_versions = models.TextField(blank=True, null=True)
    software_versions_hash = models.CharField(max_length=64, blank=True, null=True)
    gantry_id = models.TextField(blank=True, null=True)
    gantry_id_hash = models.CharField(max_length=64, blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)
    hash_generated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('manufacturer_hash', 'institution_name_hash', 'station_name_hash',
                           'institutional_department_name_hash', 'manufacturer_model_name_hash',
                           'device_serial_number_hash', 'software_versions_hash', 'gantry_id_hash')

    def __unicode__(self):
        return self.display_name


class SizeUpload(models.Model):
    sizefile = models.FileField(upload_to='sizeupload')
    height_field = models.TextField(blank=True, null=True)
    weight_field = models.TextField(blank=True, null=True)
    id_field = models.TextField(blank=True, null=True)
    id_type = models.TextField(blank=True, null=True)
    task_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    progress = models.TextField(blank=True, null=True)
    num_records = models.IntegerField(blank=True, null=True)
    logfile = models.FileField(upload_to='sizelogs/%Y/%m/%d', null=True)
    import_date = models.DateTimeField(blank=True, null=True)
    processtime = models.FloatField(blank=True, null=True)


class Exports(models.Model):
    """Table to hold the export status and filenames
    """
    task_id = models.TextField()
    filename = models.FileField(upload_to='exports/%Y/%m/%d', null=True)
    status = models.TextField(blank=True, null=True)
    progress = models.TextField(blank=True, null=True)
    modality = models.CharField(max_length=16, blank=True, null=True)
    num_records = models.IntegerField(blank=True, null=True)
    export_type = models.TextField(blank=True, null=True)
    export_date = models.DateTimeField(blank=True, null=True)
    processtime = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    includes_pid = models.BooleanField(default=False)
    export_user = models.ForeignKey(User, blank=True, null=True)


class ContextID(models.Model):
    """Table to hold all the context ID code values and code meanings.

    + Could be prefilled from the tables in DICOM 3.16, but is actually populated as the codes occur. \
    This assumes they are used correctly.
    """
    code_value = models.CharField(max_length=16)
    code_meaning = models.TextField(blank=True, null=True)
    cid_table = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return self.code_meaning

    class Meta:
        ordering = ['code_value']


class GeneralStudyModuleAttr(models.Model):  # C.7.2.1
    """General Study Module C.7.2.1

    Specifies the Attributes that describe and identify the Study
    performed upon the Patient.
    From DICOM Part 3: Information Object Definitions Table C.7-3

    Additional to the module definition:
        * performing_physician_name
        * operator_name
        * modality_type
        * procedure_code_value_and_meaning
        * requested_procedure_code_value_and_meaning
    """
    study_instance_uid = models.TextField(blank=True, null=True)
    study_date = models.DateField(blank=True, null=True)
    study_time = models.TimeField(blank=True, null=True)
    study_workload_chart_time = models.DateTimeField(blank=True, null=True)
    referring_physician_name = models.TextField(blank=True, null=True)
    referring_physician_identification = models.TextField(blank=True, null=True)
    study_id = models.CharField(max_length=16, blank=True, null=True)
    accession_number = models.TextField(blank=True, null=True)
    accession_hashed = models.BooleanField(default=False)
    study_description = models.TextField(blank=True, null=True)
    physician_of_record = models.TextField(blank=True, null=True)
    name_of_physician_reading_study = models.TextField(blank=True, null=True)
    # Possibly need a few sequences linked to this table...
    # Next three don't belong in this table, but they don't belong anywhere in a RDSR!
    performing_physician_name = models.TextField(blank=True, null=True)
    operator_name = models.TextField(blank=True, null=True)
    modality_type = models.CharField(max_length=16, blank=True, null=True)
    procedure_code_value = models.CharField(max_length=16, blank=True, null=True)
    procedure_code_meaning = models.TextField(blank=True, null=True)
    requested_procedure_code_value = models.CharField(max_length=16, blank=True, null=True)
    requested_procedure_code_meaning = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.study_instance_uid


class ProjectionXRayRadiationDose(models.Model):  # TID 10001
    """Projection X-Ray Radiation Dose template TID 10001

    From DICOM Part 16:
        This template defines a container (the root) with subsidiary content items, each of which represents a
        single projection X-Ray irradiation event entry or plane-specific dose accumulations. There is a defined
        recording observer (the system or person responsible for recording the log, generally the system). A
        Biplane irradiation event will be recorded as two individual events, one for each plane. Accumulated
        values will be kept separate for each plane.

    """
    general_study_module_attributes = models.ForeignKey(GeneralStudyModuleAttr)
    procedure_reported = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_procedure')
    has_intent = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_intent')
    acquisition_device_type_cid = models.ForeignKey(ContextID, blank=True, null=True, related_name='tid10001_type')
    scope_of_accumulation = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_scope')
    xray_detector_data_available = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_detector')
    xray_source_data_available = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_source')
    xray_mechanical_data_available = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_mech')
    comment = models.TextField(blank=True, null=True)
    # might need to be a table on its own as is 1-n, even though it should only list the primary source...
    source_of_dose_information = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10001_infosource')


class AccumXRayDose(models.Model):  # TID 10002
    """Accumulated X-Ray Dose TID 10002

    From DICOM Part 16:
        This general template provides detailed information on projection X-Ray dose value accumulations over
        several irradiation events from the same equipment (typically a study or a performed procedure step).

    """
    projection_xray_radiation_dose = models.ForeignKey(ProjectionXRayRadiationDose)
    acquisition_plane = models.ForeignKey(ContextID, blank=True, null=True)


class Calibration(models.Model):
    """Table to hold the calibration information

    + Container in TID 10002 Accumulated X-ray dose

    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose)
    dose_measurement_device = models.ForeignKey(ContextID, blank=True, null=True)
    calibration_date = models.DateTimeField(blank=True, null=True)
    calibration_factor = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    calibration_uncertainty = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    calibration_responsible_party = models.TextField(blank=True, null=True)


class IrradEventXRayData(models.Model):  # TID 10003
    """Irradiation Event X-Ray Data TID 10003

    From DICOM part 16:
        This template conveys the dose and equipment parameters of a single irradiation event.

    """
    projection_xray_radiation_dose = models.ForeignKey(ProjectionXRayRadiationDose)
    acquisition_plane = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_plane')  # CID 10003
    irradiation_event_uid = models.TextField(blank=True, null=True)
    irradiation_event_label = models.TextField(blank=True, null=True)
    label_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_labeltype')  # CID 10022
    date_time_started = models.DateTimeField(blank=True, null=True)
    irradiation_event_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_eventtype')  # CID 10002
    acquisition_protocol = models.TextField(blank=True, null=True)
    anatomical_structure = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_anatomy')  # CID 4009
    laterality = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_laterality')  # CID 244
    image_view = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_view'
    )  # CID 4010 "DX View" or CID 4014 "View for Mammography"
    # Lines below are incorrect, but exist in current databases. Replace with lines below them:
    projection_eponymous_name = models.CharField(max_length=16, blank=True, null=True)  # Added null to originals
    patient_table_relationship = models.CharField(max_length=16, blank=True, null=True)
    patient_orientation = models.CharField(max_length=16, blank=True, null=True)
    patient_orientation_modifier = models.CharField(max_length=16, blank=True, null=True)
    # TODO: Projection Eponymous Name should be in ImageViewModifier, not here :-(
    projection_eponymous_name_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_pojectioneponymous')  # CID 4012
    patient_table_relationship_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_pttablerel')  # CID 21
    patient_orientation_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_ptorientation')  # CID 19
    patient_orientation_modifier_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_ptorientationmod')  # CID 20
    target_region = models.ForeignKey(
        ContextID, blank=True, null=True, related_name="tid10003_region")  # CID 4031
    dose_area_product = models.DecimalField(max_digits=16, decimal_places=10, blank=True, null=True)
    half_value_layer = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    patient_equivalent_thickness = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    entrance_exposure_at_rp = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    reference_point_definition_text = models.TextField(blank=True, null=True) # in other models the code version is _code
    reference_point_definition = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_rpdefinition')  # CID 10025
    # Another char field that should be a cid
    breast_composition = models.CharField(max_length=16, blank=True, null=True)  # TID 4007, CID 6000
    breast_composition_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003_breastcomposition')  # CID 6000/6001
    percent_fibroglandular_tissue = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)  # TID 4007
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.irradiation_event_uid

    def convert_gym2_to_cgycm2(self):
        if self.dose_area_product:
            return 1000000*self.dose_area_product


class ImageViewModifier(models.Model):  # EV 111032
    """Table to hold image view modifiers for the irradiation event x-ray data table

    From DICOM Part 16 Annex D DICOM controlled Terminology Definitions
        + Code Value 111032
        + Code Meaning Image View Modifier
        + Code Definition Modifier for image view
    """
    irradiation_event_xray_data = models.ForeignKey(IrradEventXRayData)
    image_view_modifier = models.ForeignKey(
        ContextID, blank=True, null=True
    )  # CID 4011 "DX View Modifier" or CID 4015 "View Modifier for Mammography"
    # TODO: Add Projection Eponymous Name


class IrradEventXRayDetectorData(models.Model):  # TID 10003a
    """Irradiation Event X-Ray Detector Data TID 10003a

    From DICOM Part 16 Correction Proposal CP-1077:
        This template contains data which is expected to be available to the X-ray detector or plate reader component of
        the equipment.
    """
    irradiation_event_xray_data = models.ForeignKey(IrradEventXRayData)
    exposure_index = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    target_exposure_index = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    deviation_index = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # New fields added to record the non-IEC exposure index from CR/DX image headers
    relative_xray_exposure = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    relative_exposure_unit = models.CharField(max_length=16, blank=True, null=True)
    sensitivity = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class IrradEventXRaySourceData(models.Model):  # TID 10003b
    """Irradiation Event X-Ray Source Data TID 10003b

    From DICOM Part 16 Correction Proposal CP-1077:
        This template contains data which is expected to be available to the X-ray source component of the equipment.

    Additional to the template:
        * ii_field_size
        * exposure_control_mode
        * grid information over and above grid type
    """
    irradiation_event_xray_data = models.ForeignKey(IrradEventXRayData)
    dose_rp = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    reference_point_definition = models.TextField(blank=True, null=True)
    reference_point_definition_code = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003b_rpdefinition')  # CID 10025
    average_glandular_dose = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    fluoro_mode = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003b_fluoromode')  # CID 10004
    pulse_rate = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    number_of_pulses = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    # derivation should be a cid - has never been used in extractor, but was non null=True so will exist in database :-(
    derivation = models.CharField(max_length=16, blank=True, null=True)
    derivation_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003b_derivation')  # R-10260, "Estimated"
    irradiation_duration = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    average_xray_tube_current = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    exposure_time = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    focal_spot_size = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    anode_target_material = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10003b_anodetarget')  # CID 10016
    collimated_field_area = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    collimated_field_height = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    collimated_field_width = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # not in DICOM standard - 'image intensifier' field size and exposure control mode
    ii_field_size = models.IntegerField(blank=True, null=True)
    exposure_control_mode = models.CharField(max_length=16, blank=True, null=True)
    grid_absorbing_material = models.TextField(blank=True, null=True)
    grid_spacing_material = models.TextField(blank=True, null=True)
    grid_thickness = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    grid_pitch = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    grid_aspect_ratio = models.TextField(blank=True, null=True)
    grid_period = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)
    grid_focal_distance = models.DecimalField(max_digits=16, decimal_places=6, blank=True, null=True)


class XrayGrid(models.Model):
    """Content ID 10017 X-Ray Grid

    From DICOM Part 16
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    xray_grid = models.ForeignKey(ContextID, blank=True, null=True)  # CID 10017


class PulseWidth(models.Model):  # EV 113793
    """In TID 10003b. Code value 113793 (ms)
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    pulse_width = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class Kvp(models.Model):  # EV 113733
    """In TID 10003b. Code value 113733 (kV)
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    kvp = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class XrayTubeCurrent(models.Model):  # EV 113734
    """In TID 10003b. Code value 113734 (mA)
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    xray_tube_current = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class Exposure(models.Model):  # EV 113736
    """In TID 10003b. Code value 113736 (uAs)
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    exposure = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)

    def convert_uAs_to_mAs(self):
        """Converts uAs to mAs for display in web interface
        """
        if self.exposure:
            return self.exposure / 1000


class XrayFilters(models.Model):  # EV 113771
    """Container in TID 10003b. Code value 113771
    """
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData)
    xray_filter_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='xrayfilters_type')  # CID 10007
    xray_filter_material = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='xrayfilters_material')  # CID 10006
    xray_filter_thickness_minimum = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    xray_filter_thickness_maximum = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class IrradEventXRayMechanicalData(models.Model):  # TID 10003c
    """Irradiation Event X-Ray Mechanical Data TID 10003c

    From DICOM Part 16 Correction Proposal CP-1077:
        This template contains data which is expected to be available to the gantry or mechanical component of the
        equipment.

    Additional to the template:
        * compression_force
        * magnification_factor
    """
    irradiation_event_xray_data = models.ForeignKey(IrradEventXRayData)
    crdr_mechanical_configuration = models.ForeignKey(ContextID, blank=True, null=True)
    positioner_primary_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    positioner_secondary_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    positioner_primary_end_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    positioner_secondary_end_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    column_angulation = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_head_tilt_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_horizontal_rotation_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_cradle_tilt_angle = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    compression_thickness = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # not in DICOM standard - compression force in N
    compression_force = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    magnification_factor = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class DoseRelatedDistanceMeasurements(models.Model):  # CID 10008
    """Dose Related Distance Measurements Context ID 10008

    Called from TID 10003c
    """
    irradiation_event_xray_mechanical_data = models.ForeignKey(IrradEventXRayMechanicalData)
    distance_source_to_isocenter = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    distance_source_to_reference_point = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    distance_source_to_detector = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_longitudinal_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_lateral_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_height_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    distance_source_to_table_plane = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_longitudinal_end_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_lateral_end_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    table_height_end_position = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # not in DICOM standard - distance source to entrance surface distance in mm
    distance_source_to_entrance_surface = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    radiological_thickness = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class AccumProjXRayDose(models.Model):  # TID 10004
    """Accumulated Fluoroscopy and Acquisition Projection X-Ray Dose TID 10004

    From DICOM Part 16:
        This general template provides detailed information on projection X-Ray dose value accumulations over
        several irradiation events from the same equipment (typically a study or a performed procedure step).

    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose)
    fluoro_dose_area_product_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    fluoro_dose_rp_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    total_fluoro_time = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    acquisition_dose_area_product_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    acquisition_dose_rp_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    total_acquisition_time = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # The following fields should not be in this table, and are duplicated in the
    # AccumCassetteBsdProjRadiogDose and AccumIntegratedProjRadiogDose
    # tables below.
    # TODO: Ensure rdsr.py and dx.py use the other table and do not populate this one any further.
    dose_area_product_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    dose_rp_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    total_number_of_radiographic_frames  = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    reference_point_definition = models.TextField(blank=True, null=True)
    reference_point_definition_code = models.ForeignKey(ContextID, blank=True, null=True)


class AccumMammographyXRayDose(models.Model):  # TID 10005
    """Accumulated Mammography X-Ray Dose TID 10005

    From DICOM Part 16:
        This modality specific template provides detailed information on mammography X-Ray dose value
        accumulations over several irradiation events from the same equipment (typically a study or a performed
        procedure step).
    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose)
    accumulated_average_glandular_dose = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    laterality = models.ForeignKey(ContextID, blank=True, null=True)


class AccumCassetteBsdProjRadiogDose(models.Model):  # TID 10006
    """Accumulated Cassette-based Projection Radiography Dose TID 10006

    From DICOM Part 16 Correction Proposal CP-1077:
        This template provides information on Projection Radiography dose values accumulated on Cassette-
        based systems over one or more irradiation events (typically a study or a performed procedure step) from
        the same equipment.
    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose)
    detector_type = models.ForeignKey(ContextID, blank=True, null=True)
    total_number_of_radiographic_frames = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)


class AccumIntegratedProjRadiogDose(models.Model):  # TID 10007
    """Accumulated Integrated Projection Radiography Dose TID 10007

    From DICOM Part 16 Correction Proposal CP-1077:
        This template provides information on Projection Radiography dose values accumulated on Integrated
        systems over one or more irradiation events (typically a study or a performed procedure step) from the
        same equipment.
    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose)
    dose_area_product_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    dose_rp_total = models.DecimalField(max_digits=16, decimal_places=12, blank=True, null=True)
    total_number_of_radiographic_frames = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    reference_point_definition_code = models.ForeignKey(ContextID, blank=True, null=True)
    reference_point_definition = models.TextField(blank=True, null=True)

    def convert_gym2_to_cgycm2(self):
        """Converts Gy.m2 to cGy.cm2 for display in web interface
        """
        if self.dose_area_product_total:
            return 1000000*self.dose_area_product_total


class PatientModuleAttr(models.Model):  # C.7.1.1
    """Patient Module C.7.1.1

    From DICOM Part 3: Information Object Definitions Table C.7-1:
        Specifies the Attributes of the Patient that describe and identify the Patient who is
        the subject of a diagnostic Study. This Module contains Attributes of the patient that are needed
        for diagnostic interpretation of the Image and are common for all studies performed on the
        patient. It contains Attributes that are also included in the Patient Modules in Section C.2.
    """
    general_study_module_attributes = models.ForeignKey(GeneralStudyModuleAttr)
    patient_name = models.TextField(blank=True, null=True)
    name_hashed = models.BooleanField(default=False)
    patient_id = models.TextField(blank=True, null=True)
    id_hashed = models.BooleanField(default=False)
    patient_birth_date = models.DateField(blank=True, null=True)
    patient_sex = models.CharField(max_length=2, blank=True, null=True)
    other_patient_ids = models.TextField(blank=True, null=True)
    not_patient_indicator = models.TextField(blank=True, null=True)


class PatientStudyModuleAttr(models.Model):  # C.7.2.2
    """Patient Study Module C.7.2.2

    From DICOM Part 3: Information Object Definitions Table C.7-4a:
        Defines Attributes that provide information about the Patient at the time the Study
        started.
    """
    general_study_module_attributes = models.ForeignKey(GeneralStudyModuleAttr)
    admitting_diagnosis_description = models.TextField(blank=True, null=True)
    admitting_diagnosis_code_sequence = models.TextField(blank=True, null=True)
    patient_age = models.CharField(max_length=4, blank=True, null=True)
    patient_age_decimal = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    patient_size = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    patient_weight = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # TODO: Add patient size code sequence


class GeneralEquipmentModuleAttr(models.Model):  # C.7.5.1
    """General Equipment Module C.7.5.1

    From DICOM Part 3: Information Object Definitions Table C.7-8:
        Specifies the Attributes that identify and describe the piece of equipment that
        produced a Series of Composite Instances.
    """
    general_study_module_attributes = models.ForeignKey(GeneralStudyModuleAttr)
    manufacturer = models.TextField(blank=True, null=True)
    institution_name = models.TextField(blank=True, null=True)
    institution_address = models.TextField(blank=True, null=True)
    station_name = models.CharField(max_length=32, blank=True, null=True)
    institutional_department_name = models.TextField(blank=True, null=True)
    manufacturer_model_name = models.TextField(blank=True, null=True)
    device_serial_number = models.TextField(blank=True, null=True)
    software_versions = models.TextField(blank=True, null=True)
    gantry_id = models.TextField(blank=True, null=True)
    spatial_resolution = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    date_of_last_calibration = models.DateTimeField(blank=True, null=True)
    time_of_last_calibration = models.DateTimeField(blank=True, null=True)
    unique_equipment_name = models.ForeignKey(UniqueEquipmentNames, null=True)

    def __unicode__(self):
        return self.station_name


# CT

class CtRadiationDose(models.Model):  # TID 10011
    """CT Radiation Dose TID 10011

    From DICOM Part 16:
        This template defines a container (the root) with subsidiary content items, each of which corresponds to a
        single CT X-Ray irradiation event entry. There is a defined recording observer (the system or person
        responsible for recording the log, generally the system). Accumulated values shall be kept for a whole
        Study or at least a part of a Study, if the Study is divided in the workflow of the examination, or a
        performed procedure step. Multiple CT Radiation Dose objects may be created for one Study.
    """
    general_study_module_attributes = models.ForeignKey(GeneralStudyModuleAttr)
    procedure_reported = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10011_procedure')
    has_intent = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10011_intent')  # CID 3629
    start_of_xray_irradiation = models.DateTimeField(blank=True, null=True)
    end_of_xray_irradiation = models.DateTimeField(blank=True, null=True)
    scope_of_accumulation = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10011_scope')  # CID 10000
    uid_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1011_uid')  # CID 10001
    comment = models.TextField(blank=True, null=True)
    # does need to be a table on its own as is 1-n
    source_of_dose_information = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10011_source')


class SourceOfCTDoseInformation(models.Model):  # CID 10021
    """Source of CT Dose Information
    """
    # TODO: populate this table when extracting and move existing data. Task #164
    ct_radiation_dose = models.ForeignKey(CtRadiationDose)
    source_of_dose_information = models.ForeignKey(
        ContextID, blank=True, null=True)  # CID 10021


class CtAccumulatedDoseData(models.Model):  # TID 10012
    """CT Accumulated Dose Data

    From DICOM Part 16:
        This general template provides detailed information on CT X-Ray dose value accumulations over several
        irradiation events from the same equipment and over the scope of accumulation specified for the report
        (typically a Study or a Performed Procedure Step).
    """
    ct_radiation_dose = models.ForeignKey(CtRadiationDose)
    total_number_of_irradiation_events = models.DecimalField(max_digits=16, decimal_places=0, blank=True, null=True)
    ct_dose_length_product_total = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    ct_effective_dose_total = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    reference_authority_code = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10012_authority')  # CID 10015 (ICRP60/103)
    reference_authority_text = models.TextField(blank=True, null=True)
    measurement_method = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10012_method')  # CID 10011
    patient_model = models.TextField(blank=True, null=True)
    effective_dose_phantom_type = models.TextField(blank=True, null=True)
    dosimeter_type = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class CtIrradiationEventData(models.Model):  # TID 10013
    """CT Irradiation Event Data TID 10013

    From DICOM Part 16:
        This template conveys the dose and equipment parameters of a single irradiation event.

    Additional to the template:
        + date_time_started
        + series_description
    """
    ct_radiation_dose = models.ForeignKey(CtRadiationDose)
    acquisition_protocol = models.TextField(blank=True, null=True)
    target_region = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_region')  # CID 4030
    ct_acquisition_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_type')  # CID 10013
    procedure_context = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_context')  # CID 10014
    irradiation_event_uid = models.TextField(blank=True, null=True)
    #  TODO: Add extraction of the label and label type (Series, acquisition, instance number) Issue #167
    irradiation_event_label = models.TextField(blank=True, null=True)
    label_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_labeltype')  # CID 10022
    exposure_time = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    nominal_single_collimation_width = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    nominal_total_collimation_width = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    pitch_factor = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    number_of_xray_sources = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    mean_ctdivol = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    ctdiw_phantom_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_phantom')  # CID 4052
    ctdifreeair_calculation_factor = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    mean_ctdifreeair = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    dlp = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    effective_dose = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    measurement_method = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid10013_method')  # CID 10011
    effective_dose_conversion_factor = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    xray_modulation_type = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # Not in DICOM standard:
    date_time_started = models.DateTimeField(blank=True, null=True)
    series_description = models.TextField(blank=True, null=True)


class CtReconstructionAlgorithm(models.Model):
    """Container in TID 10013 to hold CT reconstruction methods
    """
    # TODO: Add this to the rdsr extraction routines. Issue #166
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData)
    reconstruction_algorithm = models.ForeignKey(ContextID, blank=True, null=True)  # CID 10033


class CtXRaySourceParameters(models.Model):
    """Container in TID 10013 to hold CT x-ray source parameters
    """
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData)
    identification_of_the_xray_source = models.TextField(blank=True, null=True)
    kvp = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    maximum_xray_tube_current = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    xray_tube_current = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    exposure_time_per_rotation = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    xray_filter_aluminum_equivalent = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class ScanningLength(models.Model):  # TID 10014
    """Scanning Length TID 10014

    From DICOM Part 16:
        No description
    """
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData)
    scanning_length = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    length_of_reconstructable_volume = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    exposed_range = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    top_z_location_of_reconstructable_volume = models.DecimalField(
        max_digits=16, decimal_places=8, blank=True, null=True)
    bottom_z_location_of_reconstructable_volume = models.DecimalField(
        max_digits=16, decimal_places=8, blank=True, null=True)
    top_z_location_of_scanning_length = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    bottom_z_location_of_scanning_length = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    frame_of_reference_uid = models.TextField(blank=True, null=True)


class SizeSpecificDoseEstimation(models.Model):
    """Container in TID 10013 to hold size specific dose estimation details
    """
    # TODO: Add this to the rdsr extraction routines. Issue #168
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData)
    measurement_method = models.ForeignKey(ContextID, blank=True, null=True)  # CID 10023
    measured_lateral_dimension = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    measured_ap_dimension = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    derived_effective_diameter = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)


class CtDoseCheckDetails(models.Model):  # TID 10015
    """CT Dose Check Details TID 10015

    From DICOM Part 16:
        This template records details related to the use of the NEMA Dose Check Standard (NEMA XR-25-2010).
    """
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData)
    dlp_alert_value_configured = models.NullBooleanField()
    ctdivol_alert_value_configured = models.NullBooleanField()
    dlp_alert_value = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    ctdivol_alert_value = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    accumulated_dlp_forward_estimate = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    accumulated_ctdivol_forward_estimate = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    # alert_ added to allow two fields that are in different containers in std
    alert_reason_for_proceeding = models.TextField(blank=True, null=True)
    dlp_notification_value_configured = models.NullBooleanField()
    ctdivol_notification_value_configured = models.NullBooleanField()
    dlp_notification_value = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    ctdivol_notification_value = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    dlp_forward_estimate = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    ctdivol_forward_estimate = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    # notification_ added to allow two fields that are in different containers in std
    notification_reason_for_proceeding = models.TextField(blank=True, null=True)


# Models common to both

class ObserverContext(models.Model):  # TID 1002
    """Observer Context TID 1002

    From DICOM Part 16:
        The observer (person or device) that created the Content Items to which this context applies.
    """
    projection_xray_radiation_dose = models.ForeignKey(ProjectionXRayRadiationDose, blank=True, null=True)
    ct_radiation_dose = models.ForeignKey(CtRadiationDose, blank=True, null=True)
    observer_type = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1002_observertype')  # CID 270
    person_observer_name = models.TextField(blank=True, null=True)
    person_observer_organization_name = models.TextField(blank=True, null=True)
    person_observer_role_in_organization = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1002_ptroleorg')  # CID 7452
    person_observer_role_in_procedure = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1002_ptroleproc')  # CID 7453
    device_observer_uid = models.TextField(blank=True, null=True)
    device_observer_name = models.TextField(blank=True, null=True)
    device_observer_manufacturer = models.TextField(blank=True, null=True)
    device_observer_model_name = models.TextField(blank=True, null=True)
    device_observer_serial_number = models.TextField(blank=True, null=True)
    device_observer_physical_location_during_observation = models.TextField(blank=True, null=True)
    device_role_in_procedure = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1002_role')  # CID 7445

    def __unicode__(self):
        return self.device_observer_name


class DeviceParticipant(models.Model):  # TID 1021
    """Device Participant TID 1021

    From DICOM Part 16:
        This template describes a device participating in an activity as other than an observer or subject. E.g. for
        a dose report documenting an irradiating procedure, participants include the irradiating device.
    """
    accumulated_xray_dose = models.ForeignKey(AccumXRayDose, blank=True, null=True)
    irradiation_event_xray_detector_data = models.ForeignKey(IrradEventXRayDetectorData, blank=True, null=True)
    irradiation_event_xray_source_data = models.ForeignKey(IrradEventXRaySourceData, blank=True, null=True)
    ct_accumulated_dose_data = models.ForeignKey(CtAccumulatedDoseData, blank=True, null=True)
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData, blank=True, null=True)
    device_role_in_procedure = models.ForeignKey(ContextID, blank=True, null=True)
    device_name = models.TextField(blank=True, null=True)
    device_manufacturer = models.TextField(blank=True, null=True)
    device_model_name = models.TextField(blank=True, null=True)
    device_serial_number = models.TextField(blank=True, null=True)
    device_observer_uid = models.TextField(blank=True, null=True)


class PersonParticipant(models.Model):  # TID 1020
    """Person Participant TID 1020

    From DICOM Part 16:
        This template describes a person participating in an activity as other than an observer or subject. E.g. for
        a dose report documenting an irradiating procedure, participants include the person administering the
        irradiation and the person authorizing the irradiation.
    """
    projection_xray_radiation_dose = models.ForeignKey(ProjectionXRayRadiationDose, blank=True, null=True)
    ct_radiation_dose = models.ForeignKey(CtRadiationDose, blank=True, null=True)
    irradiation_event_xray_data = models.ForeignKey(IrradEventXRayData, blank=True, null=True)
    ct_accumulated_dose_data = models.ForeignKey(CtAccumulatedDoseData, blank=True, null=True)
    ct_irradiation_event_data = models.ForeignKey(CtIrradiationEventData, blank=True, null=True)
    ct_dose_check_details_alert = models.ForeignKey(
        CtDoseCheckDetails, blank=True, null=True, related_name='tid1020_alert')
    ct_dose_check_details_notification = models.ForeignKey(
        CtDoseCheckDetails, blank=True, null=True, related_name='tid1020_notification')
    person_name = models.TextField(blank=True, null=True)
    # CharField version is a mistake and shouldn't be used
    person_role_in_procedure = models.CharField(max_length=16, blank=True)
    person_role_in_procedure_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1020_roleproc')
    person_id = models.TextField(blank=True, null=True)
    person_id_issuer = models.TextField(blank=True, null=True)
    organization_name = models.TextField(blank=True, null=True)
    # TextField version is a mistake and shouldn't be used
    person_role_in_organization = models.TextField(blank=True, null=True)
    person_role_in_organization_cid = models.ForeignKey(
        ContextID, blank=True, null=True, related_name='tid1020_roleorg')  # CID 7452

    def __unicode__(self):
        return self.person_name


from django.db.models.sql.aggregates import Aggregate as SQLAggregate

class MedianSQL(SQLAggregate):
    sql_function = 'Median'
    sql_template = '%(function)s(%(field)s)'
    is_ordinal = True


class Median(models.Aggregate):
    name = 'Median'
    sql = MedianSQL

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = self.sql(col, **self.extra)
        query.aggregates[alias] = aggregate
