#################
Adding new charts
#################

To add a new chart several files need to be updated:

* ``models.py``
* ``forms.py``
* ``views.py``
* ``xxfiltered.html``
* ``xxChartAjax.js``
* ``displaychartoptions.html``

Where xx is one of ``ct``, ``dx``, ``mg`` or ``rf``

The additions to the files add:

* database fields in the user profile to control whether the new charts are plotted (``models.py``)
* new options on the chart plotting forms (``forms.py``, ``displaychartoptions.html``)
* extra code to calculate the data for the new charts if they are switched on (``views.py``)
* a section of html and JavaScript to contain the charts (``xxfiltered.html``)
* a section of JavaScript to pass the data calculated by ``views.py`` to ``xxfiltered.html``

The process is probably best illustrated with an example. What follows is a
description of how to add a new chart that displays study workload for
fluoroscopy, and a pie chart of study description frequency.

==========================
Additions to ``models.py``
==========================

A field per chart needs to be added to the ``UserProfile`` section in
``models.py`` to control whether the new charts should be plotted. There is a
section of this file that looks like the following:

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

Two new lines needs to be added to this section, using appropriate names such
as:

.. sourcecode:: python

    plotRFStudyPerDayAndHour = models.BooleanField(default=False)
    plotRFStudyFreq = models.BooleanField(default=False)

Adding new fields to ``models.py`` requires that a database migration is carried
out to add the fields to the database. This is done via the command line::

    python manage.py makemigrations remapp
    python manage.py migrate remapp

The first command should result in a response similar to::

    Migrations for 'remapp':
      0004_auto_20160424_1116.py:
        - Add field plotRFAcquisitionCTDIOverTime to userprofile
        - Add field plotRFStudyFreq to userprofile

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

Two additional lines need to be added to the ``XXChartOptionsForm`` and
``XXChartOptionsDisplayForm`` methods in ``forms.py``, where ``XX`` is one of
``CT``, ``DX``, ``MG`` or ``RF``.

For our new charts the following lines needs to be added to both
``RFChartOptionsForm`` and ``RFChartOptionsDisplayForm``:

.. sourcecode:: python

    plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
    plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)

In addition, a new method needs to be added so that the RF chart options are
shown when the user goes to Config -> Chart options:

.. sourcecode:: python

    class RFChartOptionsDisplayForm(forms.Form):
        plotRFStudyPerDayAndHour = forms.BooleanField(label='Study workload', required=False)
        plotRFStudyFreq = forms.BooleanField(label='Study frequency', required=False)

That's the end of the changes required in ``forms.py``

=========================
Additions to ``views.py``
=========================

Four methods in this file need to be updated.

------------------------------------
``xx_summary_list_filter`` additions
------------------------------------

Some additions need to be made to the ``xx_summary_list_filter`` method in
``views.py``, where ``xx`` is one of ``ct``, ``dx``, ``mg`` or ``rf``. As we're
adding new RF charts, we need to edit ``rf_summary_list_filter``.

A section of this method examines the user's chart plotting preferences. Code
must be added to include the new chart in these checks. An abbreviated version
of the section is shown below.

.. sourcecode:: python

    # Obtain the chart options from the request
    chart_options_form = RFChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice}
            chart_options_form = RFChartOptionsForm(form_data)

Two new lines needs to be inserted into the ``if`` and ``else`` sections for the
new chart:

.. sourcecode:: python

    # Obtain the chart options from the request
    chart_options_form = RFChartOptionsForm(request.GET)
    # Check whether the form data is valid
    if chart_options_form.is_valid():
        # Use the form data if the user clicked on the submit button
        if "submit" in request.GET:
            # process the data in form.cleaned_data as required
            user_profile.plotCharts = chart_options_form.cleaned_data['plotCharts']
            user_profile.plotRFStudyPerDayAndHour = chart_options_form.cleaned_data['plotRFStudyPerDayAndHour']
            user_profile.plotRFStudyFreq = chart_options_form.cleaned_data['plotRFStudyFreq']
            if median_available:
                user_profile.plotAverageChoice = chart_options_form.cleaned_data['plotMeanMedianOrBoth']
            user_profile.save()

        else:
            form_data = {'plotCharts': user_profile.plotCharts,
                         'plotRFStudyPerDayAndHour': user_profile.plotRFStudyPerDayAndHour,
                         'plotRFStudyFreq': user_profile.plotRFStudyFreq,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice}
            chart_options_form = RFChartOptionsForm(form_data)

-----------------------------------
``xx_summary_chart_data`` additions
-----------------------------------

