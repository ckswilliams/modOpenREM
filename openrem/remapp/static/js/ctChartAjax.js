function URLToArray(url) {
    var request = {};
    var pairs = url.substring(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < pairs.length; i++) {
        if(!pairs[i])
            continue;
        var pair = pairs[i].split('=');
        request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]).replace(/\+/g, ' ');
    }
    return request;
}


function ArrayToURL(array) {
    var pairs = [];
    for (var key in array)
        if (array.hasOwnProperty(key))
            pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(array[key]));
    return pairs.join('&');
}


// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var request_data = ArrayToURL(URLToArray(this.URL));
    var i;

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: "/openrem/ct/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colour_scale = chroma.scale('RdYlBu');

            // DLP per acquisition chart data
            if(typeof plotCTAcquisitionMeanDLP !== 'undefined') {
                updateAverageChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummary, json.acquisitionHistogramData, plotAverageChoice, 'histogramAcquisitionPlotDLPdiv', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'histogramAcquisitionPlotDLPdiv');
            }

            // CTDI per acquisition chart data
            if(typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                updateAverageChart(json.acquisitionNameListCTDI, json.acquisitionSystemListCTDI, json.acquisitionSummaryCTDI, json.acquisitionHistogramDataCTDI, plotAverageChoice, 'histogramAcquisitionPlotCTDIdiv', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'histogramAcquisitionPlotCTDIdiv');
            }

            // DLP per study chart data
            if(typeof plotCTStudyMeanDLP !== 'undefined') {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, 'histogramStudyPlotDIV', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'histogramStudyPlotDIV');
            }

            // CTDI per study chart data
            if(typeof plotCTStudyMeanCTDI !== 'undefined') {
                updateAverageChart(json.studyNameListCTDI, json.studySystemListCTDI, json.studySummaryCTDI, json.studyHistogramDataCTDI, plotAverageChoice, 'histogramStudyPlotCTDIdiv', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'histogramStudyPlotCTDIdiv');
            }

            // DLP per request chart data start
            if(typeof plotCTRequestMeanDLP !== 'undefined') {
                updateAverageChart(json.requestNameList, json.requestSystemList, json.requestSummary, json.requestHistogramData, plotAverageChoice, 'histogramRequestPlotDIV', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'histogramRequestPlotDIV');
            }

            // Acquisition frequency chart data start
            if(typeof plotCTAcquisitionFreq !== 'undefined' && typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                updateFrequencyChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummaryCTDI, urlStartAcq, 'piechartAcquisitionDIV', colour_scale);
            }
            else if(typeof plotCTAcquisitionFreq !== 'undefined') {
                updateFrequencyChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummary, urlStartAcq, 'piechartAcquisitionDIV', colour_scale);
            }

            // Study frequency chart data start
            if(typeof plotCTStudyFreq !== 'undefined') {
                updateFrequencyChart(json.studyNameList, json.studySystemList, json.studySummary, urlStartStudy, 'piechartStudyDIV', colour_scale);
            }

            // Study frequency chart data start
            if(typeof plotCTRequestFreq !== 'undefined') {
                updateFrequencyChart(json.requestNameList, json.requestSystemList, json.requestSummary, urlStartReq, 'piechartRequestDIV', colour_scale);
            }

            // DLP over time chart data
            if(typeof plotCTStudyMeanDLPOverTime !== 'undefined') {
                var study_line_colours = new Array(json.studyNameList.length);
                if (typeof plotCTStudyFreq !== 'undefined') {
                    study_line_colours = [];
                    var piechart_study_div = $('#piechartStudyDIV');
                    for (i = 0; i < piechart_study_div.highcharts().series[0].data.length; i++) {
                        study_line_colours.push(piechart_study_div.highcharts().series[0].data.sort(sort_by_name)[i].color);
                    }
                    piechart_study_div.highcharts().series[0].data.sort(sort_by_y);
                }
                else study_line_colours = colour_scale.colors(json.studyNameList.length);

                var study_dlp_over_time = (plotAverageChoice == "mean") ? json.studyMeanDLPoverTime : json.studyMedianDLPoverTime;
                updateOverTimeChart(json.studyNameList, study_dlp_over_time, study_line_colours, urlStartStudyOverTime, 'studyMeanDLPOverTimeDIV');
            }

            // Study workload chart data
            if(typeof plotCTStudyPerDayAndHour !== 'undefined') {
                updateWorkloadChart(json.studiesPerHourInWeekdays, 'piechartStudyWorkloadDIV', colour_scale);
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