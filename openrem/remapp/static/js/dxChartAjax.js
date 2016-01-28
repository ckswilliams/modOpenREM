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
    var i, j, temp;

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: "/openrem/dx/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // this.url contains info about which charts need to be plotted
            var plotting_info = URLToArray(this.url);

            // Initialise some colours to use for plotting
            var colourScale = chroma.scale('RdYlBu');

            //-------------------------------------------------------------------------------------
            // Acquisition DAP chart data start
            if( typeof plotDXAcquisitionMeanDAP !== 'undefined' || typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                var acquisition_summary = json.acquisitionSummary;
                var acquisition_names = json.acquisition_names;
                var acquisition_system_names = json.acquisitionSystemList;
                var acquisition_histogram_data = json.acquisitionHistogramData;
            }

            if(typeof plotDXAcquisitionMeanDAP !== 'undefined') {
                var acquisition_counts = []; while(acquisition_counts.push([]) < acquisition_system_names.length);
                var acquisition_bins = []; while(acquisition_bins.push([]) < acquisition_system_names.length);
                for (i = 0; i < acquisition_system_names.length; i++) {
                    for (j = 0; j < acquisition_names.length; j++) {
                        (acquisition_counts[i]).push(acquisition_histogram_data[i][j][0]);
                        (acquisition_bins[i]).push(acquisition_histogram_data[i][j][1]);
                    }
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var acquisition_data = []; while(acquisition_data.push([]) < acquisition_system_names.length);
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        for (j = 0; j < acquisition_names.length; j++) {
                            (acquisition_data[i]).push({
                                name: acquisition_names[j],
                                y: acquisition_summary[i][j].mean_dap,
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + acquisition_summary[i][j].mean_dap.toFixed(1) + ' mean<br>(n=' + acquisition_summary[i][j].num_acq + ')',
                                drilldown: acquisition_system_names[i]+acquisition_names[j]
                            });
                        }
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var acquisition_data_median = []; while(acquisition_data_median.push([]) < acquisition_system_names.length);
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        for (j = 0; j < acquisition_names.length; j++) {
                            (acquisition_data_median[i]).push({
                                name: acquisition_names[j],
                                y: parseFloat(acquisition_summary[i][j].median_dap),
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + parseFloat(acquisition_summary[i][j].median_dap).toFixed(1) + ' median<br>(n=' + acquisition_summary[i][j].num_acq + ')',
                                drilldown: acquisition_system_names[i]+acquisition_names[j]
                            });
                        }
                    }
                }

                temp = [];
                var series_drilldown_acquisition = [];
                for (i = 0; i < acquisition_system_names.length; i++) {
                    for (j = 0; j < acquisition_names.length; j++) {
                        temp = [];
                        for (k = 0; k < acquisition_counts[i][0].length; k++) {
                            temp.push([acquisition_bins[i][j][k].toFixed(1).toString() + ' \u2264 x < ' + acquisition_bins[i][j][k + 1].toFixed(1).toString(), acquisition_counts[i][j][k]]);
                        }
                        series_drilldown_acquisition.push({
                            id: acquisition_system_names[i]+acquisition_names[j],
                            name: acquisition_system_names[i],
                            useHTML: true,
                            data: temp
                        });
                    }
                }

                var chartPlotDXAcquisitionDAP = $('#container').highcharts();
                chartPlotDXAcquisitionDAP.xAxis[0].setCategories(acquisition_names);
                chartPlotDXAcquisitionDAP.options.drilldown.series = series_drilldown_acquisition;
                chartPlotDXAcquisitionDAP.options.exporting.sourceWidth = $(window).width();
                chartPlotDXAcquisitionDAP.options.exporting.sourceHeight = $(window).height();

                var acq_sys_colour_max = acquisition_system_names.length == 1 ? acquisition_system_names.length : acquisition_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotDXAcquisitionDAP.series.length > i) {
                            chartPlotDXAcquisitionDAP.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotDXAcquisitionDAP.addSeries({
                                name: acquisition_system_names[i],
                                data: acquisition_data[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotDXAcquisitionDAP.series.length > i) {
                            chartPlotDXAcquisitionDAP.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data_median[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotDXAcquisitionDAP.addSeries({
                                name: acquisition_system_names[i],
                                data: acquisition_data_median[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else {
                    var current_series = 0;
                    for (i = 0; i < (acquisition_system_names.length)*2; i+=2) {
                        if (chartPlotDXAcquisitionDAP.series.length > i+1) {
                            chartPlotDXAcquisitionDAP.series[i].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data[current_series],
                                color: colourScale(i/(acq_sys_colour_max*2+1)).hex()
                            });
                            chartPlotDXAcquisitionDAP.series[i+1].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_median[current_series],
                                color: colourScale((i+1)/(acq_sys_colour_max*2+1)).hex()
                            });
                        }
                        else {
                            chartPlotDXAcquisitionDAP.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data[current_series],
                                color: colourScale(i/(acq_sys_colour_max*2+1)).hex()
                            });
                            chartPlotDXAcquisitionDAP.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_median[current_series],
                                color: colourScale((i+1)/(acq_sys_colour_max*2+1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartPlotDXAcquisitionDAP.redraw({ duration: 1000 });
            }
            // DAP chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Requested procedure frequency and DAP per requested procedure data start
            if( typeof plotDXRequestMeanDAP !== 'undefined' || typeof plotDXRequestFreq !== 'undefined') {
                var request_summary = json.requestSummary;
                var request_names = json.request_names;
                var request_system_names = json.requestSystemList;
                var request_histogram_data = json.requestHistogramData;
            }
            
            if(typeof plotDXRequestMeanDAP !== 'undefined') {
                var request_counts = []; while(request_counts.push([]) < request_system_names.length);
                var request_bins = []; while(request_bins.push([]) < request_system_names.length);
                for (i = 0; i < request_system_names.length; i++) {
                    for (j = 0; j < request_names.length; j++) {
                        (request_counts[i]).push(request_histogram_data[i][j][0]);
                        (request_bins[i]).push(request_histogram_data[i][j][1]);
                    }
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var request_data = []; while(request_data.push([]) < request_system_names.length);
                    for (i = 0; i < request_system_names.length; i++) {
                        for (j = 0; j < request_names.length; j++) {
                            (request_data[i]).push({
                                name: request_names[j],
                                y: request_summary[i][j].mean_dap,
                                freq: request_summary[i][j].num_req,
                                bins: request_bins[i][j],
                                tooltip: request_system_names[i] + '<br>' + request_names[j] + '<br>' + request_summary[i][j].mean_dap.toFixed(1) + ' mean<br>(n=' + request_summary[i][j].num_req + ')',
                                drilldown: request_system_names[i]+request_names[j]
                            });
                        }
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var request_data_median = []; while(request_data_median.push([]) < request_system_names.length);
                    for (i = 0; i < request_system_names.length; i++) {
                        for (j = 0; j < request_names.length; j++) {
                            (request_data_median[i]).push({
                                name: request_names[j],
                                y: parseFloat(request_summary[i][j].median_dap),
                                freq: request_summary[i][j].num_req,
                                bins: request_bins[i][j],
                                tooltip: request_system_names[i] + '<br>' + request_names[j] + '<br>' + parseFloat(request_summary[i][j].median_dap).toFixed(1) + ' median<br>(n=' + request_summary[i][j].num_req + ')',
                                drilldown: request_system_names[i]+request_names[j]
                            });
                        }
                    }
                }

                temp = [];
                var series_drilldown_request = [];
                for (i = 0; i < request_system_names.length; i++) {
                    for (j = 0; j < request_names.length; j++) {
                        temp = [];
                        for (k = 0; k < request_counts[i][0].length; k++) {
                            temp.push([request_bins[i][j][k].toFixed(1).toString() + ' \u2264 x < ' + request_bins[i][j][k + 1].toFixed(1).toString(), request_counts[i][j][k]]);
                        }
                        series_drilldown_request.push({
                            id: request_system_names[i]+request_names[j],
                            name: request_system_names[i],
                            useHTML: true,
                            data: temp
                        });
                    }
                }

                var chartplotDXRequestDAP = $('#plotDXRequestMeanDAPContainer').highcharts();
                chartplotDXRequestDAP.xAxis[0].setCategories(request_names);
                chartplotDXRequestDAP.options.drilldown.series = series_drilldown_request;
                chartplotDXRequestDAP.options.exporting.sourceWidth = $(window).width();
                chartplotDXRequestDAP.options.exporting.sourceHeight = $(window).height();

                var req_sys_colour_max = request_system_names.length == 1 ? request_system_names.length : request_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < request_system_names.length; i++) {
                        if (chartplotDXRequestDAP.series.length > i) {
                            chartplotDXRequestDAP.series[i].update({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < request_system_names.length; i++) {
                        if (chartplotDXRequestDAP.series.length > i) {
                            chartplotDXRequestDAP.series[i].update({
                                name: request_system_names[i],
                                data: request_data_median[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[i],
                                data: request_data_median[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else {
                    var current_series = 0;
                    for (i = 0; i < (request_system_names.length)*2; i+=2) {
                        if (chartplotDXRequestDAP.series.length > i+1) {
                            chartplotDXRequestDAP.series[i].update({
                                name: request_system_names[current_series],
                                data: request_data[current_series],
                                color: colourScale(i/(req_sys_colour_max*2+1)).hex()
                            });
                            chartplotDXRequestDAP.series[i+1].update({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(req_sys_colour_max*2+1)).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data[current_series],
                                color: colourScale(i/(req_sys_colour_max*2+1)).hex()
                            });
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(req_sys_colour_max*2+1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartplotDXRequestDAP.redraw({ duration: 1000 });
            }
            // DAP per requested procedure name chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study description frequency and DAP per study description data start
            if( typeof plotDXStudyMeanDAP !== 'undefined' || typeof plotDXStudyFreq !== 'undefined') {
                var study_summary = json.studySummary
                var study_names = json.study_names;
                var study_system_names = json.studySystemList;
                var study_histogram_data = json.studyHistogramData;
            }
            
            if(typeof plotDXStudyMeanDAP !== 'undefined') {
                var study_counts = []; while(study_counts.push([]) < study_system_names.length);
                var study_bins = []; while(study_bins.push([]) < study_system_names.length);
                for (i = 0; i < study_system_names.length; i++) {
                    for (j = 0; j < study_names.length; j++) {
                        (study_counts[i]).push(study_histogram_data[i][j][0]);
                        (study_bins[i]).push(study_histogram_data[i][j][1]);
                    }
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var study_data = []; while(study_data.push([]) < study_system_names.length);
                    for (i = 0; i < study_system_names.length; i++) {
                        for (j = 0; j < study_names.length; j++) {
                            (study_data[i]).push({
                                name: study_names[j],
                                y: study_summary[i][j].mean_dap,
                                freq: study_summary[i][j].num_stu,
                                bins: study_bins[i][j],
                                tooltip: study_system_names[i] + '<br>' + study_names[j] + '<br>' + study_summary[i][j].mean_dap.toFixed(1) + ' mean<br>(n=' + study_summary[i][j].num_stu + ')',
                                drilldown: study_system_names[i]+study_names[j]
                            });
                        }
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var study_data_median = []; while(study_data_median.push([]) < study_system_names.length);
                    for (i = 0; i < study_system_names.length; i++) {
                        for (j = 0; j < study_names.length; j++) {
                            (study_data_median[i]).push({
                                name: study_names[j],
                                y: parseFloat(study_summary[i][j].median_dap),
                                freq: study_summary[i][j].num_stu,
                                bins: study_bins[i][j],
                                tooltip: study_system_names[i] + '<br>' + study_names[j] + '<br>' + parseFloat(study_summary[i][j].median_dap).toFixed(1) + ' median<br>(n=' + study_summary[i][j].num_stu + ')',
                                drilldown: study_system_names[i]+study_names[j]
                            });
                        }
                    }
                }

                temp = [];
                var series_drilldown_study = [];
                for (i = 0; i < study_system_names.length; i++) {
                    for (j = 0; j < study_names.length; j++) {
                        temp = [];
                        for (k = 0; k < study_counts[i][0].length; k++) {
                            temp.push([study_bins[i][j][k].toFixed(1).toString() + ' \u2264 x < ' + study_bins[i][j][k + 1].toFixed(1).toString(), study_counts[i][j][k]]);
                        }
                        series_drilldown_study.push({
                            id: study_system_names[i]+study_names[j],
                            name: study_system_names[i],
                            useHTML: true,
                            data: temp
                        });
                    }
                }

                var chartplotDXStudyDAP = $('#plotDXStudyMeanDAPContainer').highcharts();
                chartplotDXStudyDAP.xAxis[0].setCategories(study_names);
                chartplotDXStudyDAP.options.drilldown.series = series_drilldown_study;
                chartplotDXStudyDAP.options.exporting.sourceWidth = $(window).width();
                chartplotDXStudyDAP.options.exporting.sourceHeight = $(window).height();

                var stu_sys_colour_max = study_system_names.length == 1 ? study_system_names.length : study_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < study_system_names.length; i++) {
                        if (chartplotDXStudyDAP.series.length > i) {
                            chartplotDXStudyDAP.series[i].update({
                                name: study_system_names[i],
                                data: study_data[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartplotDXStudyDAP.addSeries({
                                name: study_system_names[i],
                                data: study_data[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < study_system_names.length; i++) {
                        if (chartplotDXStudyDAP.series.length > i) {
                            chartplotDXStudyDAP.series[i].update({
                                name: study_system_names[i],
                                data: study_data_median[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartplotDXStudyDAP.addSeries({
                                name: study_system_names[i],
                                data: study_data_median[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else {
                    var current_series = 0;
                    for (i = 0; i < (study_system_names.length)*2; i+=2) {
                        if (chartplotDXStudyDAP.series.length > i+1) {
                            chartplotDXStudyDAP.series[i].update({
                                name: study_system_names[current_series],
                                data: study_data[current_series],
                                color: colourScale(i/(stu_sys_colour_max*2+1)).hex()
                            });
                            chartplotDXStudyDAP.series[i+1].update({
                                name: study_system_names[current_series],
                                data: study_data_median[current_series],
                                color: colourScale((i+1)/(stu_sys_colour_max*2+1)).hex()
                            });
                        }
                        else {
                            chartplotDXStudyDAP.addSeries({
                                name: study_system_names[current_series],
                                data: study_data[current_series],
                                color: colourScale(i/(stu_sys_colour_max*2+1)).hex()
                            });
                            chartplotDXStudyDAP.addSeries({
                                name: study_system_names[current_series],
                                data: study_data_median[current_series],
                                color: colourScale((i+1)/(stu_sys_colour_max*2+1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartplotDXStudyDAP.redraw({ duration: 1000 });
            }
            // DAP per study description chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // kVp chart data start
            if( typeof plotDXAcquisitionMeankVp !== 'undefined' || typeof plotDXAcquisitionMeankVpOverTime !== 'undefined') {
                var protocolkVpNames = json.acquisition_kvp_names;
            }

            if(typeof plotDXAcquisitionMeankVp !== 'undefined') {
                var acq_kVp_summary = $.map(json.acquisitionkVpSummary, function (el) {
                    return el;
                });

                var acq_histogram_kVp_data = json.acquisitionHistogramkVpData;
                var protocolkVpCounts = [];
                var protocolkVpBins = [];
                for (i = 0; i < protocolkVpNames.length; i++) {
                    protocolkVpCounts.push(acq_histogram_kVp_data[i][0]);
                    protocolkVpBins.push(acq_histogram_kVp_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var serieskVpData = [];
                    for (i = 0; i < protocolkVpNames.length; i++) {
                        serieskVpData.push({
                            name: protocolkVpNames[i],
                            y: acq_kVp_summary[i].mean_kVp,
                            freq: acq_kVp_summary[i].num_acq,
                            bins: protocolkVpBins[i],
                            tooltip: protocolkVpNames[i] + '<br>' + acq_kVp_summary[i].mean_kVp.toFixed(1) + ' mean<br>(n=' + acq_kVp_summary[i].num_acq + ')',
                            drilldown: protocolkVpNames[i]
                        });
                    }
                }

                if(plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var seriesMediankVpData = [];
                    for (i = 0; i < protocolkVpNames.length; i++) {
                        seriesMediankVpData.push({
                            name: protocolkVpNames[i],
                            y: parseFloat(acq_kVp_summary[i].median_kVp),
                            freq: acq_kVp_summary[i].num_acq,
                            bins: protocolkVpBins[i],
                            tooltip: protocolkVpNames[i] + '<br>' + parseFloat(acq_kVp_summary[i].median_kVp).toFixed(1) + ' median<br>(n=' + acq_kVp_summary[i].num_acq + ')',
                            drilldown: protocolkVpNames[i]
                        });
                    }
                }

                temp = [];
                var serieskVpDrilldown = [];
                for (i = 0; i < protocolkVpNames.length; i++) {
                    temp = [];
                    for (j = 0; j < protocolkVpCounts[0].length; j++) {
                        temp.push([protocolkVpBins[i][j].toFixed(1).toString() + ' \u2264 x < ' + protocolkVpBins[i][j+1].toFixed(1).toString(), protocolkVpCounts[i][j]]);
                    }
                    serieskVpDrilldown.push({id: protocolkVpNames[i], name: protocolkVpNames[i], useHTML: true, data: temp});
                }

                var chartplotDXAcquisitionMeankVp = $('#chartAcquisitionMeankVp').highcharts();
                chartplotDXAcquisitionMeankVp.xAxis[0].setCategories(protocolkVpNames);
                chartplotDXAcquisitionMeankVp.options.drilldown.series = serieskVpDrilldown;
                chartplotDXAcquisitionMeankVp.options.exporting.sourceWidth = $(window).width();
                chartplotDXAcquisitionMeankVp.options.exporting.sourceHeight = $(window).height();

                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionMeankVp.series[0].update({
                        color: colourScale(0).hex(),
                        data: serieskVpData
                    });
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionMeankVp.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesMediankVpData
                    });
                }
                else {
                    chartplotDXAcquisitionMeankVp.series[0].update({
                        color: colourScale(0).hex(),
                        data: serieskVpData
                    });
                    chartplotDXAcquisitionMeankVp.series[1].update({
                        color: colourScale(1).hex(),
                        data: seriesMediankVpData
                    });
                }
                chartplotDXAcquisitionMeankVp.redraw({ duration: 1000 });
            }
            // kVp chart data end
            //-------------------------------------------------------------------------------------

            
            //-------------------------------------------------------------------------------------
            // mAs chart data start
            if( typeof plotDXAcquisitionMeanmAs !== 'undefined' || typeof plotDXAcquisitionMeanmAsOverTime !== 'undefined') {
                var protocolmAsNames = json.acquisition_mas_names;
            }

            if(typeof plotDXAcquisitionMeanmAs !== 'undefined') {
                var acq_mAs_summary = $.map(json.acquisitionmAsSummary, function (el) {
                    return el;
                });

                var acq_histogram_mAs_data = json.acquisitionHistogrammAsData;

                var protocolmAsCounts = [];
                var protocolmAsBins = [];
                for (i = 0; i < protocolmAsNames.length; i++) {
                    protocolmAsCounts.push(acq_histogram_mAs_data[i][0]);
                    protocolmAsBins.push(acq_histogram_mAs_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var seriesmAsData = [];
                    for (i = 0; i < protocolmAsNames.length; i++) {
                        seriesmAsData.push({
                            name: protocolmAsNames[i],
                            y: acq_mAs_summary[i].mean_mAs,
                            freq: acq_mAs_summary[i].num_acq,
                            bins: protocolmAsBins[i],
                            tooltip: protocolmAsNames[i] + '<br>' + acq_mAs_summary[i].mean_mAs.toFixed(1) + ' mean<br>(n=' + acq_mAs_summary[i].num_acq + ')',
                            drilldown: protocolmAsNames[i]
                        });
                    }
                }

                if(plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var seriesMedianmAsData = [];
                    for (i = 0; i < protocolmAsNames.length; i++) {
                        seriesMedianmAsData.push({
                            name: protocolmAsNames[i],
                            y: parseFloat(acq_mAs_summary[i].median_mAs),
                            freq: acq_mAs_summary[i].num_acq,
                            bins: protocolmAsBins[i],
                            tooltip: protocolmAsNames[i] + '<br>' + parseFloat(acq_mAs_summary[i].median_mAs).toFixed(1) + ' median<br>(n=' + acq_mAs_summary[i].num_acq + ')',
                            drilldown: protocolmAsNames[i]
                        });
                    }
                }

                temp = [];
                var seriesmAsDrilldown = [];
                for (i = 0; i < protocolmAsNames.length; i++) {
                    temp = [];
                    for (j = 0; j < protocolmAsCounts[0].length; j++) {
                        temp.push([protocolmAsBins[i][j].toFixed(1).toString() + ' \u2264 x < ' + protocolmAsBins[i][j+1].toFixed(1).toString(), protocolmAsCounts[i][j]]);
                    }
                    seriesmAsDrilldown.push({id: protocolmAsNames[i], name: protocolmAsNames[i], useHTML: true, data: temp});
                }

                var chartplotDXAcquisitionMeanmAs = $('#chartAcquisitionMeanmAs').highcharts();
                chartplotDXAcquisitionMeanmAs.xAxis[0].setCategories(protocolmAsNames);
                chartplotDXAcquisitionMeanmAs.options.drilldown.series = seriesmAsDrilldown;
                chartplotDXAcquisitionMeanmAs.options.exporting.sourceWidth = $(window).width();
                chartplotDXAcquisitionMeanmAs.options.exporting.sourceHeight = $(window).height();
                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionMeanmAs.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesmAsData
                    });
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionMeanmAs.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesMedianmAsData
                    });
                }
                else {
                    chartplotDXAcquisitionMeanmAs.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesmAsData
                    });
                    chartplotDXAcquisitionMeanmAs.series[1].update({
                        color: colourScale(1).hex(),
                        data: seriesMedianmAsData
                    });
                }
                chartplotDXAcquisitionMeanmAs.redraw({ duration: 1000 });
            }
            // mAs chart data end
            //-------------------------------------------------------------------------------------

            
            //-------------------------------------------------------------------------------------
            // Acquisition frequency chart data start
            if(typeof plotDXAcquisitionFreq !== 'undefined') {
                var acquisitionPiechartData = new Array(acquisition_names.length);
                var num_acquisitions = 0;
                for (i = 0; i < acquisition_names.length; i++) {
                    num_acquisitions = 0;
                    for (j = 0; j < acquisition_system_names.length; j++) {
                        num_acquisitions += parseInt(acquisition_summary[j][i].num_acq)
                    }
                    acquisitionPiechartData[i] = {
                        name: acquisition_names[i],
                        y: num_acquisitions,
                        url: urlStartAcq + acquisition_names[i]
                    };
                }

                acquisitionPiechartData.sort(sort_by_y);

                var acq_name_colour_max = acquisition_names.length == 1 ? acquisition_names.length : acquisition_names.length - 1;
                for(i=0; i<acquisition_names.length; i++) {
                    acquisitionPiechartData[i].color = colourScale(i/acq_name_colour_max).hex();
                }

                var chart = $('#piechartProtocolDIV').highcharts();
                chart.series[0].setData(acquisitionPiechartData);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Acquisition frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Requested procedure frequency chart data start
            if(typeof plotDXRequestFreq !== 'undefined') {
                var requestPiechartData = new Array(request_names.length);
                var num_requests = 0;
                for (i = 0; i < request_names.length; i++) {
                    num_requests = 0;
                    for (j = 0; j < request_system_names.length; j++) {
                        num_requests += parseInt(request_summary[j][i].num_req)
                    }
                    requestPiechartData[i] = {
                        name: request_names[i],
                        y: num_requests,
                        url: urlStartReq + request_names[i]
                    };
                }

                requestPiechartData.sort(sort_by_y);

                var req_name_colour_max = request_names.length == 1 ? request_names.length : request_names.length - 1;
                for(i=0; i<request_names.length; i++) {
                    requestPiechartData[i].color = colourScale(i/req_name_colour_max).hex();
                }

                var chart = $('#piechartRequestDIV').highcharts();
                chart.series[0].setData(requestPiechartData);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Requested procedure frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study description frequency chart data start
            if(typeof plotDXStudyFreq !== 'undefined') {
                var studyPiechartData = new Array(study_names.length);
                var num_studies = 0;
                for (i = 0; i < study_names.length; i++) {
                    num_studies = 0;
                    for (j = 0; j < study_system_names.length; j++) {
                        num_studies += parseInt(study_summary[j][i].num_stu)
                    }
                    studyPiechartData[i] = {
                        name: study_names[i],
                        y: num_studies,
                        url: urlStartStudy + study_names[i]
                    };
                }

                studyPiechartData.sort(sort_by_y);

                var stu_name_colour_max = study_names.length == 1 ? study_names.length : study_names.length - 1;
                for(i=0; i<study_names.length; i++) {
                    studyPiechartData[i].color = colourScale(i/stu_name_colour_max).hex();
                }

                var chart = $('#piechartStudyDIV').highcharts();
                chart.series[0].setData(studyPiechartData);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Study description frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study workload chart data start
            if(typeof plotDXStudyPerDayAndHour !== 'undefined') {
                var dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

                // A [7][24] list of integer values
                var studies_per_hour_in_weekdays = json.studiesPerHourInWeekdays;
                var dayTotal = 0;
                var studyWorkloadPieChartData = [];
                var seriesDrillDownPieChart = [];
                var tempTime;
                for (i = 0; i < 7; i++) {
                    dayTotal = 0;
                    temp = [];
                    for (j = 0; j < 24; j++) {
                        dayTotal += studies_per_hour_in_weekdays[i][j];
                        tempTime = "0" + j;
                        tempTime = tempTime.substr(tempTime.length-2);
                        temp.push({name: tempTime + ':00', y: studies_per_hour_in_weekdays[i][j], color: colourScale(j/(23)).hex()});
                    }
                    studyWorkloadPieChartData.push({
                        name: dayNames[i],
                        y: dayTotal,
                        color: colourScale(i/(6)).hex(),
                        drilldown: dayNames[i]
                    });
                    seriesDrillDownPieChart.push({
                        id: dayNames[i],
                        name: dayNames[i],
                        useHTML: true,
                        type: 'pie',
                        data: temp
                    });
                }

                var chartplotDXStudyPerDayAndHour = $('#piechartStudyWorkloadDIV').highcharts();
                chartplotDXStudyPerDayAndHour.options.drilldown.series = seriesDrillDownPieChart;
                chartplotDXStudyPerDayAndHour.series[0].setData(studyWorkloadPieChartData);
                chartplotDXStudyPerDayAndHour.options.exporting.sourceWidth = $(window).width();
                chartplotDXStudyPerDayAndHour.options.exporting.sourceHeight = $(window).height();
                chartplotDXStudyPerDayAndHour.redraw({duration: 1000});
            }
            // Study workload chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Sort out colours for the ...OverTime plots
            if(typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                if(typeof plotDXAcquisitionFreq !== 'undefined') {
                    var protocolLineColours =  new Array(acquisition_names.length);
                    protocolPiechartData.sort(sort_by_name);
                    for(i=0; i<acquisition_names.length; i++) {
                        protocolLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);
                }
                else {
                    var protocolLineColours = colourScale.colors(acquisition_names.length);
                }
            }

            if(typeof plotDXAcquisitionMeankVpOverTime !== 'undefined') {
                if(typeof plotDXAcquisitionFreq !== 'undefined') {
                    var protocolkVpLineColours =  new Array(protocolkVpNames.length);
                    protocolPiechartData.sort(sort_by_name);
                    for (i = 0; i < protocolkVpNames.length; i++) {
                        protocolkVpLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);
                }
                else {
                    var protocolkVpLineColours = colourScale.colors(protocolkVpNames.length);
                }
            }

            if(typeof plotDXAcquisitionMeanmAsOverTime !== 'undefined') {
                if(typeof protocolkVpLineColours !== 'undefined') {
                    var protocolmAsLineColours = protocolkVpLineColours;
                }
                else if(typeof plotDXAcquisitionFreq !== 'undefined') {
                    var protocolmAsLineColours =  new Array(protocolmAsNames.length);
                    protocolPiechartData.sort(sort_by_name);
                    for (i = 0; i < protocolmAsNames.length; i++) {
                        protocolmAsLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);
                }
                else {
                    var protocolmAsLineColours = colourScale.colors(protocolmAsNames.length);
                }
            }
            // End of sorting out colours for the ...OverTime plots
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // kVp over time chart data start
            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average kVp values
            if(typeof plotDXAcquisitionMeankVpOverTime !== 'undefined') {
                var kVpOverTime, acq_kvp_over_time, dateAxis, currentValue, tempDate, date_after, date_before;
                var chartDXAcquisitionMeankVpOverTime = $('#AcquisitionMeankVpOverTimeDIV').highcharts();

                acq_kvp_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeankVpoverTime : json.acquisitionMediankVpoverTime;

                dateAxis = [];
                for(i=0; i<acq_kvp_over_time[0].length; i++) {
                    tempDate = new Date(Date.parse(acq_kvp_over_time[0][i][0]));
                    tempDate = formatDate(tempDate);
                    dateAxis.push(tempDate);
                }

                kVpOverTime = [];
                for(i=0; i<acq_kvp_over_time.length; i++) {
                    temp = [];
                    for(j=0; j<acq_kvp_over_time[0].length; j++) {
                        tempDate = new Date(Date.parse(acq_kvp_over_time[i][j][0]));
                        date_after = formatDate(tempDate);
                        date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                        currentValue = parseFloat(acq_kvp_over_time[i][j][1]);
                        if(currentValue == 0) currentValue = null;

                        temp.push({y:currentValue, url: urlStartAcq+protocolkVpNames[i]+'&date_after='+date_after+'&date_before='+date_before});
                    }
                    kVpOverTime.push({name: protocolkVpNames[i], color: protocolkVpLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
                }

                chartDXAcquisitionMeankVpOverTime.xAxis[0].setCategories(dateAxis);
                for(i=0; i<kVpOverTime.length; i++) {
                    chartDXAcquisitionMeankVpOverTime.addSeries(kVpOverTime[i]);
                }

                chartDXAcquisitionMeankVpOverTime.options.exporting.sourceWidth = $(window).width();
                chartDXAcquisitionMeankVpOverTime.options.exporting.sourceHeight = $(window).height();

                chartDXAcquisitionMeankVpOverTime.redraw({duration: 1000});
            }
            // kVp over time chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // mAs over time chart data start
            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average mAs values
            if(typeof plotDXAcquisitionMeanmAsOverTime !== 'undefined') {
                var mAsOverTime, acq_mas_over_time, dateAxis, currentValue, tempDate, date_after, date_before;
                var chartDXAcquisitionMeanmAsOverTime = $('#AcquisitionMeanmAsOverTimeDIV').highcharts();

                acq_mas_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeanmAsoverTime : json.acquisitionMedianmAsoverTime;

                dateAxis = [];
                for(i=0; i<acq_mas_over_time[0].length; i++) {
                    tempDate = new Date(Date.parse(acq_mas_over_time[0][i][0]));
                    tempDate = formatDate(tempDate);
                    dateAxis.push(tempDate);
                }

                mAsOverTime = [];
                for(i=0; i<acq_mas_over_time.length; i++) {
                    temp = [];
                    for(j=0; j<acq_mas_over_time[0].length; j++) {
                        tempDate = new Date(Date.parse(acq_mas_over_time[i][j][0]));
                        date_after = formatDate(tempDate);
                        date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                        currentValue = parseFloat(acq_mas_over_time[i][j][1]);
                        if(currentValue == 0) currentValue = null;

                        temp.push({y:currentValue, url: urlStartAcq+protocolmAsNames[i]+'&date_after='+date_after+'&date_before='+date_before});
                    }
                    mAsOverTime.push({name: protocolmAsNames[i], color: protocolmAsLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
                }

                chartDXAcquisitionMeanmAsOverTime.xAxis[0].setCategories(dateAxis);
                for(i=0; i<mAsOverTime.length; i++) {
                    chartDXAcquisitionMeanmAsOverTime.addSeries(mAsOverTime[i]);
                }

                chartDXAcquisitionMeanmAsOverTime.options.exporting.sourceWidth = $(window).width();
                chartDXAcquisitionMeanmAsOverTime.options.exporting.sourceHeight = $(window).height();

                chartDXAcquisitionMeanmAsOverTime.redraw({duration: 1000});
            }
            // mAs over time chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DAP over time chart data start
            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average DAP values
            if(typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                var DAPOverTime, acq_dap_over_time, dateAxis, currentValue, tempDate, date_after, date_before;
                var chartDXAcquisitionMeanDAPOverTime = $('#AcquisitionMeanDAPOverTimeDIV').highcharts();

                acq_dap_over_time = (plotAverageChoice == "mean") ? json.acquisitionMeanDAPoverTime : json.acquisitionMedianDAPoverTime;

                dateAxis = [];
                for(i=0; i<acq_dap_over_time[0].length; i++) {
                    tempDate = new Date(Date.parse(acq_dap_over_time[0][i][0]));
                    tempDate = formatDate(tempDate);
                    dateAxis.push(tempDate);
                }

                DAPOverTime = [];
                for(i=0; i<acq_dap_over_time.length; i++) {
                    temp = [];
                    for(j=0; j<acq_dap_over_time[0].length; j++) {
                        tempDate = new Date(Date.parse(acq_dap_over_time[i][j][0]));
                        date_after = formatDate(tempDate);
                        date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                        currentValue = parseFloat(acq_dap_over_time[i][j][1]);
                        if(currentValue == 0) currentValue = null;

                        temp.push({y:currentValue, url: urlStartAcq+acquisition_names[i]+'&date_after='+date_after+'&date_before='+date_before});
                    }
                    DAPOverTime.push({name: acquisition_names[i], color: protocolLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
                }

                chartDXAcquisitionMeanDAPOverTime.xAxis[0].setCategories(dateAxis);
                for(i=0; i<DAPOverTime.length; i++) {
                    chartDXAcquisitionMeanDAPOverTime.addSeries(DAPOverTime[i]);
                }

                chartDXAcquisitionMeanDAPOverTime.options.exporting.sourceWidth = $(window).width();
                chartDXAcquisitionMeanDAPOverTime.options.exporting.sourceHeight = $(window).height();

                chartDXAcquisitionMeanDAPOverTime.redraw({duration: 1000});
            }
            // DAP over time chart data end
            //-------------------------------------------------------------------------------------

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