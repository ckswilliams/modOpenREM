from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, PrependedText, InlineCheckboxes, Accordion, AccordionGroup
from openremproject import settings
from remapp.models import DicomDeleteSettings, DicomRemoteQR, DicomStoreSCP, SkinDoseMapCalcSettings

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


class DXChartOptionsForm(forms.Form):
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


class CTChartOptionsForm(forms.Form):
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotCTAcquisitionMeanDLP = forms.BooleanField(label='DLP per acquisition', required=False)
    plotCTAcquisitionMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per acquisition'),
                                                   required=False)
    plotCTAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotCTStudyMeanDLP = forms.BooleanField(label='DLP per study', required=False)
    plotCTStudyMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per study'), required=False)
    plotCTStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotCTRequestMeanDLP = forms.BooleanField(label='DLP per requested procedure', required=False)
    plotCTRequestFreq = forms.BooleanField(label='Requested procedure frequency', required=False)
    plotCTStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotCTStudyMeanDLPOverTime = forms.BooleanField(label='Study DLP over time', required=False)
    plotCTStudyMeanDLPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)


class RFChartOptionsForm(forms.Form):
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotRFStudyDAP = forms.BooleanField(label='DAP per study', required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)


class RFChartOptionsDisplayForm(forms.Form):
    plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotRFStudyDAP = forms.BooleanField(label='DAP per study', required=False)
    plotRFInitialSortingChoice = forms.ChoiceField(label='Default chart sorting', choices=SORTING_CHOICES_DX,
                                               required=False)


class MGChartOptionsForm(forms.Form):
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    plotMGStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotMGAGDvsThickness = forms.BooleanField(label='AGD vs. compressed thickness', required=False)
    # if 'postgresql' in settings.DATABASES['default']['ENGINE']:
    #     plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)


class MGChartOptionsDisplayForm(forms.Form):
    plotMGStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotMGAGDvsThickness = forms.BooleanField(label='AGD vs. compressed thickness', required=False)


class DXChartOptionsDisplayForm(forms.Form):
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
    plotCTAcquisitionMeanDLP = forms.BooleanField(label='DLP per acquisition', required=False)
    plotCTAcquisitionMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per acquisition'),
                                                   required=False)
    plotCTAcquisitionFreq = forms.BooleanField(label='Acquisition frequency', required=False)
    plotCTStudyMeanDLP = forms.BooleanField(label='DLP per study', required=False)
    plotCTStudyMeanCTDI = forms.BooleanField(label=mark_safe('CTDI<sub>vol</sub> per study'), required=False)
    plotCTStudyFreq = forms.BooleanField(label='Study frequency', required=False)
    plotCTRequestMeanDLP = forms.BooleanField(label='DLP per requested procedure', required=False)
    plotCTRequestFreq = forms.BooleanField(label='Requested procedure frequency', required=False)
    plotCTStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotCTStudyMeanDLPOverTime = forms.BooleanField(label='Study DLP over time', required=False)
    plotCTStudyMeanDLPOverTimePeriod = forms.ChoiceField(label='Time period', choices=TIME_PERIOD, required=False)
    plotCTInitialSortingChoice = forms.ChoiceField(label='Default chart sorting', choices=SORTING_CHOICES_CT,
                                                   required=False)


class GeneralChartOptionsDisplayForm(forms.Form):
    plotCharts = forms.BooleanField(label='Plot charts?', required=False)
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        plotMeanMedianOrBoth = forms.ChoiceField(label='Average to use', choices=AVERAGES, required=False)
    plotInitialSortingDirection = forms.ChoiceField(label='Default sorting direction', choices=SORTING_DIRECTION,
                                                    required=False)
    plotSeriesPerSystem = forms.BooleanField(label='Plot a series per system', required=False)
    plotHistograms = forms.BooleanField(label='Calculate histogram data', required=False)
    plotHistogramBins = forms.IntegerField(label='Number of histogram bins', min_value=2, max_value=40, required=False)

class UpdateDisplayNamesForm(forms.Form):
    display_names = forms.CharField()


class DicomQueryForm(forms.Form):
    """Form for launching DICOM Query
    """

    MODALITIES = (
        ('CT', 'CT'),
        ('FL', 'Fluoroscopy'),
        ('DX', 'DX, including CR'),
        ('MG', 'Mammography'),
    )

    remote_host_field = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}))
    store_scp_field = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-control"}))
    date_from_field = forms.DateField(label='Date from',
                                      widget=forms.DateInput(attrs={"class": "form-control datepicker", }),
                                      required=False,
                                      help_text="Format yyyy-mm-dd, restrict as much as possible for best results")
    date_until_field = forms.DateField(label='Date until',
                                       widget=forms.DateInput(attrs={"class": "form-control datepicker", }),
                                       required=False,
                                       help_text="Format yyyy-mm-dd, restrict as much as possible for best results")
    modality_field = forms.MultipleChoiceField(
        choices=MODALITIES, widget=forms.CheckboxSelectMultiple(
            attrs={"checked": ""}), required=True, help_text="At least one modality must be ticked")
    inc_sr_field = forms.BooleanField(label='Include SR only studies?', required=False, initial=False,
                                      help_text="Normally only useful if querying a store holding just DICOM Radiation Dose Structured Reports")
    duplicates_field = forms.BooleanField(label='Ignore studies already in the database?', required=False, initial=True,
                                          help_text="Studies with the same study UID won't be imported, so there isn't any point getting them!")
    desc_exclude_field = forms.CharField(required=False,
                                         label="Exclude studies with these terms in the study description:",
                                         help_text="Comma separated list of terms")
    desc_include_field = forms.CharField(required=False,
                                         label="Only keep studies with these terms in the study description:",
                                         help_text="Comma separated list of terms")

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
                Accordion(
                    AccordionGroup(
                        'Advanced',
                        'inc_sr_field',
                        'duplicates_field',
                        active=False
                    )
                ),
            ),
        )


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
                    <a href="/openrem/admin/dicomsummary#delete" role="button" class="btn btn-default">
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
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            Div(
                'name', 'aetitle', 'callingaet', 'port', 'ip', 'hostname'
            ),
            FormActions(
                Submit('submit', 'Submit')
            ),
            Div(
                HTML("""
                <div class="col-lg-4 col-lg-offset-4">
                    <a href="/openrem/admin/dicomsummary" role="button" class="btn btn-default">
                        Cancel and return to DICOM configuration summary page
                    </a>
                </div>
                """)
            )
        )

    class Meta:
        model = DicomRemoteQR
        fields = ['name', 'aetitle', 'callingaet', 'port', 'ip', 'hostname']


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
                            <a href="http://docs.openrem.org/en/{{ admin.docsversion }}/netdicom-nodes.html"
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
                    <a href="/openrem/admin/dicomsummary" role="button" class="btn btn-default">
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
