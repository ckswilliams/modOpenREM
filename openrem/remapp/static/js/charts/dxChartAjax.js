/*global arrayToURL, urlToArray, chroma, updateAverageChart, sortChartDataToDefault, hideButtonsIfOneSeries,
updateFrequencyChart, sortByY, sortByName, plotAverageChoice, updateWorkloadChart, updateOverTimeChart, urlStartAcq,
urlStartReq, urlStartStudy*/
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
        url: Urls.dx_summary_chart_data(),
        data: requestData,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colourScale = chroma.scale("RdYlBu");

            // Acquisition DAP chart data
            if(typeof plotDXAcquisitionMeanDAP !== "undefined") {
                updateAverageChart(json.acquisition_names, json.acquisitionSystemList, json.acquisitionSummary, json.acquisitionHistogramData, plotAverageChoice, "container", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "container");
                hideButtonsIfOneSeries("container", "acq_dap_series_");
            }

            // DAP per requested procedure data
            if( typeof plotDXRequestMeanDAP !== "undefined") {
                updateAverageChart(json.request_names, json.requestSystemList, json.requestSummary, json.requestHistogramData, plotAverageChoice, "plotDXRequestMeanDAPContainer", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotDXRequestMeanDAPContainer");
                hideButtonsIfOneSeries("plotDXRequestMeanDAPContainer", "req_dap_series_");
            }

            // DAP per study description data
            if( typeof plotDXStudyMeanDAP !== "undefined") {
                updateAverageChart(json.study_names, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, "plotDXStudyMeanDAPContainer", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotDXStudyMeanDAPContainer");
                hideButtonsIfOneSeries("plotDXStudyMeanDAPContainer", "study_dap_series_");
            }

            // kVp chart data
            if( typeof plotDXAcquisitionMeankVp !== "undefined") {
                updateAverageChart(json.acquisition_kvp_names, json.acquisitionkVpSystemList, json.acquisitionkVpSummary, json.acquisitionHistogramkVpData, plotAverageChoice, "chartAcquisitionMeankVp", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "chartAcquisitionMeankVp");
                hideButtonsIfOneSeries("chartAcquisitionMeankVp", "acq_kvp_series_");
            }

            // mAs chart data start
            if(typeof plotDXAcquisitionMeanmAs !== "undefined") {
                updateAverageChart(json.acquisition_mas_names, json.acquisitionmAsSystemList, json.acquisitionmAsSummary, json.acquisitionHistogrammAsData, plotAverageChoice, "chartAcquisitionMeanmAs", colourScale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "chartAcquisitionMeanmAs");
                hideButtonsIfOneSeries("chartAcquisitionMeanmAs", "acq_mas_series_");
            }

            // Acquisition frequency chart data
            if(typeof plotDXAcquisitionFreq !== "undefined") {
                updateFrequencyChart(json.acquisition_names, json.acquisitionSystemList, json.acquisitionSummary, urlStartAcq, "piechartProtocolDIV", colourScale);
            }

            // Requested procedure frequency chart data
            if(typeof plotDXRequestFreq !== "undefined") {
                updateFrequencyChart(json.request_names, json.requestSystemList, json.requestSummary, urlStartReq, "piechartRequestDIV", colourScale);
            }

            // Study description frequency chart data start
            if(typeof plotDXStudyFreq !== "undefined") {
                updateFrequencyChart(json.study_names, json.studySystemList, json.studySummary, urlStartStudy, "piechartStudyDIV", colourScale);
            }

            var piechartProtocolDiv;

            // DAP over time chart data
            if(typeof plotDXAcquisitionMeanDAPOverTime !== "undefined") {
                var acquisitionLineColours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    acquisitionLineColours = [];
                    piechartProtocolDiv = $("#piechartProtocolDIV");
                    for (i = 0; i < piechartProtocolDiv.highcharts().series[0].data.length; i++) {
                        acquisitionLineColours.push(piechartProtocolDiv.highcharts().series[0].data.sort(sortByName)[i].color);
                    }
                    piechartProtocolDiv.highcharts().series[0].data.sort(sortByY);
                }
                else {acquisitionLineColours = colourScale.colors(json.acquisition_names.length);}

                var acqDapOverTime = (plotAverageChoice === "mean") ? json.acquisitionMeanDAPoverTime : json.acquisitionMedianDAPoverTime;
                updateOverTimeChart(json.acquisition_names, acqDapOverTime, acquisitionLineColours, urlStartAcq, "AcquisitionMeanDAPOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeanDAPOverTimeDIV", "acq_dap_over_time_series_");
            }

            // kVp over time chart data
            if(typeof plotDXAcquisitionMeankVpOverTime !== "undefined") {
                var protocolKvpLineColours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    protocolKvpLineColours = [];
                    piechartProtocolDiv = $("#piechartProtocolDIV");
                    for (i = 0; i < piechartProtocolDiv.highcharts().series[0].data.length; i++) {
                        protocolKvpLineColours.push(piechartProtocolDiv.highcharts().series[0].data.sort(sortByName)[i].color);
                    }
                    piechartProtocolDiv.highcharts().series[0].data.sort(sortByY);
                }
                else {protocolKvpLineColours = colourScale.colors(json.acquisition_kvp_names.length);}

                var acqKvpOverTime = (plotAverageChoice === "mean") ? json.acquisitionMeankVpoverTime : json.acquisitionMediankVpoverTime;
                updateOverTimeChart(json.acquisition_kvp_names, acqKvpOverTime, protocolKvpLineColours, urlStartAcq, "AcquisitionMeankVpOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeankVpOverTimeDIV", "acq_kvp_over_time_series_");
            }

            // mAs over time chart data
            if(typeof plotDXAcquisitionMeanmAsOverTime !== "undefined") {
                var protocolMasLineColours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    protocolMasLineColours = [];
                    piechartProtocolDiv = $("#piechartProtocolDIV");
                    for (i = 0; i < piechartProtocolDiv.highcharts().series[0].data.length; i++) {
                        protocolMasLineColours.push(piechartProtocolDiv.highcharts().series[0].data.sort(sortByName)[i].color);
                    }
                    piechartProtocolDiv.highcharts().series[0].data.sort(sortByY);
                }
                else {protocolMasLineColours = colourScale.colors(json.acquisition_mas_names.length);}

                var acqMasOverTime = (plotAverageChoice === "mean") ? json.acquisitionMeanmAsoverTime : json.acquisitionMedianmAsoverTime;
                updateOverTimeChart(json.acquisition_mas_names, acqMasOverTime, protocolMasLineColours, urlStartAcq, "AcquisitionMeanmAsOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeanmAsOverTimeDIV", "acq_mas_over_time_series_");
            }

            // Study workload chart data
            if(typeof plotDXStudyPerDayAndHour !== "undefined") {
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