The ``return_structure`` variable needs the new user_profile fields adding.

Before:

.. sourcecode:: python

    return_structure =\
        rf_plot_calculations(f, request_results, median_available, user_profile.plotAverageChoice,
                             user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins)

After:

.. sourcecode:: python

    return_structure =\
        rf_plot_calculations(f, request_results, median_available, user_profile.plotAverageChoice,
                             user_profile.plotSeriesPerSystem, user_profile.plotHistogramBins,
                             user_profile.plotRFStudyPerDayAndHour,  user_profile.plotRFStudyFreq)

----------------------------------
``xx_plot_calculations`` additions
----------------------------------

Two items needs to be added to this method's parameters.

Before:

.. sourcecode:: python

    def rf_plot_calculations(f, request_results, median_available, plot_average_choice, plot_series_per_systems,
                             plot_histogram_bins):

After:

.. sourcecode:: python

    def rf_plot_calculations(f, request_results, median_available, plot_average_choice, plot_series_per_systems,
                             plot_histogram_bins, plot_study_per_day_and_hour, plot_study_freq):

Our new charts makes use of ``study_events`` (rather than ``acquisition_events``
or ``request_events``). We therefore need to ensure that ``study_events`` are
available if the user has chosen to show the new chart.

After additions:

.. sourcecode:: python

    if plot_study_per_day_and_hour:
        study_events = GeneralStudyModuleAttr.objects.exclude(
            study_description__isnull=True
        ).filter(
            study_instance_uid__in=exp_include
        )

We now need to add code that will calculate the data for the new charts. This
uses one of the methods in the ``chart_functions.py`` file, located in the
``interface`` folder of the OpenREM project.

.. sourcecode:: python

    if plot_study_per_day_and_hour:
        result = workload_chart_data(study_events)
        return_structure['studiesPerHourInWeekdays'] = result['workload']

    if plot_study_freq:
        result = average_chart_inc_histogram_data(study_events,
                                                  'generalequipmentmoduleattr__unique_equipment_name_id__display_name',
                                                  'study_description',
                                                  'projectionxrayradiationdose__accumxraydose__accumintegratedprojradiogdose__dose_area_product_total',
                                                  1, 0, plot_study_freq, plot_series_per_systems, plot_average_choice,
                                                  median_available, plot_histogram_bins)

        return_structure['studySystemList'] = result['system_list']
        return_structure['studyNameList'] = result['series_names']
        return_structure['studySummary'] = result['summary']

The data in ``return_structure`` will now be available to the browser via
JavaScript, and can be used to populate the charts themselves.

----------------------------------
``chart_options_view`` additions
----------------------------------

The RF options form need to be imported

Before:

.. sourcecode:: python

    from remapp.forms import GeneralChartOptionsDisplayForm, DXChartOptionsDisplayForm, CTChartOptionsDisplayForm

After:

.. sourcecode:: python

    from remapp.forms import GeneralChartOptionsDisplayForm, DXChartOptionsDisplayForm, CTChartOptionsDisplayForm,\
        RFChartOptionsDisplayForm

The RF form items need to be included

Before (abbreviated):

.. sourcecode:: python

    if request.method == 'POST':
        general_form = GeneralChartOptionsDisplayForm(request.POST)
        ct_form = CTChartOptionsDisplayForm(request.POST)
        dx_form = DXChartOptionsDisplayForm(request.POST)
        if general_form.is_valid() and ct_form.is_valid() and dx_form.is_valid() and rf_form.is_valid():
            try:
                # See if the user has plot settings in userprofile
                user_profile = request.user.userprofile
            except:
                # Create a default userprofile for the user if one doesn't exist
                create_user_profile(sender=request.user, instance=request.user, created=True)
                user_profile = request.user.userprofile

            user_profile.plotCharts = general_form.cleaned_data['plotCharts']
            ...
            ...
            user_profile.plotHistogramBins = general_form.cleaned_data['plotHistogramBins']

            user_profile.plotCTAcquisitionMeanDLP = ct_form.cleaned_data['plotCTAcquisitionMeanDLP']
            ...
            ...
            user_profile.plotCTInitialSortingChoice = ct_form.cleaned_data['plotCTInitialSortingChoice']

            user_profile.plotDXAcquisitionMeanDAP = dx_form.cleaned_data['plotDXAcquisitionMeanDAP']
            ...
            ...
            user_profile.plotDXInitialSortingChoice = dx_form.cleaned_data['plotDXInitialSortingChoice']

            user_profile.save()

        messages.success(request, "Chart options have been updated")

    ...
    ...

    general_form_data = {'plotCharts': user_profile.plotCharts,
                         'plotMeanMedianOrBoth': user_profile.plotAverageChoice,
                         'plotInitialSortingDirection': user_profile.plotInitialSortingDirection,
                         'plotSeriesPerSystem': user_profile.plotSeriesPerSystem,
                         'plotHistogramBins': user_profile.plotHistogramBins}

    ct_form_data = {'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                    ...
                    ...
                    'plotCTInitialSortingChoice': user_profile.plotCTInitialSortingChoice}

    dx_form_data = {'plotDXAcquisitionMeanDAP': user_profile.plotDXAcquisitionMeanDAP,
                    ...
                    ...
                    'plotDXInitialSortingChoice': user_profile.plotDXInitialSortingChoice}


    general_chart_options_form = GeneralChartOptionsDisplayForm(general_form_data)
    ct_chart_options_form = CTChartOptionsDisplayForm(ct_form_data)
    dx_chart_options_form = DXChartOptionsDisplayForm(dx_form_data)

    return_structure = {'admin': admin,
                        'GeneralChartOptionsForm': general_chart_options_form,
                        'CTChartOptionsForm': ct_chart_options_form,
                        'DXChartOptionsForm': dx_chart_options_form
                        }

