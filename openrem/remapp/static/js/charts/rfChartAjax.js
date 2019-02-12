/* global arrayToURL, urlToArray, chroma, updateAverageChart, sortChartDataToDefault, hideButtonsIfOneSeries, updateFrequencyChart, plotAverageChoice, updateWorkloadChart, urlStartStudy, urlStartRequest, chartSortingDirection */
/*eslint no-undef: "error"*/
/*eslint object-shorthand: "off" */

// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var requestData = arrayToURL(urlToArray(this.URL));

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: Urls.rf_summary_chart_data(),
        data: requestData,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colourScale = chroma.scale("RdYlBu");

            // Study workload chart data
            if(typeof plotRFStudyPerDayAndHour !== "undefined") {
                updateWorkloadChart(json.studiesPerHourInWeekdays, "piechartStudyWorkloadDIV", colourScale);
            }

            // Study description frequency chart data start
            if(typeof plotRFStudyFreq !== "undefined") {
                updateFrequencyChart(json.studyNameList, json.studySystemList, json.studySummary, urlStartStudy, "piechartStudyDIV", colourScale);
            }

            // Requested procedure frequency chart data start
            if(typeof plotRFRequestFreq !== "undefined") {
                updateFrequencyChart(json.requestNameList, json.requestSystemList, json.requestSummary, urlStartRequest, "piechartRequestDIV", colourScale);
            }

            // DAP per study description data
            if( typeof plotRFStudyDAP !== "undefined") {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, "plotRFStudyDAPContainer", colourScale);
                /*eslint-disable no-undef*/
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotRFStudyDAPContainer");
                /*eslint-enable no-undef*/
                hideButtonsIfOneSeries("plotRFStudyDAPContainer", "study_dap_series_");
            }

            // DAP per requested procedure data
            if( typeof plotRFRequestDAP !== "undefined") {
                updateAverageChart(json.requestNameList, json.requestSystemList, json.requestSummary, json.requestHistogramData, plotAverageChoice, "plotRFRequestDAPContainer", colourScale);
                /*eslint-disable no-undef*/
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotRFRequestDAPContainer");
                /*eslint-enable no-undef*/
                hideButtonsIfOneSeries("plotRFRequestDAPContainer", "request_dap_series_");
            }

            $(".ajax-progress").hide();
        },
        error: function( xhr, status, errorThrown ) {
            $(".ajax-progress").hide();
            $(".ajax-error").show();
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }
    });
    return false;
});