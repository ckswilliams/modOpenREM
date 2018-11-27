from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, PrependedText, InlineCheckboxes, Accordion, AccordionGroup
import logging
from openremproject import settings
from remapp.models import DicomDeleteSettings, DicomRemoteQR, DicomStoreSCP, SkinDoseMapCalcSettings, \
    NotPatientIndicatorsName, NotPatientIndicatorsID, HighDoseMetricAlertSettings

logger = logging.getLogger()

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
    (MEAN, 'Mean'),
    (MEDIAN, 'Median'),
    (BOTH, 'Both'),
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
    (DAP, 'DAP or kVp or mAs'),
    (FREQ, 'Frequency'),
    (NAME, 'Name'),
)

ASCENDING = 1
DESCENDING = -1
SORTING_DIRECTION = (
    (ASCENDING, 'Ascending'),
    (DESCENDING, 'Descending'),
)

ITEMS_PER_PAGE = (
    (10, '10'),
    (25, '25'),
    (50, '50'),
    (100, '100'),
    (200, '200'),
    (400, '400'),
)


class SizeUploadForm(forms.Form):
    """Form for patient size csv file upload
    """
    sizefile = forms.FileField(
        label='Select a file'
    )


class SizeHeadersForm(forms.Form):
    """Form for csv column header patient size imports through the web interface
    """

    height_field = forms.ChoiceField(choices='')
    weight_field = forms.ChoiceField(choices='')
    id_field = forms.ChoiceField(choices='')
    id_type = forms.ChoiceField(choices='')

    def __init__(self, my_choice=None, **kwargs):
        super(SizeHeadersForm, self).__init__(**kwargs)
        if my_choice:
            self.fields['height_field'] = forms.ChoiceField(
                choices=my_choice, widget=forms.Select(attrs={"class": "form-control"}))
            self.fields['weight_field'] = forms.ChoiceField(
                choices=my_choice, widget=forms.Select(attrs={"class": "form-control"}))
            self.fields['id_field'] = forms.ChoiceField(
                choices=my_choice, widget=forms.Select(attrs={"class": "form-control"}))
            ID_TYPES = (("acc-no", "Accession Number"), ("si-uid", "Study instance UID"))
            self.fields['id_type'] = forms.ChoiceField(
                choices=ID_TYPES, widget=forms.Select(attrs={"class": "form-control"}))


class itemsPerPageForm(forms.Form):
    itemsPerPage = forms.ChoiceField(label='Items per page', choices=ITEMS_PER_PAGE, required=False)


class DXChartOptionsForm(forms.Form):
    """Form for DX chart options
    """
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotDXAcquisitionMeanDAP = forms.BooleanField(label='DAP per acquisition', required=False)
    plotDXAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotDXStudyMeanDAP = forms.BooleanField(label='DAP per study', required=False)
    plotDXStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotDXRequestMeanDAP = forms.BooleanField(label='DAP per requested procedure', required=False)
    plotDXRequestFreq = forms.BooleanField(label='Requested procedure frequency', required=False)
    plotDXAcquisitionMeankVp = forms.BooleanField(label='kVp per acquisition', required=False)
    plotDXAcquisitionMeanmAs = forms.BooleanField(label='mAs per acquisition', required=False)
    plotDXStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotDXAcquisitionMeankVpOverTime = forms.BooleanField(label='Acquisition kVp over time', required=False)
    plotDXAcquisitionMeanmAsOverTime = forms.BooleanField(label='Acquisition mAs over time', required=False)
    plotDXAcquisitionMeanDAPOverTime = forms.BooleanField(label='Acquisition DAP over time', required=False)
    plotDXAcquisitionMeanDAPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)


class CTChartOptionsForm(forms.Form):
    """Form for CT chart options
    """
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotCTAcquisitionMeanDLP = forms.BooleanField(label='DLP per acquisition', required=False)
    plotCTAcquisitionMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per acquisition'),
                                                   required=False) # nosec
    plotCTAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotCTStudyMeanDLP = forms.BooleanField(label='DLP per study', required=False)
    plotCTStudyMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per study'), required=False)  # nosec
    plotCTStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotCTStudyNumEvents = forms.BooleanField(label='# events per study', required=False)
    plotCTRequestMeanDLP = forms.BooleanField(label='DLP per requested procedure', required=False)
    plotCTRequestFreq = forms.BooleanField(label='Requested procedure frequency', required=False)
    plotCTRequestNumEvents = forms.BooleanField(label='# events per requested procedure', required=False)
    plotCTStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotCTStudyMeanDLPOverTime = forms.BooleanField(label='Study DLP over time', required=False)
    plotCTStudyMeanDLPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)


