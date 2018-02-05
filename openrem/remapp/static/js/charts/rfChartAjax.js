/*global arrayToURL, urlToArray, chroma, updateAverageChart, sortChartDataToDefault, hideButtonsIfOneSeries,
updateFrequencyChart, plotAverageChoice, updateWorkloadChart, urlStartStudy*/
/*eslint no-undef: "error"*/
/*eslint object-shorthand: "off" */

// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var requestData = arrayToURL(urlToArray(this.URL));

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: "/openrem/rf/chart/",
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

            // DAP per study description data
            if( typeof plotRFStudyDAP !== "undefined") {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, "plotRFStudyDAPContainer", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotRFStudyDAPContainer");
                hideButtonsIfOneSeries("plotRFStudyDAPContainer", "study_dap_series_");
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