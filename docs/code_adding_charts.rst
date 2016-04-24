##################
Adding a new chart
##################

To add a new CT or DX chart several files need to be updated:

* ``models.py``
* ``forms.py``
* ``views.py``
* ``xxfiltered.html``
* ``xxChartAjax.js``

Where xx is one of ``ct`` or ``dx``

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

A new item needs to be added to this method's parameters.

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

Our new chart makes use of ``acquisition events`` (rather than ``study_events``
or ``request_events``). We therefore need to ensure that ``acquisition_events``
are available if the user has chosen to show the new chart.

Before:

.. sourcecode:: python

    if plot_acquisition_mean_dlp or plot_acquisition_mean_ctdi or plot_acquisition_freq:
        acquisition_events = CtIrradiationEventData.objects.exclude(
            ct_acquisition_type__code_meaning__exact=u'Constant Angle Acquisition').exclude(
            **{'dlp__isnull': True}).exclude(
            **{'acquisition_protocol__isnull': True}).exclude(
            **{'acquisition_protocol': ''}).filter(
            **acquisition_filters
        )

After:

.. sourcecode:: python

    if plot_acquisition_mean_dlp or plot_acquisition_mean_ctdi or plot_acquisition_freq or plot_acquisition_ctdi_over_time:
        acquisition_events = CtIrradiationEventData.objects.exclude(
            ct_acquisition_type__code_meaning__exact=u'Constant Angle Acquisition').exclude(
            **{'dlp__isnull': True}).exclude(
            **{'acquisition_protocol__isnull': True}).exclude(
            **{'acquisition_protocol': ''}).filter(
            **acquisition_filters
        )

We now need to add code that will calculate the data for the new chart. This
uses one of the methods in the ``chart_functions.py`` file, located in the
``interface`` folder of the OpenREM project.

.. sourcecode:: python

    if plot_acquisition_ctdi_over_time:
        result = average_chart_over_time_data(f, acquisition_events,
                                              'acquisition_protocol',
                                              'mean_ctdivol',
                                              'study_date', 'date_time_started',
                                              median_available, plot_average_choice,
                                              1, plot_study_mean_dlp_over_time_period)
        if median_available and (plot_average_choice == 'median' or plot_average_choice == 'both'):
            return_structure['acquisitionCTDIoverTime'] = result['median_over_time']
        if plot_average_choice == 'mean' or plot_average_choice == 'both':
            return_structure['acquisitionCTDIoverTime'] = result['mean_over_time']
        if not plot_acquisition_mean_ctdi:
            return_structure['acquisitionNameListCTDI'] = result['series_names']

This data will now be available to the browser via JavaScript, and can be used
to populate the chart itself.

================================
Additions to ``ctfiltered.html``
================================

A section of this file sets a JavaScript variable per chart. A new one needs to
be added.

Before:

.. sourcecode:: html

        <!-- Flags to determine if charts should be plotted -->
        {% if request.user.userprofile.plotCTAcquisitionMeanDLP %}
            <script>var plotCTAcquisitionMeanDLP = true;</script>
        {% endif %}

        {% if request.user.userprofile.plotCTAcquisitionMeanCTDI %}
            <script>var plotCTAcquisitionMeanCTDI = true;</script>
        {% endif %}

        {% if request.user.userprofile.plotCTAcquisitionFreq %}
            <script>var plotCTAcquisitionFreq = true;</script>
        {% endif %}

        ...
        ...

        <script>var plotAverageChoice = '{{ request.user.userprofile.plotAverageChoice }}';</script>
        <!-- End of flags to determine if charts should be plotted -->

After:

.. sourcecode:: html

        <!-- Flags to determine if charts should be plotted -->
        {% if request.user.userprofile.plotCTAcquisitionMeanDLP %}
            <script>var plotCTAcquisitionMeanDLP = true;</script>
        {% endif %}

        {% if request.user.userprofile.plotCTAcquisitionMeanCTDI %}
            <script>var plotCTAcquisitionMeanCTDI = true;</script>
        {% endif %}

        {% if request.user.userprofile.plotCTAcquisitionFreq %}
            <script>var plotCTAcquisitionFreq = true;</script>
        {% endif %}

        {% if request.user.userprofile.plotCTAcquisitionCTDIOverTime %}
            <script>var plotCTAcquisitionCTDIOverTime = true;</script>
        {% endif %}

        ...
        ...

        <script>var plotAverageChoice = '{{ request.user.userprofile.plotAverageChoice }}';</script>
        <!-- End of flags to determine if charts should be plotted -->