class RFChartOptionsForm(forms.Form):
    """Form for RF chart options
    """
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotRFStudyDAP = forms.BooleanField(label='DAP per study', required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)


class RFChartOptionsDisplayForm(forms.Form):
    """Form for RF chart display options
    """
    plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotRFStudyDAP = forms.BooleanField(label='DAP per study', required=False)
    plotRFInitialSortingChoice = forms.ChoiceField(label='Default chart sorting', choices=SORTING_CHOICES_DX,
                                                   required=False)


class MGChartOptionsForm(forms.Form):
    """Form for MG chart options
    """
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotMGStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotMGAGDvsThickness = forms.BooleanField(label='AGD vs. compressed thickness', required=False)
    plotMGkVpvsThickness = forms.BooleanField(label='kVp vs. compressed thickness', required=False)
    plotMGmAsvsThickness = forms.BooleanField(label='mAs vs. compressed thickness', required=False)
    # if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    #     plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)


class MGChartOptionsDisplayForm(forms.Form):
    """Form for MG chart display options
    """
    plotMGStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotMGAGDvsThickness = forms.BooleanField(label='AGD vs. compressed thickness', required=False)
    plotMGkVpvsThickness = forms.BooleanField(label='kVp vs. compressed thickness', required=False)
    plotMGmAsvsThickness = forms.BooleanField(label='mAs vs. compressed thickness', required=False)


class DXChartOptionsDisplayForm(forms.Form):
    """Form for DX chart display options
    """
    plotDXAcquisitionMeanDAP = forms.BooleanField(label='DAP per acquisition', required=False)
    plotDXAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotDXStudyMeanDAP = forms.BooleanField(label='DAP per study', required=False)
    plotDXStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotDXRequestMeanDAP = forms.BooleanField(label='DAP per requested procedure', required=False)
    plotDXRequestFreq = forms.BooleanField(label='requested procedure frequency', required=False)
    plotDXAcquisitionMeankVp = forms.BooleanField(label='kVp per acquisition', required=False)
    plotDXAcquisitionMeanmAs = forms.BooleanField(label='mAs per acquisition', required=False)
    plotDXStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotDXAcquisitionMeankVpOverTime = forms.BooleanField(label='Acquisition kVp over time', required=False)
    plotDXAcquisitionMeanmAsOverTime = forms.BooleanField(label='Acquisition mAs over time', required=False)
    plotDXAcquisitionMeanDAPOverTime = forms.BooleanField(label='Acquisition DAP over time', required=False)
    plotDXAcquisitionMeanDAPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    plotDXInitialSortingChoice = forms.ChoiceField(label='Default chart sorting', choices=SORTING_CHOICES_DX,
                                                   required=False)


class CTChartOptionsDisplayForm(forms.Form):
    """Form for CT chart display options
    """
    plotCTAcquisitionMeanDLP = forms.BooleanField(label='DLP per acquisition', required=False)
    plotCTAcquisitionMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per acquisition'),
                                                   required=False) # nosec
    plotCTAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotCTStudyMeanDLP = forms.BooleanField(label='DLP per study', required=False)
    plotCTStudyMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per study'), required=False) # nosec
    plotCTStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotCTStudyNumEvents = forms.BooleanField(label='# events per study', required=False)
    plotCTRequestMeanDLP = forms.BooleanField(label='DLP per requested procedure', required=False)
    plotCTRequestFreq = forms.BooleanField(label='Requested procedure frequency', required=False)
    plotCTRequestNumEvents = forms.BooleanField(label='# events per requested procedure', required=False)
    plotCTStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotCTStudyMeanDLPOverTime = forms.BooleanField(label='Study DLP over time', required=False)
    plotCTStudyMeanDLPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    plotCTInitialSortingChoice = forms.ChoiceField(label='Default chart sorting', choices=SORTING_CHOICES_CT,
                                                   required=False)