After (abbreviated):

.. sourcecode:: python

    if request.method == 'POST':
        general_form = GeneralChartOptionsDisplayForm(request.POST)
        ct_form = CTChartOptionsDisplayForm(request.POST)
        dx_form = DXChartOptionsDisplayForm(request.POST)
        rf_form = RFChartOptionsDisplayForm(request.POST)
        if general_form.is_valid() and ct_form.is_valid() and dx_form.is_valid() and rf_form.is_valid():
            try:
                # See if the user has plot settings in userprofile
                user_profile = request.user.userprofile
            except:
                # Create a default userprofile for the user if one doesn't exist
                create_user_profile(sender=request.user, instance=request.user, created=True)
                user_profile = request.user.userprofile

            user_profile.plotCharts = general_form.cleaned_data['plotCharts']
            ...
            ...
            user_profile.plotHistogramBins = general_form.cleaned_data['plotHistogramBins']

            user_profile.plotCTAcquisitionMeanDLP = ct_form.cleaned_data['plotCTAcquisitionMeanDLP']
            ...
            ...
            user_profile.plotCTInitialSortingChoice = ct_form.cleaned_data['plotCTInitialSortingChoice']

            user_profile.plotDXAcquisitionMeanDAP = dx_form.cleaned_data['plotDXAcquisitionMeanDAP']
            ...
            ...
            user_profile.plotDXInitialSortingChoice = dx_form.cleaned_data['plotDXInitialSortingChoice']

            user_profile.plotRFStudyPerDayAndHour = rf_form.cleaned_data['plotRFStudyPerDayAndHour']
            user_profile.plotRFStudyFreq = rf_form.cleaned_data['plotRFStudyFreq']

            user_profile.save()

        messages.success(request, "Chart options have been updated")

    ...
    ...
    
    general_form_data = {'plotCharts': user_profile.plotCharts,
                         ...
                         ...
                         'plotHistogramBins': user_profile.plotHistogramBins}

    ct_form_data = {'plotCTAcquisitionMeanDLP': user_profile.plotCTAcquisitionMeanDLP,
                    ...
                    ...
                    'plotCTInitialSortingChoice': user_profile.plotCTInitialSortingChoice}

    dx_form_data = {'plotDXAcquisitionMeanDAP': user_profile.plotDXAcquisitionMeanDAP,
                    ...
                    ...
                    'plotDXInitialSortingChoice': user_profile.plotDXInitialSortingChoice}

    rf_form_data = {'plotDXStudyPerDayAndHour': user_profile.plotDXStudyPerDayAndHour,
                    'plotRFStudyFreq': user_profile.plotRFStudyFreq}

    general_chart_options_form = GeneralChartOptionsDisplayForm(general_form_data)
    ct_chart_options_form = CTChartOptionsDisplayForm(ct_form_data)
    dx_chart_options_form = DXChartOptionsDisplayForm(dx_form_data)
    rf_chart_options_form = RFChartOptionsDisplayForm(rf_form_data)

    return_structure = {'admin': admin,
                        'GeneralChartOptionsForm': general_chart_options_form,
                        'CTChartOptionsForm': ct_chart_options_form,
                        'DXChartOptionsForm': dx_chart_options_form,
                        'RFChartOptionsForm': rf_chart_options_form,
                        }


=========================================
Additions to ``displaychartoptions.html``
=========================================