A second section of code needs to be added to ``ctfiltered.html`` to include a
DIV for the new chart:

.. sourcecode:: html

        {% if request.user.userprofile.plotCTAcquisitionCTDIOverTime %}
            <!-- HTML to include div container for acquisition CTDI over time -->

            <script>
                $(window).resize(function() {
                    chartSetExportSize('acqCTDIOverTimeDIV');
                });
            </script>

            <div class="panel-group" id="accordion10">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 class="panel-title">
                            <a data-toggle="collapse" data-parent="#accordion10" href="#collapseAcqCTDIOverTimeChart" onclick="setTimeout(function() {$(document).resize();}, 0);">
                                {% if request.user.userprofile.plotAverageChoice == 'mean' %}
                                    Line plot showing mean CTDI<sub>vol</sub> of each acquisition type over time ({{ request.user.userprofile.plotCTStudyMeanDLPOverTimePeriod }}).
                                {% else %}
                                    Line plot showing median CTDI<sub>vol</sub> of each acquisition type over time ({{ request.user.userprofile.plotCTStudyMeanDLPOverTimePeriod }}).
                                {% endif %}
                            </a>
                        </h4>
                    </div>
                    <div id="collapseAcqCTDIOverTimeChart" class="panel-collapse collapse">
                        <div class="panel-body">
                            <div id="acqCTDIOverTimeDIV" style="height: auto; margin: 0 0"></div>
                            <p>Click on the legend entries to show or hide the corresponding series. Click and drag the mouse over a date range to zoom in.</p>
                            <a onclick="enterFullScreen('collapseAcqCTDIOverTimeChart', 'acqCTDIOverTimeDIV')" class="btn btn-default btn-sm" role="button">Toggle fullscreen</a>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End of HTML to include div container for acquisition CTDI over time -->
        {% endif %}


And finally a third section:

.. sourcecode:: html

        {% if request.user.userprofile.plotCTAcquisitionCTDIOverTime %}
            <!-- JavaScript for CTDI over time -->
            <script>
                var urlStartAcqCTDIOverTime = '/openrem/ct/?{% for field in filter.form %}{% if field.name != 'acquisition_protocol' and field.name != 'date_before' and field.name != 'date_after' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&acquisition_protocol=';
            </script>

            {% if request.user.userprofile.plotAverageChoice == 'mean' %}
                <script>
                    result = chartAverageOverTime('acqCTDIOverTimeDIV', 'CTDI<sub>vol</sub>', 'mGy', 'Mean');
                </script>
            {% else %}
                <script>
                    result = chartAverageOverTime('acqCTDIOverTimeDIV', 'CTDI<sub>vol</sub>', 'mGy', 'Median');
                </script>
            {% endif %}
            <!-- End of JavaScript for CTDI over time -->
        {% endif %}

===============================
Additions to ``ctChartAjax.js``
===============================

.. sourcecode:: javascript

            // CTDI over time chart data
            if(typeof plotCTAcquisitionCTDIOverTime !== 'undefined') {
                var acq_line_colours = new Array(json.acquisitionNameListCTDI.length);
                if (typeof plotCTAcquisitionFreq !== 'undefined') {
                    acq_line_colours = [];
                    for (i = 0; i < $('#piechartAcquisitionDIV').highcharts().series[0].data.length; i++) {
                        acq_line_colours.push($('#piechartAcquisitionDIV').highcharts().series[0].data.sort(sort_by_name)[i].color);
                    }
                    $('#piechartAcquisitionDIV').highcharts().series[0].data.sort(sort_by_y);
                }
                else acq_line_colours = colour_scale.colors(json.acquisitionNameListCTDI.length);

                var acq_ctdi_over_time = json.acquisitionCTDIoverTime;
                updateOverTimeChart(json.acquisitionNameListCTDI, acq_ctdi_over_time, acq_line_colours, urlStartAcq, 'acqCTDIOverTimeDIV');
            }
