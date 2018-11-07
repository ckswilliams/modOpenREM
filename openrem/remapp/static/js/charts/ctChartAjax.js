/*global arrayToURL, urlToArray, chroma, updateAverageChart, sortChartDataToDefault, hideButtonsIfOneSeries,
updateFrequencyChart, sortByY, sortByName, plotAverageChoice, updateWorkloadChart, chartSorting, urlStartAcq,
urlStartReq, urlStartStudy, updateOverTimeChart, chartSortingDirection*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */
/*eslint object-shorthand: "off" */

// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var requestData = arrayToURL(urlToArray(this.URL));
    var i;

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: Urls.ct_summary_chart_data(),
        data: requestData,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colourScale = chroma.scale("RdYlBu");

            // DLP per acquisition chart data
            if(typeof plotCTAcquisitionMeanDLP !== "undefined") {
                updateAverageChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummary, json.acquisitionHistogramData, plotAverageChoice, "histogramAcquisitionPlotDLPdiv", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "histogramAcquisitionPlotDLPdiv");
                hideButtonsIfOneSeries("histogramAcquisitionPlotDLPdiv", "acq_dlp_series_");
            }

            // CTDI per acquisition chart data
            if(typeof plotCTAcquisitionMeanCTDI !== "undefined") {
                updateAverageChart(json.acquisitionNameListCTDI, json.acquisitionSystemListCTDI, json.acquisitionSummaryCTDI, json.acquisitionHistogramDataCTDI, plotAverageChoice, "histogramAcquisitionPlotCTDIdiv", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "histogramAcquisitionPlotCTDIdiv");
                hideButtonsIfOneSeries("histogramAcquisitionPlotCTDIdiv", "acq_ctdi_series_");
            }

            // DLP per study chart data
            if(typeof plotCTStudyMeanDLP !== "undefined") {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, "histogramStudyPlotDIV", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "histogramStudyPlotDIV");
                hideButtonsIfOneSeries("histogramStudyPlotDIV", "study_dlp_series_");
            }

            // CTDI per study chart data
            if(typeof plotCTStudyMeanCTDI !== "undefined") {
                updateAverageChart(json.studyNameListCTDI, json.studySystemListCTDI, json.studySummaryCTDI, json.studyHistogramDataCTDI, plotAverageChoice, "histogramStudyPlotCTDIdiv", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "histogramStudyPlotCTDIdiv");
                hideButtonsIfOneSeries("histogramStudyPlotCTDIdiv", "study_ctdi_series_");
            }

            // DLP per request chart data start
            if(typeof plotCTRequestMeanDLP !== "undefined") {
                updateAverageChart(json.requestNameList, json.requestSystemList, json.requestSummary, json.requestHistogramData, plotAverageChoice, "histogramRequestPlotDIV", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "histogramRequestPlotDIV");
                hideButtonsIfOneSeries("histogramRequestPlotDIV", "req_dlp_series_");
            }

            // Number of events per study chart data
            if(typeof plotCTStudyNumEvents !== "undefined") {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummaryNumEvents, json.studyHistogramDataNumEvents, plotAverageChoice, "studyNumEventsDIV", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "studyNumEventsDIV");
            }

            // Number of events per request chart data
            if(typeof plotCTRequestNumEvents !== "undefined") {
                updateAverageChart(json.requestNameList, json.requestSystemList, json.requestSummaryNumEvents, json.requestHistogramDataNumEvents, plotAverageChoice, "requestPlotNumEventsDIV", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "requestPlotNumEventsDIV");
            }

            // Acquisition frequency chart data start
            if(typeof plotCTAcquisitionFreq !== "undefined" && typeof plotCTAcquisitionMeanCTDI !== "undefined") {
                updateFrequencyChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummaryCTDI, urlStartAcq, "piechartAcquisitionDIV", colourScale);
            }
            else if(typeof plotCTAcquisitionFreq !== "undefined") {
                updateFrequencyChart(json.acquisitionNameList, json.acquisitionSystemList, json.acquisitionSummary, urlStartAcq, "piechartAcquisitionDIV", colourScale);
            }

            // Study frequency chart data start
            if(typeof plotCTStudyFreq !== "undefined") {
                updateFrequencyChart(json.studyNameList, json.studySystemList, json.studySummary, urlStartStudy, "piechartStudyDIV", colourScale);
            }

            // Study frequency chart data start
            if(typeof plotCTRequestFreq !== "undefined") {
                updateFrequencyChart(json.requestNameList, json.requestSystemList, json.requestSummary, urlStartReq, "piechartRequestDIV", colourScale);
            }

            // DLP over time chart data
            if(typeof plotCTStudyMeanDLPOverTime !== "undefined") {
                var studyLineColours = new Array(json.studyNameList.length);
                if (typeof plotCTStudyFreq !== "undefined") {
                    studyLineColours = [];
                    var piechartStudyDiv = $("#piechartStudyDIV");
                    for (i = 0; i < piechartStudyDiv.highcharts().series[0].data.length; i++) {
                        studyLineColours.push(piechartStudyDiv.highcharts().series[0].data.sort(sortByName)[i].color);
                    }
                    piechartStudyDiv.highcharts().series[0].data.sort(sortByY);
                }
                else {studyLineColours = colourScale.colors(json.studyNameList.length);}

                var studyDlpOverTime = (plotAverageChoice === "mean") ? json.studyMeanDLPoverTime : json.studyMedianDLPoverTime;
                updateOverTimeChart(json.studyNameList, studyDlpOverTime, studyLineColours, urlStartStudyOverTime, "studyMeanDLPOverTimeDIV");
                hideButtonsIfOneSeries("studyMeanDLPOverTimeDIV", "study_dlp_time_series_");
            }

            // Study workload chart data
            if(typeof plotCTStudyPerDayAndHour !== "undefined") {
                updateWorkloadChart(json.studiesPerHourInWeekdays, "piechartStudyWorkloadDIV", colourScale);
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