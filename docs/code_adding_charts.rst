##################
Adding a new chart
##################

To add a new CT or DX chart several files need to be updated:

* ``models.py``
* ``forms.py``
* ``views.py``
* The ``xxfiltered.html`` and ``xxChartAjax.js`` files corresponding to the
  modality, where xx is one of ``ct`` or ``dx``

The process is probably best illustrated via an example. What follows is a
description of how to add a new chart that displays acquisition protocol
CTDI\ :sub:`vol`\ over time.

*********************************************
Adding a chart of CTDI\ :sub:`vol`\ over time
*********************************************

==========================
Additions to ``models.py``
==========================

A field needs to be added to the ``UserProfile`` section in ``models.py`` to
control whether the new chart should be plotted. There is a section of this
file that looks like the following:

.. sourcecode:: python

    plotCTAcquisitionMeanDLP = models.BooleanField(default=True)
    plotCTAcquisitionMeanCTDI = models.BooleanField(default=True)
    plotCTAcquisitionFreq = models.BooleanField(default=False)
    plotCTStudyMeanDLP = models.BooleanField(default=True)
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

A new line needs to be added to this section, using an appropriate name such
as:

.. sourcecode:: python

    plotCTAcquisitionCTDIOverTime = models.BooleanField(default=False)

Adding a new field to ``models.py`` requires that a database migration is carried
out to add the field to the database. This is done via the command line::

    python manage.py makemigrations remapp
    python manage.py migrate remapp

The first command should result in a response similar to::

    Migrations for 'remapp':
      0004_auto_20160424_1116.py:
        - Add field plotCTAcquisitionCTDIOverTime to userprofile

The second command should result in a response similar to::

    Operations to perform:
      Apply all migrations: remapp
    Running migrations:
      Rendering model states... DONE
      Applying remapp.0004_auto_20160424_1116... OK

That's the end of the changes required in ``models.py``

=========================
Additions to ``forms.py``
=========================

An additional line needs to be added to the ``XXChartOptionsForm`` and
``XXChartOptionsDisplayForm`` methods in ``forms.py``, where ``XX`` is either
``CT`` or ``DX``.

For our new chart the following line needs to be added to both
``CTChartOptionsForm`` and ``CTChartOptionsDisplayForm``:

.. sourcecode:: python

    plotCTAcquisitionCTDIOverTime = forms.BooleanField(label='Acquisition CTDI over time', required=False)

That's the end of the changes required in ``models.py``

=========================
Additions to ``views.py``
=========================

Three methods in this file need to be updated.

------------------------------------
``xx_summary_list_filter`` additions
------------------------------------

Some additions need to be made to the ``xx_summary_list_filter`` method in
``views.py``, where ``xx`` is either ``ct`` or ``dx``. As we're adding a
new CT chart, we need to edit ``ct_summary_list_filter``.

A section of this method examines the user's chart plotting preferences. Code
must be added to include the new chart in these checks. An abbreviated version
of the section is shown below.

.. sourcecode:: python

    # Obtain the chart options from the request
    chart_options_form = CTChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotCTAcquisitionMeanDLP = chart_options_form.cleaned_data['plotCTAcquisitionMeanDLP']
            user_profile.plotCTAcquisitionMeanCTDI = chart_options_form.cleaned_data['plotCTAcquisitionMeanCTDI']
            ...
            ...
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                        'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                        'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                        'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                        ...
                        ...
            chart_options_form = CTChartOptionsForm(form_data)

A new line needs to be inserted into the ``if`` and ``else`` sections for the
new chart:

.. sourcecode:: python

    # Obtain the chart options from the request
    chart_options_form = CTChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotCTAcquisitionMeanDLP = chart_options_form.cleaned_data['plotCTAcquisitionMeanDLP']
            user_profile.plotCTAcquisitionMeanCTDI = chart_options_form.cleaned_data['plotCTAcquisitionMeanCTDI']
            user_profile.plotCTAcquisitionCTDIOverTime = chart_options_form.cleaned_data['plotCTAcquisitionCTDIOverTime']
            ...
            ...
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                        'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                        'plotCTAcquisitionMeanCTDI': user_profile.plotCTAcquisitionMeanCTDI,
                        'plotCTAcquisitionFreq': user_profile.plotCTAcquisitionFreq,
                        'plotCTAcquisitionCTDIOverTime': user_profile.plotCTAcquisitionCTDIOverTime,
                        ...
                        ...
            chart_options_form = CTChartOptionsForm(form_data)

-----------------------------------
``xx_summary_chart_data`` additions
-----------------------------------

The ``return_structure`` variable needs the new user_profile field adding.

Before:

.. sourcecode:: python

    return_structure =\
        ct_plot_calculations(f, user_profile.plotCTAcquisitionFreq, user_profile.plotCTAcquisitionMeanCTDI, user_profile.plotCTAcquisitionMeanDLP,
                             user_profile.plotCTRequestFreq, user_profile.plotCTRequestMeanDLP, user_profile.plotCTStudyFreq, user_profile.plotCTStudyMeanDLP,
                             user_profile.plotCTStudyMeanDLPOverTime, user_profile.plotCTStudyMeanDLPOverTimePeriod, user_profile.plotCTStudyPerDayAndHour,
                             request_results, median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins)

After:

.. sourcecode:: python

    return_structure =\
        ct_plot_calculations(f, user_profile.plotCTAcquisitionFreq, user_profile.plotCTAcquisitionMeanCTDI, user_profile.plotCTAcquisitionMeanDLP,
                             user_profile.plotCTRequestFreq, user_profile.plotCTRequestMeanDLP, user_profile.plotCTStudyFreq, user_profile.plotCTStudyMeanDLP,
                             user_profile.plotCTStudyMeanDLPOverTime, user_profile.plotCTStudyMeanDLPOverTimePeriod, user_profile.plotCTStudyPerDayAndHour,
                             request_results, median_available, user_profile.plotAverageChoice, user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins,
                             user_profile.plotCTAcquisitionCTDIOverTime)

----------------------------------
``XX_plot_calculations`` additions
----------------------------------

A new item needs to be added to the parameters.

Before:

.. sourcecode:: python

    def ct_plot_calculations(f, plot_acquisition_freq, plot_acquisition_mean_ctdi, plot_acquisition_mean_dlp,
                             plot_request_freq, plot_request_mean_dlp, plot_study_freq, plot_study_mean_dlp,
                             plot_study_mean_dlp_over_time, plot_study_mean_dlp_over_time_period, plot_study_per_day_and_hour,
                             request_results, median_available, plot_average_choice, plot_series_per_systems, plot_histogram_bins):

After:

.. sourcecode:: python

    def ct_plot_calculations(f, plot_acquisition_freq, plot_acquisition_mean_ctdi, plot_acquisition_mean_dlp,
                             plot_request_freq, plot_request_mean_dlp, plot_study_freq, plot_study_mean_dlp,
                             plot_study_mean_dlp_over_time, plot_study_mean_dlp_over_time_period, plot_study_per_day_and_hour,
                             request_results, median_available, plot_average_choice, plot_series_per_systems, plot_histogram_bins,
                             plot_acquisition_ctdi_over_time):