class GeneralChartOptionsDisplayForm(forms.Form):
    """Form for general chart display options
    """
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotInitialSortingDirection = forms.ChoiceField(label='Default sorting direction', choices=SORTING_DIRECTION,
                                                    required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)
    plotHistogramBins = forms.IntegerField(label='Number of histogram bins', min_value=2, max_value=40, required=False)
    plotCaseInsensitiveCategories = forms.BooleanField(label='Case-insensitive categories', required=False)


class UpdateDisplayNamesForm(forms.Form):
    display_names = forms.CharField()


class RFHighDoseFluoroAlertsForm(forms.ModelForm):
    """Form for displaying and changing fluoroscopy high dose alert settings
    """

    def __init__(self, *args, **kwargs):
        from crispy_forms.layout import Button
        super(RFHighDoseFluoroAlertsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'

        # If HighDoseMetricAlertSettings.changed_accum_dose_delta_weeks is True then the summed DAP and dose at RP
        # values have not yet been recalculated - display the recalculate button on the form.
        if self.instance.changed_accum_dose_delta_weeks:
            self.helper.add_input(Button('recalc_all_summed_data', 'Recalculate all summed data', css_class='btn btn-warning'))

        # If there is nothing in self.data and accum_dose_delta_weeks is in self.changed_data then the user must have
        # changed the accum_dose_delta_weeks value: set the changed_accum_dose_delta_weeks flag to True. This updates
        # the HighDoseMetricAlertSettings.changed_accum_dose_delta_weeks to True.
        if len(self.data):
            if self.has_changed():
                if 'accum_dose_delta_weeks' in self.changed_data:
                    self.instance.changed_accum_dose_delta_weeks = True
                    self.save()
        self.helper.layout = Layout(
            Div(
                'alert_total_dap_rf',
                'alert_total_rp_dose_rf',
                'accum_dose_delta_weeks',
                'show_accum_dose_over_delta_weeks',
                'calc_accum_dose_over_delta_weeks_on_import',
                'send_high_dose_metric_alert_emails',
            ),
            FormActions(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = HighDoseMetricAlertSettings
        fields = ['alert_total_dap_rf',
                  'alert_total_rp_dose_rf',
                  'accum_dose_delta_weeks',
                  'show_accum_dose_over_delta_weeks',
                  'calc_accum_dose_over_delta_weeks_on_import',
                  'send_high_dose_metric_alert_emails']


class HomepageOptionsForm(forms.Form):
    """Form for displaying and changing the home page options
    """
    dayDeltaA = forms.IntegerField(label='Primary time period to sum studies (days)', required=False)
    dayDeltaB = forms.IntegerField(label='Secondary time period to sum studies (days)', required=False)
    enable_workload_stats = forms.BooleanField(label='Enable calculation and display of workload stats on home page?',
                                               required=False)


class DicomQueryForm(forms.Form):
    """Form for launching DICOM Query
    """
    from datetime import date

    MODALITIES = (
        ('CT', 'CT'),
        ('FL', 'Fluoroscopy (XA and RF)'),
        ('DX', 'DX, including CR'),
        ('MG', 'Mammography'),
    )

    remote_host_field = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}))
    store_scp_field = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}))
    date_from_field = forms.DateField(label='Date from',
                                      widget=forms.DateInput(attrs={"class": "form-control datepicker", }),
                                      required=False, initial=date.today().isoformat(),
                                      help_text="Format yyyy-mm-dd, restrict as much as possible for best results")
    date_until_field = forms.DateField(label='Date until',
                                       widget=forms.DateInput(attrs={"class": "form-control datepicker", }),
                                       required=False,
                                       help_text="Format yyyy-mm-dd, restrict as much as possible for best results")
    modality_field = forms.MultipleChoiceField(
        choices=MODALITIES, widget=forms.CheckboxSelectMultiple(
            attrs={"checked": ""}), required=False, help_text=("At least one modality must be ticked - if SR only is "
                                                               "ticked (Advanced) these modalities will be ignored"))
    inc_sr_field = forms.BooleanField(label='Include SR only studies?', required=False, initial=False,
                                      help_text="Only use with stores containing only RDSRs, "
                                                "with no accompanying images")
    duplicates_field = forms.BooleanField(label='Ignore studies already in the database?', required=False, initial=True,
                                          help_text="Objects that have already been processed won't be imported, so "
                                                    "there isn't any point getting them!")
    desc_exclude_field = forms.CharField(required=False,
                                         label="Exclude studies with these terms in the study description:",
                                         help_text="Comma separated list of terms")
    desc_include_field = forms.CharField(required=False,
                                         label="Only keep studies with these terms in the study description:",
                                         help_text="Comma separated list of terms")
    stationname_exclude_field = forms.CharField(required=False,
                                                label="Exclude studies or series with these terms in the station name:",
                                                help_text="Comma separated list of terms")
    stationname_include_field = forms.CharField(required=False,
                                                label="Only keep studies or series with these terms in the station name:",
                                                help_text="Comma separated list of terms")
    get_toshiba_images_field = forms.BooleanField(label=u"Attempt to get Toshiba dose images", required=False,
                                                  help_text=u"Only applicable if using Toshiba RDSR generator extension, "
                                                            u"see Docs")

    def __init__(self, *args, **kwargs):
        super(DicomQueryForm, self).__init__(*args, **kwargs)
        from remapp.models import DicomRemoteQR, DicomStoreSCP
        self.fields['remote_host_field'].choices = [(x.pk, x.name) for x in DicomRemoteQR.objects.all()]
        self.fields['store_scp_field'].choices = [(x.pk, x.name) for x in DicomStoreSCP.objects.all()]
        self.helper = FormHelper(self)
        self.helper.form_id = 'post-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'q_process'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('remote_host_field', css_class='col-md-6', ),
                    Div('store_scp_field', css_class='col-md-6', ),
                ),
                InlineCheckboxes('modality_field'),
                Div(
                    Div('date_from_field', css_class='col-md-6', ),
                    Div('date_until_field', css_class='col-md-6', ),
                ),
                'desc_exclude_field',
                'desc_include_field',
                'stationname_exclude_field',
                'stationname_include_field',
                Accordion(
                    AccordionGroup(
                        'Advanced',
                        'get_toshiba_images_field',
                        'duplicates_field',
                        'inc_sr_field',
                        active=False
                    )
                ),
            ),
        )

    def clean(self):
        """
        Validate the form data to clear modality selections if sr_only is selected.
        :return: Form with modalities _or_ sr_only selected
        """
        qr_logger = logging.getLogger('remapp.netdicom.qrscu')

        cleaned_data = super(DicomQueryForm, self).clean()
        mods = cleaned_data.get("modality_field")
        inc_sr = cleaned_data.get("inc_sr_field")
        qr_logger.debug("Form mods are {0}, inc_sr is {1}".format(mods, inc_sr))
        qr_logger.debug("All form modes are {0}".format(cleaned_data))
        if inc_sr:
            self.cleaned_data['modality_field'] = None
        elif not mods:
            raise forms.ValidationError("You must select at least one modality (or Advanced SR Only)")
        return cleaned_data


