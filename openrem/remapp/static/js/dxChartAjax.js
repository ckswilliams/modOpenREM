// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var request_data = ArrayToURL(URLToArray(this.URL));
    var i;

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: "/openrem/dx/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colour_scale = chroma.scale("RdYlBu");

            // Acquisition DAP chart data
            if(typeof plotDXAcquisitionMeanDAP !== "undefined") {
                updateAverageChart(json.acquisition_names, json.acquisitionSystemList, json.acquisitionSummary, json.acquisitionHistogramData, plotAverageChoice, "container", colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "container");
                hideButtonsIfOneSeries("container", "acq_dap_series_");
            }

            // DAP per requested procedure data
            if( typeof plotDXRequestMeanDAP !== "undefined") {
                updateAverageChart(json.request_names, json.requestSystemList, json.requestSummary, json.requestHistogramData, plotAverageChoice, "plotDXRequestMeanDAPContainer", colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotDXRequestMeanDAPContainer");
                hideButtonsIfOneSeries("plotDXRequestMeanDAPContainer", "req_dap_series_");
            }

            // DAP per study description data
            if( typeof plotDXStudyMeanDAP !== "undefined") {
                updateAverageChart(json.study_names, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, "plotDXStudyMeanDAPContainer", colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "plotDXStudyMeanDAPContainer");
                hideButtonsIfOneSeries("plotDXStudyMeanDAPContainer", "study_dap_series_");
            }

            // kVp chart data
            if( typeof plotDXAcquisitionMeankVp !== "undefined") {
                updateAverageChart(json.acquisition_kvp_names, json.acquisitionkVpSystemList, json.acquisitionkVpSummary, json.acquisitionHistogramkVpData, plotAverageChoice, "chartAcquisitionMeankVp", colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "chartAcquisitionMeankVp");
                hideButtonsIfOneSeries("chartAcquisitionMeankVp", "acq_kvp_series_");
            }

            // mAs chart data start
            if(typeof plotDXAcquisitionMeanmAs !== "undefined") {
                updateAverageChart(json.acquisition_mas_names, json.acquisitionmAsSystemList, json.acquisitionmAsSummary, json.acquisitionHistogrammAsData, plotAverageChoice, "chartAcquisitionMeanmAs", colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, "chartAcquisitionMeanmAs");
                hideButtonsIfOneSeries("chartAcquisitionMeanmAs", "acq_mas_series_");
            }

            // Acquisition frequency chart data
            if(typeof plotDXAcquisitionFreq !== "undefined") {
                updateFrequencyChart(json.acquisition_names, json.acquisitionSystemList, json.acquisitionSummary, urlStartAcq, "piechartProtocolDIV", colour_scale);
            }

            // Requested procedure frequency chart data
            if(typeof plotDXRequestFreq !== "undefined") {
                updateFrequencyChart(json.request_names, json.requestSystemList, json.requestSummary, urlStartReq, "piechartRequestDIV", colour_scale);
            }

            // Study description frequency chart data start
            if(typeof plotDXStudyFreq !== "undefined") {
                updateFrequencyChart(json.study_names, json.studySystemList, json.studySummary, urlStartStudy, "piechartStudyDIV", colour_scale);
            }

            var piechart_protocol_div;

            // DAP over time chart data
            if(typeof plotDXAcquisitionMeanDAPOverTime !== "undefined") {
                var acquisition_line_colours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    acquisition_line_colours = [];
                    piechart_protocol_div = $("#piechartProtocolDIV");
                    for (i = 0; i < piechart_protocol_div.highcharts().series[0].data.length; i++) {
                        acquisition_line_colours.push(piechart_protocol_div.highcharts().series[0].data.sort(sort_by_name)[i].color);
                    }
                    piechart_protocol_div.highcharts().series[0].data.sort(sort_by_y);
                }
                else acquisition_line_colours = colour_scale.colors(json.acquisition_names.length);

                var acq_dap_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeanDAPoverTime : json.acquisitionMedianDAPoverTime;
                updateOverTimeChart(json.acquisition_names, acq_dap_over_time, acquisition_line_colours, urlStartAcq, "AcquisitionMeanDAPOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeanDAPOverTimeDIV", "acq_dap_over_time_series_");
            }

            // kVp over time chart data
            if(typeof plotDXAcquisitionMeankVpOverTime !== "undefined") {
                var protocol_kvp_line_colours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    protocol_kvp_line_colours = [];
                    piechart_protocol_div = $("#piechartProtocolDIV");
                    for (i = 0; i < piechart_protocol_div.highcharts().series[0].data.length; i++) {
                        protocol_kvp_line_colours.push(piechart_protocol_div.highcharts().series[0].data.sort(sort_by_name)[i].color);
                    }
                    piechart_protocol_div.highcharts().series[0].data.sort(sort_by_y);
                }
                else protocol_kvp_line_colours = colour_scale.colors(json.acquisition_kvp_names.length);

                var acq_kvp_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeankVpoverTime : json.acquisitionMediankVpoverTime;
                updateOverTimeChart(json.acquisition_kvp_names, acq_kvp_over_time, protocol_kvp_line_colours, urlStartAcq, "AcquisitionMeankVpOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeankVpOverTimeDIV", "acq_kvp_over_time_series_");
            }

            // mAs over time chart data
            if(typeof plotDXAcquisitionMeanmAsOverTime !== "undefined") {
                var protocol_mas_line_colours;
                if (typeof plotDXAcquisitionFreq !== "undefined") {
                    protocol_mas_line_colours = [];
                    piechart_protocol_div = $("#piechartProtocolDIV");
                    for (i = 0; i < piechart_protocol_div.highcharts().series[0].data.length; i++) {
                        protocol_mas_line_colours.push(piechart_protocol_div.highcharts().series[0].data.sort(sort_by_name)[i].color);
                    }
                    piechart_protocol_div.highcharts().series[0].data.sort(sort_by_y);
                }
                else protocol_mas_line_colours = colour_scale.colors(json.acquisition_mas_names.length);

                var acq_mas_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeanmAsoverTime : json.acquisitionMedianmAsoverTime;
                updateOverTimeChart(json.acquisition_mas_names, acq_mas_over_time, protocol_mas_line_colours, urlStartAcq, "AcquisitionMeanmAsOverTimeDIV");
                hideButtonsIfOneSeries("AcquisitionMeanmAsOverTimeDIV", "acq_mas_over_time_series_");
            }

            // Study workload chart data
            if(typeof plotDXStudyPerDayAndHour !== "undefined") {
                updateWorkloadChart(json.studiesPerHourInWeekdays, "piechartStudyWorkloadDIV", colour_scale);
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
