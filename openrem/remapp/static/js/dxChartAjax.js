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
            // DAP chart data start
            if( typeof plotDXAcquisitionMeanDAP !== 'undefined' || typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {

                var acq_summary = $.map(json.acquisitionSummary, function (el) {
                    return el;
                });

                var protocolNames = $.map(json.acquisition_names, function (el) {
                    return el.acquisition_protocol;
                });
            }

            if(typeof plotDXAcquisitionMeanDAP !== 'undefined') {
                var acq_histogram_data = json.acquisitionHistogramData;

                var protocolCounts = [];
                var protocolBins = [];
                for (i = 0; i < protocolNames.length; i++) {
                    protocolCounts.push(acq_histogram_data[i][0]);
                    protocolBins.push(acq_histogram_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var seriesData = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        seriesData.push({
                            name: protocolNames[i],
                            y: acq_summary[i].mean_dap,
                            freq: acq_summary[i].num_acq,
                            bins: protocolBins[i],
                            tooltip: protocolNames[i] + '<br>' + acq_summary[i].mean_dap.toFixed(1) + ' mean<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                if(plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var seriesMedianData = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        seriesMedianData.push({
                            name: protocolNames[i],
                            y: parseFloat(acq_summary[i].median_dap),
                            freq: acq_summary[i].num_acq,
                            bins: protocolBins[i],
                            tooltip: protocolNames[i] + '<br>' + parseFloat(acq_summary[i].median_dap).toFixed(1) + ' median<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                temp = [];
                var seriesDrilldown = [];
                for (i = 0; i < protocolNames.length; i++) {
                    temp = [];
                    for (j = 0; j < protocolCounts[0].length; j++) {
                        temp.push([protocolBins[i][j].toFixed(1).toString() + ' \u2264 x < ' + protocolBins[i][j+1].toFixed(1).toString(), protocolCounts[i][j]]);
                    }
                    seriesDrilldown.push({id: protocolNames[i], name: protocolNames[i], useHTML: true, data: temp});
                }

                var chartplotDXAcquisitionDAP = $('#container').highcharts();
                chartplotDXAcquisitionDAP.xAxis[0].setCategories(protocolNames);
                chartplotDXAcquisitionDAP.options.drilldown.series = seriesDrilldown;
                chartplotDXAcquisitionDAP.options.exporting.sourceWidth = $(window).width();
                chartplotDXAcquisitionDAP.options.exporting.sourceHeight = $(window).height();
                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesData
                    });
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesMedianData
                    });
                }
                else {
                    chartplotDXAcquisitionDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesData
                    });
                    chartplotDXAcquisitionDAP.series[1].update({
                        color: colourScale(1).hex(),
                        data: seriesMedianData
                    });
                }
                chartplotDXAcquisitionDAP.redraw({ duration: 1000 });
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

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < request_system_names.length; i++) {
                        if (chartplotDXRequestDAP.series.length > i) {
                            chartplotDXRequestDAP.series[i].update({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/(request_system_names.length)).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/(request_system_names.length)).hex()
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
                                color: colourScale(i/(request_system_names.length)).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[i],
                                data: request_data_median[i],
                                color: colourScale(i/(request_system_names.length)).hex()
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
                                color: colourScale(i/(request_system_names.length*2)).hex()
                            });
                            chartplotDXRequestDAP.series[i+1].update({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(request_system_names.length*2)).hex()
                            });
                        }
                        else {
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data[current_series],
                                color: colourScale(i/(request_system_names.length*2)).hex()
                            });
                            chartplotDXRequestDAP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(request_system_names.length*2)).hex()
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

                var study_summary = $.map(json.studySummary, function (el) {
                    return el;
                });

                var studyNames = $.map(json.study_names, function (el) {
                    return el.study_description;
                });
            }
            
            if(typeof plotDXStudyMeanDAP !== 'undefined') {
                var study_histogram_data = json.studyHistogramData;

                var studyCounts = [];
                var studyBins = [];
                for (i = 0; i < studyNames.length; i++) {
                    studyCounts.push(study_histogram_data[i][0]);
                    studyBins.push(study_histogram_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var seriesData = [];
                    for (i = 0; i < studyNames.length; i++) {
                        seriesData.push({
                            name: studyNames[i],
                            y: study_summary[i].mean_dap,
                            freq: study_summary[i].num_stu,
                            bins: studyBins[i],
                            tooltip: studyNames[i] + '<br>' + study_summary[i].mean_dap.toFixed(1) + ' mean<br>(n=' + study_summary[i].num_stu + ')',
                            drilldown: studyNames[i]
                        });
                    }
                }

                if(plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var seriesMedianData = [];
                    for (i = 0; i < studyNames.length; i++) {
                        seriesMedianData.push({
                            name: studyNames[i],
                            y: parseFloat(study_summary[i].median_dap),
                            freq: study_summary[i].num_stu,
                            bins: studyBins[i],
                            tooltip: studyNames[i] + '<br>' + parseFloat(study_summary[i].median_dap).toFixed(1) + ' median<br>(n=' + study_summary[i].num_stu + ')',
                            drilldown: studyNames[i]
                        });
                    }
                }

                temp = [];
                var seriesDrilldown = [];
                for (i = 0; i < studyNames.length; i++) {
                    temp = [];
                    for (j = 0; j < studyCounts[0].length; j++) {
                        temp.push([studyBins[i][j].toFixed(1).toString() + ' \u2264 x < ' + studyBins[i][j+1].toFixed(1).toString(), studyCounts[i][j]]);
                    }
                    seriesDrilldown.push({id: studyNames[i], name: studyNames[i], useHTML: true, data: temp});
                }

                var chartplotDXStudyDAP = $('#plotDXStudyMeanDAPContainer').highcharts();
                chartplotDXStudyDAP.xAxis[0].setCategories(studyNames);
                chartplotDXStudyDAP.options.drilldown.series = seriesDrilldown;
                chartplotDXStudyDAP.options.exporting.sourceWidth = $(window).width();
                chartplotDXStudyDAP.options.exporting.sourceHeight = $(window).height();
                if(plotAverageChoice == "mean") {
                    chartplotDXStudyDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesData
                    });
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXStudyDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesMedianData
                    });
                }
                else {
                    chartplotDXStudyDAP.series[0].update({
                        color: colourScale(0).hex(),
                        data: seriesData
                    });
                    chartplotDXStudyDAP.series[1].update({
                        color: colourScale(1).hex(),
                        data: seriesMedianData
                    });
                }
                chartplotDXStudyDAP.redraw({ duration: 1000 });
            }
            // DAP per study description chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // kVp chart data start
            if( typeof plotDXAcquisitionMeankVp !== 'undefined' || typeof plotDXAcquisitionMeankVpOverTime !== 'undefined') {

                var acq_kVp_summary = $.map(json.acquisitionkVpSummary, function (el) {
                    return el;
                });

                var protocolkVpNames = [];
                for (i = 0; i < acq_kVp_summary.length; i++) {
                    protocolkVpNames.push(acq_kVp_summary[i].acquisition_protocol);
                }
            }

            if(typeof plotDXAcquisitionMeankVp !== 'undefined') {
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

                var acq_mAs_summary = $.map(json.acquisitionmAsSummary, function (el) {
                    return el;
                });

                var protocolmAsNames = [];
                for (i = 0; i < acq_mAs_summary.length; i++) {
                    protocolmAsNames.push(acq_mAs_summary[i].acquisition_protocol);
                }
            }

            if(typeof plotDXAcquisitionMeanmAs !== 'undefined') {
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
            if(typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                //var urlStart = '/openrem/dx/?{% for field in filter.form %}{% if field.name != 'acquisition_protocol' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&acquisition_protocol=';
                var protocolPiechartData = new Array(protocolNames.length);
                for(i=0; i<protocolNames.length; i++) {
                    if(typeof plotDXAcquisitionFreq !== 'undefined') {
                        protocolPiechartData[i] = {name: protocolNames[i], y: parseInt(acq_summary[i].num_acq), url: urlStartAcq + protocolNames[i]};
                    }
                    else {
                        protocolPiechartData[i] = {name:protocolNames[i], y:parseInt(i), url:urlStartAcq+protocolNames[i]};
                    }
                }

                if(typeof plotDXAcquisitionFreq !== 'undefined') {
                    protocolPiechartData.sort(sort_by_y);
                }

                for(i=0; i<protocolNames.length; i++) {
                    protocolPiechartData[i].color = colourScale(i/(protocolNames.length)).hex();
                }
            }

            if(typeof plotDXAcquisitionFreq !== 'undefined') {
                var chart = $('#piechartProtocolDIV').highcharts();
                chart.series[0].setData(protocolPiechartData);
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

                for(i=0; i<request_names.length; i++) {
                    requestPiechartData[i].color = colourScale(i/(request_names.length)).hex();
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
                var studyPiechartData = new Array(studyNames.length);
                for(i=0; i<studyNames.length; i++) {
                    studyPiechartData[i] = {name: studyNames[i], y: parseInt(study_summary[i].num_stu), url: urlStartStudy + studyNames[i]};
                }

                studyPiechartData.sort(sort_by_y);

                for(i=0; i<studyNames.length; i++) {
                    studyPiechartData[i].color = colourScale(i/(studyNames.length)).hex();
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
                var studiesPerWeekday = [];
                var dayTotal = 0;
                for (i = 0; i < 7; i++) {
                    dayTotal = 0;
                    for (j = 0; j < 24; j++) {
                        dayTotal = dayTotal + studies_per_hour_in_weekdays[i][j];
                    }
                    studiesPerWeekday[i] = dayTotal;
                }

                var studyWorkloadPieChartData = [];
                var seriesDrillDownPieChart = [];
                var tempTime;
                for (i = 0; i < 7; i++) {
                    temp = [];
                    for (j = 0; j < 24; j++) {
                        tempTime = "0" + j;
                        tempTime = tempTime.substr(tempTime.length-2);
                        temp.push({name: tempTime + ':00', y: studies_per_hour_in_weekdays[i][j], color: colourScale(j/(23)).hex()});
                    }
                    studyWorkloadPieChartData.push({
                        name: dayNames[i],
                        y: studiesPerWeekday[i],
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
                    var protocolLineColours =  new Array(protocolNames.length);
                    protocolPiechartData.sort(sort_by_name);
                    for(i=0; i<protocolNames.length; i++) {
                        protocolLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);
                }
                else {
                    var protocolLineColours = colourScale.colors(protocolNames.length);
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

                        temp.push({y:currentValue, url: urlStartAcq+protocolNames[i]+'&date_after='+date_after+'&date_before='+date_before});
                    }
                    DAPOverTime.push({name: protocolNames[i], color: protocolLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
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