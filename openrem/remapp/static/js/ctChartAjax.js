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
        url: "/openrem/ct/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // this.url contains info about which charts need to be plotted
            var plotting_info = URLToArray(this.url);

            // Initialise some colours to use for plotting
            var colourScale = chroma.scale('RdYlBu');

            //-------------------------------------------------------------------------------------
            // DLP per acquisition chart data start
            if( typeof plotCTAcquisitionMeanDLP !== 'undefined' || typeof plotCTAcquisitionFreq !== 'undefined' || typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                var acquisition_names = json.acquisitionNameList;
                var acquisition_system_names = json.acquisitionSystemList;
                var acquisition_summary = json.acquisitionSummary;
            }

            if(typeof plotCTAcquisitionMeanDLP !== 'undefined') {
                var acquisition_histogram_data = json.acquisitionHistogramData;
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
                                y: acquisition_summary[i][j].mean_dlp,
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + acquisition_summary[i][j].mean_dlp.toFixed(1) + ' mean<br>(n=' + acquisition_summary[i][j].num_acq + ')',
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
                                y: parseFloat(acquisition_summary[i][j].median_dlp),
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + parseFloat(acquisition_summary[i][j].median_dlp).toFixed(1) + ' median<br>(n=' + acquisition_summary[i][j].num_acq + ')',
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

                var chartPlotCTAcquisitionMeanDLP = $('#histogramAcquisitionPlotDLPdiv').highcharts();
                chartPlotCTAcquisitionMeanDLP.xAxis[0].setCategories(acquisition_names);
                chartPlotCTAcquisitionMeanDLP.options.drilldown.series = series_drilldown_acquisition;
                chartPlotCTAcquisitionMeanDLP.options.exporting.sourceWidth = $(window).width();
                chartPlotCTAcquisitionMeanDLP.options.exporting.sourceHeight = $(window).height();

                var acq_sys_colour_max = acquisition_system_names.length == 1 ? acquisition_system_names.length : acquisition_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotCTAcquisitionMeanDLP.series.length > i) {
                            chartPlotCTAcquisitionMeanDLP.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanDLP.addSeries({
                                name: acquisition_system_names[i],
                                data: acquisition_data[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotCTAcquisitionMeanDLP.series.length > i) {
                            chartPlotCTAcquisitionMeanDLP.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data_median[i],
                                color: colourScale(i/acq_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanDLP.addSeries({
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
                        if (chartPlotCTAcquisitionMeanDLP.series.length > i+1) {
                            chartPlotCTAcquisitionMeanDLP.series[i].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data[current_series],
                                color: colourScale(i/(acq_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTAcquisitionMeanDLP.series[i+1].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_median[current_series],
                                color: colourScale((i+1)/(acq_sys_colour_max*2-1)).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanDLP.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data[current_series],
                                color: colourScale(i/(acq_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTAcquisitionMeanDLP.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_median[current_series],
                                color: colourScale((i+1)/(acq_sys_colour_max*2-1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartPlotCTAcquisitionMeanDLP.redraw({duration: 1000});
            }
            // DLP per acquisition chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // CTDI per acquisition chart data start
            if(typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                var acquisition_histogram_data_ctdi = json.acquisitionHistogramDataCTDI;
                var acquisition_counts_ctdi = []; while(acquisition_counts_ctdi.push([]) < acquisition_system_names.length);
                var acquisition_bins_ctdi = []; while(acquisition_bins_ctdi.push([]) < acquisition_system_names.length);
                for (i = 0; i < acquisition_system_names.length; i++) {
                    for (j = 0; j < acquisition_names.length; j++) {
                        (acquisition_counts_ctdi[i]).push(acquisition_histogram_data_ctdi[i][j][0]);
                        (acquisition_bins_ctdi[i]).push(acquisition_histogram_data_ctdi[i][j][1]);
                    }
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var acquisition_data_ctdi = []; while(acquisition_data_ctdi.push([]) < acquisition_system_names.length);
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        for (j = 0; j < acquisition_names.length; j++) {
                            (acquisition_data_ctdi[i]).push({
                                name: acquisition_names[j],
                                y: acquisition_summary[i][j].mean_ctdi,
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins_ctdi[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + acquisition_summary[i][j].mean_ctdi.toFixed(1) + ' mean<br>(n=' + acquisition_summary[i][j].num_acq + ')',
                                drilldown: acquisition_system_names[i]+acquisition_names[j]
                            });
                        }
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var acquisition_data_ctdimedian = []; while(acquisition_data_ctdimedian.push([]) < acquisition_system_names.length);
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        for (j = 0; j < acquisition_names.length; j++) {
                            (acquisition_data_ctdimedian[i]).push({
                                name: acquisition_names[j],
                                y: parseFloat(acquisition_summary[i][j].median_ctdi),
                                freq: acquisition_summary[i][j].num_acq,
                                bins: acquisition_bins_ctdi[i][j],
                                tooltip: acquisition_system_names[i] + '<br>' + acquisition_names[j] + '<br>' + parseFloat(acquisition_summary[i][j].median_ctdi).toFixed(1) + ' median<br>(n=' + acquisition_summary[i][j].num_acq + ')',
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
                        for (k = 0; k < acquisition_counts_ctdi[i][0].length; k++) {
                            temp.push([acquisition_bins_ctdi[i][j][k].toFixed(1).toString() + ' \u2264 x < ' + acquisition_bins_ctdi[i][j][k + 1].toFixed(1).toString(), acquisition_counts_ctdi[i][j][k]]);
                        }
                        series_drilldown_acquisition.push({
                            id: acquisition_system_names[i]+acquisition_names[j],
                            name: acquisition_system_names[i],
                            useHTML: true,
                            data: temp
                        });
                    }
                }

                var chartPlotCTAcquisitionMeanCTDI = $('#histogramAcquisitionPlotCTDIdiv').highcharts();
                chartPlotCTAcquisitionMeanCTDI.xAxis[0].setCategories(acquisition_names);
                chartPlotCTAcquisitionMeanCTDI.options.drilldown.series = series_drilldown_acquisition;
                chartPlotCTAcquisitionMeanCTDI.options.exporting.sourceWidth = $(window).width();
                chartPlotCTAcquisitionMeanCTDI.options.exporting.sourceHeight = $(window).height();

                var acq_ctdi_sys_colour_max = acquisition_system_names.length == 1 ? acquisition_system_names.length : acquisition_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotCTAcquisitionMeanCTDI.series.length > i) {
                            chartPlotCTAcquisitionMeanCTDI.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data_ctdi[i],
                                color: colourScale(i/acq_ctdi_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanCTDI.addSeries({
                                name: acquisition_system_names[i],
                                data: acquisition_data_ctdi[i],
                                color: colourScale(i/acq_ctdi_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < acquisition_system_names.length; i++) {
                        if (chartPlotCTAcquisitionMeanCTDI.series.length > i) {
                            chartPlotCTAcquisitionMeanCTDI.series[i].update({
                                name: acquisition_system_names[i],
                                data: acquisition_data_ctdimedian[i],
                                color: colourScale(i/acq_ctdi_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanCTDI.addSeries({
                                name: acquisition_system_names[i],
                                data: acquisition_data_ctdimedian[i],
                                color: colourScale(i/acq_ctdi_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else {
                    var current_series = 0;
                    for (i = 0; i < (acquisition_system_names.length)*2; i+=2) {
                        if (chartPlotCTAcquisitionMeanCTDI.series.length > i+1) {
                            chartPlotCTAcquisitionMeanCTDI.series[i].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_ctdi[current_series],
                                color: colourScale(i/(acq_ctdi_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTAcquisitionMeanCTDI.series[i+1].update({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_ctdimedian[current_series],
                                color: colourScale((i+1)/(acq_ctdi_sys_colour_max*2-1)).hex()
                            });
                        }
                        else {
                            chartPlotCTAcquisitionMeanCTDI.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_ctdi[current_series],
                                color: colourScale(i/(acq_ctdi_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTAcquisitionMeanCTDI.addSeries({
                                name: acquisition_system_names[current_series],
                                data: acquisition_data_ctdimedian[current_series],
                                color: colourScale((i+1)/(acq_ctdi_sys_colour_max*2-1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartPlotCTAcquisitionMeanCTDI.redraw({duration: 1000});
            }
            // CTDI per acquisition chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Acquisition frequency chart data start
            if(typeof plotCTAcquisitionFreq !== 'undefined') {
                var acquisition_piechart_data = new Array(acquisition_names.length);
                var num_acq = 0;
                for (i = 0; i < acquisition_names.length; i++) {
                    num_acq = 0;
                    for (j = 0; j < acquisition_system_names.length; j++) {
                        num_acq += parseInt(acquisition_summary[j][i].num_acq)
                    }
                    acquisition_piechart_data[i] = {
                        name: acquisition_names[i],
                        y: num_acq,
                        url: urlStartAcq + acquisition_names[i]
                    };
                }

                if(typeof plotCTAcquisitionFreq !== 'undefined') {
                    acquisition_piechart_data.sort(sort_by_y);
                }

                var acq_name_colour_max = acquisition_names.length == 1 ? acquisition_names.length : acquisition_names.length - 1;

                for(i=0; i<acquisition_names.length; i++) {
                    acquisition_piechart_data[i].color = colourScale(i/acq_name_colour_max).hex();
                }
            }

            if(typeof plotCTAcquisitionFreq !== 'undefined') {
                var chart = $('#piechartAcquisitionDIV').highcharts();
                chart.series[0].setData(acquisition_piechart_data);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Acquisition frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DLP per study chart data start
            if( typeof plotCTStudyMeanDLP !== 'undefined' || typeof plotCTStudyFreq !== 'undefined' || typeof plotCTStudyMeanDLPOverTime !== 'undefined') {
                var study_names = json.studyNameList;
                var study_system_names = json.studySystemList;
                var study_summary = json.studySummary;
            }

            if(typeof plotCTStudyMeanDLP !== 'undefined') {
                var study_histogram_data = json.studyHistogramData;
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
                                y: study_summary[i][j].mean_dlp,
                                freq: study_summary[i][j].num_stu,
                                bins: study_bins[i][j],
                                tooltip: study_system_names[i] + '<br>' + study_names[j] + '<br>' + study_summary[i][j].mean_dlp.toFixed(1) + ' mean<br>(n=' + study_summary[i][j].num_stu + ')',
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
                                y: parseFloat(study_summary[i][j].median_dlp),
                                freq: study_summary[i][j].num_stu,
                                bins: study_bins[i][j],
                                tooltip: study_system_names[i] + '<br>' + study_names[j] + '<br>' + parseFloat(study_summary[i][j].median_dlp).toFixed(1) + ' median<br>(n=' + study_summary[i][j].num_stu + ')',
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

                var chartPlotCTStudyMeanDLP = $('#histogramStudyPlotDIV').highcharts();
                chartPlotCTStudyMeanDLP.xAxis[0].setCategories(study_names);
                chartPlotCTStudyMeanDLP.options.drilldown.series = series_drilldown_study;
                chartPlotCTStudyMeanDLP.options.exporting.sourceWidth = $(window).width();
                chartPlotCTStudyMeanDLP.options.exporting.sourceHeight = $(window).height();

                var stu_sys_colour_max = study_system_names.length == 1 ? study_system_names.length : study_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < study_system_names.length; i++) {
                        if (chartPlotCTStudyMeanDLP.series.length > i) {
                            chartPlotCTStudyMeanDLP.series[i].update({
                                name: study_system_names[i],
                                data: study_data[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTStudyMeanDLP.addSeries({
                                name: study_system_names[i],
                                data: study_data[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < study_system_names.length; i++) {
                        if (chartPlotCTStudyMeanDLP.series.length > i) {
                            chartPlotCTStudyMeanDLP.series[i].update({
                                name: study_system_names[i],
                                data: study_data_median[i],
                                color: colourScale(i/stu_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTStudyMeanDLP.addSeries({
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
                        if (chartPlotCTStudyMeanDLP.series.length > i+1) {
                            chartPlotCTStudyMeanDLP.series[i].update({
                                name: study_system_names[current_series],
                                data: study_data[current_series],
                                color: colourScale(i/(stu_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTStudyMeanDLP.series[i+1].update({
                                name: study_system_names[current_series],
                                data: study_data_median[current_series],
                                color: colourScale((i+1)/(stu_sys_colour_max*2-1)).hex()
                            });
                        }
                        else {
                            chartPlotCTStudyMeanDLP.addSeries({
                                name: study_system_names[current_series],
                                data: study_data[current_series],
                                color: colourScale(i/(stu_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTStudyMeanDLP.addSeries({
                                name: study_system_names[current_series],
                                data: study_data_median[current_series],
                                color: colourScale((i+1)/(stu_sys_colour_max*2-1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartPlotCTStudyMeanDLP.redraw({duration: 1000});
            }
            // DLP per study chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study frequency chart data start
            if(typeof plotCTStudyFreq !== 'undefined' || typeof plotCTStudyMeanDLPOverTime !== 'undefined') {
                var study_piechart_data = new Array(study_names.length);
                var num_studies = 0;
                for (i = 0; i < study_names.length; i++) {
                    num_studies = 0;
                    for (j = 0; j < study_system_names.length; j++) {
                        num_studies += parseInt(study_summary[j][i].num_stu)
                    }
                    study_piechart_data[i] = {
                        name: study_names[i],
                        y: num_studies,
                        url: urlStartStudy + study_names[i]
                    };
                }

                if(typeof plotCTStudyFreq !== 'undefined') {
                    study_piechart_data.sort(sort_by_y);
                }

                var stu_name_colour_max = study_names.length == 1 ? study_names.length : study_names.length - 1;

                for(i=0; i<study_names.length; i++) {
                    study_piechart_data[i].color = colourScale(i/stu_name_colour_max).hex();
                }
            }

            if(typeof plotCTStudyFreq !== 'undefined') {
                var chart = $('#piechartStudyDIV').highcharts();
                chart.series[0].setData(study_piechart_data);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Study frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DLP per request chart data start
            if(typeof plotCTRequestMeanDLP !== 'undefined' || typeof plotCTRequestFreq !== 'undefined') {
                var request_summary = json.requestSummary;
                var request_names = json.requestNameList;
                var request_system_names = json.requestSystemList;
                var request_histogram_data = json.requestHistogramData;
            }

            if(typeof plotCTRequestMeanDLP !== 'undefined') {
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
                                y: request_summary[i][j].mean_dlp,
                                freq: request_summary[i][j].num_req,
                                bins: request_bins[i][j],
                                tooltip: request_system_names[i] + '<br>' + request_names[j] + '<br>' + request_summary[i][j].mean_dlp.toFixed(1) + ' mean<br>(n=' + request_summary[i][j].num_req + ')',
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
                                y: parseFloat(request_summary[i][j].median_dlp),
                                freq: request_summary[i][j].num_req,
                                bins: request_bins[i][j],
                                tooltip: request_system_names[i] + '<br>' + request_names[j] + '<br>' + parseFloat(request_summary[i][j].median_dlp).toFixed(1) + ' median<br>(n=' + request_summary[i][j].num_req + ')',
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

                var chartPlotCTRequestMeanDLP = $('#histogramRequestPlotDIV').highcharts();
                chartPlotCTRequestMeanDLP.xAxis[0].setCategories(request_names);
                chartPlotCTRequestMeanDLP.options.drilldown.series = series_drilldown_request;
                chartPlotCTRequestMeanDLP.options.exporting.sourceWidth = $(window).width();
                chartPlotCTRequestMeanDLP.options.exporting.sourceHeight = $(window).height();

                var req_sys_colour_max = request_system_names.length == 1 ? request_system_names.length : request_system_names.length - 1;

                if (plotAverageChoice == "mean") {
                    for (i = 0; i < request_system_names.length; i++) {
                        if (chartPlotCTRequestMeanDLP.series.length > i) {
                            chartPlotCTRequestMeanDLP.series[i].update({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTRequestMeanDLP.addSeries({
                                name: request_system_names[i],
                                data: request_data[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                    }
                }
                else if (plotAverageChoice == "median") {
                    for (i = 0; i < request_system_names.length; i++) {
                        if (chartPlotCTRequestMeanDLP.series.length > i) {
                            chartPlotCTRequestMeanDLP.series[i].update({
                                name: request_system_names[i],
                                data: request_data_median[i],
                                color: colourScale(i/req_sys_colour_max).hex()
                            });
                        }
                        else {
                            chartPlotCTRequestMeanDLP.addSeries({
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
                        if (chartPlotCTRequestMeanDLP.series.length > i+1) {
                            chartPlotCTRequestMeanDLP.series[i].update({
                                name: request_system_names[current_series],
                                data: request_data[current_series],
                                color: colourScale(i/(req_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTRequestMeanDLP.series[i+1].update({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(req_sys_colour_max*2-1)).hex()
                            });
                        }
                        else {
                            chartPlotCTRequestMeanDLP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data[current_series],
                                color: colourScale(i/(req_sys_colour_max*2-1)).hex()
                            });
                            chartPlotCTRequestMeanDLP.addSeries({
                                name: request_system_names[current_series],
                                data: request_data_median[current_series],
                                color: colourScale((i+1)/(req_sys_colour_max*2-1)).hex()
                            });
                        }
                        current_series++;
                    }
                }
                chartPlotCTRequestMeanDLP.redraw({duration: 1000});
            }
            // DLP per request chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Request frequency chart data start
            if(typeof plotCTRequestFreq !== 'undefined') {
                var request_piechart_data = new Array(request_names.length);
                var num_requests = 0;
                for (i = 0; i < request_names.length; i++) {
                    num_requests = 0;
                    for (j = 0; j < request_system_names.length; j++) {
                        num_requests += parseInt(request_summary[j][i].num_req)
                    }
                    request_piechart_data[i] = {
                        name: request_names[i],
                        y: num_requests,
                        url: urlStartReq + request_names[i]
                    };
                }

                request_piechart_data.sort(sort_by_y);

                var req_name_colour_max = request_names.length == 1 ? request_names.length : request_names.length - 1;

                for(i=0; i<request_names.length; i++) {
                    request_piechart_data[i].color = colourScale(i/req_name_colour_max).hex();
                }

                var chart = $('#piechartRequestDIV').highcharts();
                chart.series[0].setData(request_piechart_data);
                chart.options.exporting.sourceWidth = $(window).width();
                chart.options.exporting.sourceHeight = $(window).height();

                chart.redraw({ duration: 1000 });
            }
            // Request frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study workload chart data start
            if(typeof plotCTStudyPerDayAndHour !== 'undefined') {
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

                var chartPlotDXStudyPerDayAndHour = $('#piechartStudyWorkloadDIV').highcharts();
                chartPlotDXStudyPerDayAndHour.options.drilldown.series = seriesDrillDownPieChart;
                chartPlotDXStudyPerDayAndHour.series[0].setData(studyWorkloadPieChartData);
                chartPlotDXStudyPerDayAndHour.options.exporting.sourceWidth = $(window).width();
                chartPlotDXStudyPerDayAndHour.options.exporting.sourceHeight = $(window).height();

                chartPlotDXStudyPerDayAndHour.redraw({duration: 1000});
            }
            // Study workload chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DLP over time chart data start
            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average DAP values
            if(typeof plotCTStudyMeanDLPOverTime !== 'undefined') {
                var DLPOverTime, study_dlp_over_time, dateAxis, currentValue, tempDate, date_after, date_before;
                var chartCTStudyMeanDLPOverTime = $('#studyMeanDLPOverTimeDIV').highcharts();

                var study_line_colours =  new Array(study_names.length);
                study_piechart_data.sort(sort_by_name);
                for(i=0; i<study_names.length; i++) {
                    study_line_colours[i] = study_piechart_data[i].color;
                }
                study_piechart_data.sort(sort_by_y);

                study_dlp_over_time = (plotAverageChoice == "mean") ? json.studyMeanDLPoverTime : json.studyMedianDLPoverTime;

                dateAxis = [];
                for(i=0; i<study_dlp_over_time[0].length; i++) {
                    tempDate = new Date(Date.parse(study_dlp_over_time[0][i][0]));
                    tempDate = formatDate(tempDate);
                    dateAxis.push(tempDate);
                }

                DLPOverTime = [];
                for(i=0; i<study_dlp_over_time.length; i++) {
                    temp = [];
                    for(j=0; j<study_dlp_over_time[0].length; j++) {
                        tempDate = new Date(Date.parse(study_dlp_over_time[i][j][0]));
                        date_after = formatDate(tempDate);
                        date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                        currentValue = parseFloat(study_dlp_over_time[i][j][1]);
                        if(currentValue == 0) currentValue = null;

                        temp.push({y:currentValue, url: urlStartStudyOverTime+study_names[i]+'&date_after='+date_after+'&date_before='+date_before});
                    }
                    DLPOverTime.push({name: study_names[i], color: study_line_colours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
                }

                chartCTStudyMeanDLPOverTime.xAxis[0].setCategories(dateAxis);
                for(i=0; i<DLPOverTime.length; i++) {
                    chartCTStudyMeanDLPOverTime.addSeries(DLPOverTime[i]);
                }

                chartCTStudyMeanDLPOverTime.options.exporting.sourceWidth = $(window).width();
                chartCTStudyMeanDLPOverTime.options.exporting.sourceHeight = $(window).height();

                chartCTStudyMeanDLPOverTime.redraw({duration: 1000});
            }
            // DLP over time chart data end
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