A new div needs to be added for the fluoroscopy chart options:

.. sourcecode:: html

      <div class="panel-heading">
        <h3 class="panel-title">Fluoroscopy chart options</h3>
      </div>
      <div class="panel-body">
        <table>
          {% csrf_token %}
          {{ RFChartOptionsForm }}
        </table>
        <input class="btn btn-default" name="submit" type="submit" />
      </div>

================================
Additions to ``rffiltered.html``
================================

A section of this file sets a JavaScript variable per chart. Two new ones needs
to be added.

Additions:

.. sourcecode:: html

        {% if request.user.userprofile.plotRFStudyPerDayAndHour %}
            <script>
                var plotRFStudyPerDayAndHour = true;
                result = chartWorkload('piechartStudyWorkloadDIV', 'Studies');
            </script>
        {% endif %}

        {% if request.user.userprofile.plotRFStudyFreq %}
            <script>
                var plotRFStudyFreq = true;
                var urlStartStudy = '/openrem/rf/?{% for field in filter.form %}{% if field.name != 'study_description' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&study_description=';
                result = chartFrequency('piechartStudyDIV', 'Study description frequency');
            </script>
        {% endif %}


A second section of code needs to be added to ``rffiltered.html`` to include a
DIV for the new charts:

.. sourcecode:: html

        {% if request.user.userprofile.plotRFStudyPerDayAndHour %}
            <!-- HTML to include div container for study workload -->

            <script>
                $(window).resize(function() {
                    chartSetExportSize('piechartStudyWorkloadDIV');
                    fitChartToDiv('piechartStudyWorkloadDIV');
                });
            </script>

            <div class="panel-group" id="accordion5">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 class="panel-title">
                            <a data-toggle="collapse" data-parent="#accordion5" href="#collapseStudyWorkloadPieChart" onclick="setTimeout(function() {$(document).resize();}, 0);">
                                Pie chart showing a breakdown of number of studies per weekday.
                            </a>
                        </h4>
                    </div>
                    <div id="collapseStudyWorkloadPieChart" class="panel-collapse collapse">
                        <div class="panel-body">
                            <div id="piechartStudyWorkloadDIV" style="height: auto; margin: 0 0"></div>
                            <p>Click on a segment to be taken to a pie chart showing the breakdown per hour for that weekday.</p>
                            <a onclick="enterFullScreen('collapseStudyWorkloadPieChart', 'piechartStudyWorkloadDIV')" class="btn btn-default btn-sm" role="button">Toggle fullscreen</a>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End of HTML to include div container for studies per week day pie chart -->
        {% endif %}

        {% if request.user.userprofile.plotRFStudyFreq %}
            <!-- HTML to include div container for study name pie chart -->

            <script>
                $(window).resize(function() {
                    chartSetExportSize('piechartStudyDIV');
                    fitChartToDiv('piechartStudyDIV');
                });
            </script>

            <div class="panel-group" id="accordionPiechartStudy">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h4 class="panel-title">
                            <a data-toggle="collapse" data-parent="#accordionPiechartStudy" href="#collapseStudyPieChart" onclick="setTimeout(function() {$(document).resize();}, 0);">
                                Pie chart showing a breakdown of study name frequency.
                            </a>
                        </h4>
                    </div>
                    <div id="collapseStudyPieChart" class="panel-collapse collapse">
                        <div class="panel-body">
                            <div id="piechartStudyDIV" style="height: auto; margin: 0 0"></div>
                            <a onclick="enterFullScreen('collapseStudyPieChart', 'piechartStudyDIV')" class="btn btn-default btn-sm" role="button">Toggle fullscreen</a>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End of HTML to include div container for study name pie chart -->
        {% endif %}

===============================
Additions to ``rfChartAjax.js``
===============================

This file needs to update the skeleton chart with the data that has been
provided by ``views.py``. It does this via the appropriate routines contained
in the ``chartUpdateData.js`` file. In this case, ``updateWorkloadChart`` and
``updateFrequencyChart``:

.. sourcecode:: javascript

            // Study workload chart data
            if(typeof plotRFStudyPerDayAndHour !== 'undefined') {
                updateWorkloadChart(json.studiesPerHourInWeekdays, 'piechartStudyWorkloadDIV', colour_scale);
            }

            // Study description frequency chart data start
            if(typeof plotRFStudyFreq !== 'undefined') {
                updateFrequencyChart(json.studyNameList, json.studySystemList, json.studySummary, urlStartStudy, 'piechartStudyDIV', colour_scale);
            }

That's it - you should now have two new charts visible in the fluoroscopy
filtered page.