class DicomDeleteSettingsForm(forms.ModelForm):
    """Form for configuring whether DICOM objects are stored or deleted once processed
    """

    def __init__(self, *args, **kwargs):
        super(DicomDeleteSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Div(
                HTML("""
                     <h4>Do you want objects that we can't do anything with to be deleted?</h4>
                """),
                'del_no_match',
                HTML("""
                     <h4>The remaining choices are for DICOM objects we have processed and attempted to import to the
                     database:</h4>
                """),
                'del_rdsr',
                'del_mg_im', 'del_dx_im', 'del_ct_phil'
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-2">
                    <a href='""" + reverse('dicom_summary') + """#delete' role="button" class="btn btn-default">
                        Cancel and return to the DICOM configuration and DICOM object delete summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = DicomDeleteSettings
        fields = ['del_no_match', 'del_rdsr', 'del_mg_im', 'del_dx_im', 'del_ct_phil']


class DicomQRForm(forms.ModelForm):
    """Form for configuring remote Query Retrieve nodes
    """

    def __init__(self, *args, **kwargs):
        super(DicomQRForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-8'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Div(
                'name', 'aetitle', 'callingaet', 'port', 'ip', 'hostname'
            ),
            Accordion(
                AccordionGroup(
                    'Non-standard configuration options',
                    Div(
                        HTML("""
                        <p>
                          Some PACS systems (like Impax 6.6) need modality at study level for correct filtering. 
                          Others will return no results if modality is included at study level. See
                            <a href="http://docs.openrem.org/en/{{ admin.docsversion }}/netdicom-qr-config.html"
                                target="_blank" data-toggle="tooltip"
                                title="DICOM query-retrieve node config documentation - opens in a new tab">
                                DICOM query-retrieve node config documentation
                            </a>
                        </p>
                        """)
                    ),
                    PrependedText('use_modality_tag', ''),  # Trick to force label to join the other labels,
                                                            # otherwise sits to right
                    active=False
                )
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-4">
                    <a href='""" + reverse('dicom_summary') + """' role="button" class="btn btn-default">
                        Cancel and return to DICOM configuration summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = DicomRemoteQR
        fields = ['name', 'aetitle', 'callingaet', 'port', 'ip', 'hostname', 'use_modality_tag']


class DicomStoreForm(forms.ModelForm):
    """Form for configuring local Store nodes
    """

    def __init__(self, *args, **kwargs):
        super(DicomStoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-8'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Div(
                'name', 'aetitle', 'port',
            ),
            Accordion(
                AccordionGroup(
                    'Advanced - test/development use only',
                    Div(
                        HTML("""
                        <p>
                          DICOM store node built in to OpenREM is not yet ready for production. See
                            <a href="https://docs.openrem.org/en/{{ admin.docsversion }}/netdicom-nodes.html"
                                target="_blank" data-toggle="tooltip"
                                title="DICOM store documentation - opens in a new tab">
                                DICOM store documentation (Advanced)
                            </a>
                        </p>
                        """)
                    ),
                    PrependedText('controlled', ''),  # Trick to force label to join the other labels, otherwise sits to right
                    PrependedText('keep_alive', ''),
                    active=False
                )
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-4">
                    <a href='""" + reverse('dicom_summary') + """' role="button" class="btn btn-default">
                        Cancel and return to DICOM configuration summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = DicomStoreSCP
        fields = ['name', 'aetitle', 'port', 'controlled', 'keep_alive']
        labels = {
            'port': "Port: 104 is standard for DICOM but ports higher than 1024 requires fewer admin rights",
            'controlled': "Advanced use only: tick this box to control the server using OpenREM",
            'keep_alive': "Advanced use only: tick this box to auto-start this server using celery beat"
        }


class SkinDoseMapCalcSettingsForm(forms.ModelForm):
    """Form for configuring whether skin dose maps are shown / calculated
    """

    def __init__(self, *args, **kwargs):
        super(SkinDoseMapCalcSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                'enable_skin_dose_maps',
                'calc_on_import'
            ),
            FormActions(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = SkinDoseMapCalcSettings
        fields = ['enable_skin_dose_maps', 'calc_on_import']


class NotPatientNameForm(forms.ModelForm):
    """Form for configuring not-patient name patterns
    """

    def __init__(self, *args, **kwargs):
        super(NotPatientNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-8'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Div(
                'not_patient_name',
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-4">
                    <a href='""" + reverse('not_patient_indicators') + """' role="button" class="btn btn-default">
                        Cancel and return to not-patient indicator summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = NotPatientIndicatorsName
        fields = ['not_patient_name', ]
        labels = {
            'not_patient_name': "pattern for name matching",
        }


class NotPatientIDForm(forms.ModelForm):
    """Form for configuring not-patient ID patterns
    """

    def __init__(self, *args, **kwargs):
        super(NotPatientIDForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-8'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Div(
                'not_patient_id',
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-4">
                    <a href='""" + reverse('not_patient_indicators') + """' role="button" class="btn btn-default">
                        Cancel and return to not-patient indicator summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = NotPatientIndicatorsID
        fields = ['not_patient_id', ]
        labels = {
            'not_patient_id': "pattern for ID matching",
        }
