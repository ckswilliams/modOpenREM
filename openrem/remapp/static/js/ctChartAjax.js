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

            //-------------------------------------------------------------------------------------
            // DLP per acquisition chart data start
            if( typeof plotCTAcquisitionMeanDLP !== 'undefined' || typeof plotCTAcquisitionFreq !== 'undefined' || typeof plotCTAcquisitionMeanCTDI !== 'undefined') {

                var acq_summary = $.map(json.acquisitionSummary, function (el) {
                    return el;
                });

                var protocolNames = [];
                for (i = 0; i < acq_summary.length; i++) {
                    protocolNames.push(acq_summary[i].acquisition_protocol);
                }
            }

            if(typeof plotCTAcquisitionMeanDLP !== 'undefined') {
                var acq_histogram_data = json.acquisitionHistogramData;

                var protocolCounts = [];
                var protocolBins = [];
                for (i = 0; i < protocolNames.length; i++) {
                    protocolCounts.push(acq_histogram_data[i][0]);
                    protocolBins.push(acq_histogram_data[i][1]);
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var seriesData = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        seriesData.push({
                            name: protocolNames[i],
                            y: acq_summary[i].mean_dlp,
                            freq: acq_summary[i].num_acq,
                            bins: protocolBins[i],
                            tooltip: protocolNames[i] + '<br>' + acq_summary[i].mean_dlp.toFixed(1) + ' mean<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var seriesMedianData = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        seriesMedianData.push({
                            name: protocolNames[i],
                            y: parseFloat(acq_summary[i].median_dlp),
                            freq: acq_summary[i].num_acq,
                            bins: protocolBins[i],
                            tooltip: protocolNames[i] + '<br>' + parseFloat(acq_summary[i].median_dlp).toFixed(1) + ' median<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                temp = [];
                var seriesDrilldown = [];
                for (i = 0; i < protocolNames.length; i++) {
                    temp = [];
                    for (j = 0; j < protocolCounts[0].length; j++) {
                        temp.push([protocolBins[i][j].toFixed(1).toString() + ' \u2264 x < ' + protocolBins[i][j + 1].toFixed(1).toString(), protocolCounts[i][j]]);
                    }
                    seriesDrilldown.push({id: protocolNames[i], name: protocolNames[i], useHTML: true, data: temp});
                }
            }
            // DLP per acquisition chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // CTDI per acquisition chart data start
            if(typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                var acq_histogram_data_ctdi = json.acquisitionHistogramDataCTDI;

                var protocol_counts_ctdi = [];
                var protocol_bins_ctdi = [];
                for (i = 0; i < protocolNames.length; i++) {
                    protocol_counts_ctdi.push(acq_histogram_data_ctdi[i][0]);
                    protocol_bins_ctdi.push(acq_histogram_data_ctdi[i][1]);
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var series_data_ctdi = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        series_data_ctdi.push({
                            name: protocolNames[i],
                            y: acq_summary[i].mean_ctdi,
                            freq: acq_summary[i].num_acq,
                            bins: protocol_bins_ctdi[i],
                            tooltip: protocolNames[i] + '<br>' + acq_summary[i].mean_ctdi.toFixed(1) + ' mean<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var series_median_data_ctdi = [];
                    for (i = 0; i < protocolNames.length; i++) {
                        series_median_data_ctdi.push({
                            name: protocolNames[i],
                            y: parseFloat(acq_summary[i].median_ctdi),
                            freq: acq_summary[i].num_acq,
                            bins: protocol_bins_ctdi[i],
                            tooltip: protocolNames[i] + '<br>' + parseFloat(acq_summary[i].median_ctdi).toFixed(1) + ' median<br>(n=' + acq_summary[i].num_acq + ')',
                            drilldown: protocolNames[i]
                        });
                    }
                }

                temp = [];
                var series_drilldown_ctdi = [];
                for (i = 0; i < protocolNames.length; i++) {
                    temp = [];
                    for (j = 0; j < protocol_counts_ctdi[0].length; j++) {
                        temp.push([protocol_bins_ctdi[i][j].toFixed(1).toString() + ' \u2264 x < ' + protocol_bins_ctdi[i][j + 1].toFixed(1).toString(), protocol_counts_ctdi[i][j]]);
                    }
                    series_drilldown_ctdi.push({id: protocolNames[i], name: protocolNames[i], useHTML: true, data: temp});
                }
            }
            // CTDI per acquisition chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Use above DLP and CTDI data to populate the 1, 2 or 4 series in the DLP and/or CTDI plot as appropriate
            if(typeof plotCTAcquisitionMeanDLP !== 'undefined' && typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                var chartplotCTAcquisitionMeanDLPandCTDI = $('#histogramPlotDLPandCTDIdiv').highcharts();
                chartplotCTAcquisitionMeanDLPandCTDI.xAxis[0].setCategories(protocolNames);
                chartplotCTAcquisitionMeanDLPandCTDI.options.drilldown.series = (seriesDrilldown).concat(series_drilldown_ctdi);
                if (plotAverageChoice == "mean") {
                    chartplotCTAcquisitionMeanDLPandCTDI.series[0].setData(seriesData);
                    chartplotCTAcquisitionMeanDLPandCTDI.series[1].setData(series_data_ctdi);
                }
                else if (plotAverageChoice == "median") {
                    chartplotCTAcquisitionMeanDLPandCTDI.series[0].setData(seriesMedianData);
                    chartplotCTAcquisitionMeanDLPandCTDI.series[1].setData(series_median_data_ctdi);
                }
                else {
                    chartplotCTAcquisitionMeanDLPandCTDI.series[0].setData(seriesData);
                    chartplotCTAcquisitionMeanDLPandCTDI.series[1].setData(seriesMedianData);
                    chartplotCTAcquisitionMeanDLPandCTDI.series[2].setData(series_data_ctdi);
                    chartplotCTAcquisitionMeanDLPandCTDI.series[3].setData(series_median_data_ctdi);
                }
                chartplotCTAcquisitionMeanDLPandCTDI.redraw({duration: 1000});
            }
            else if(typeof plotCTAcquisitionMeanDLP !== 'undefined') {
                var chartplotCTAcquisitionMeanDLP = $('#histogramPlotDIV').highcharts();
                chartplotCTAcquisitionMeanDLP.xAxis[0].setCategories(protocolNames);
                chartplotCTAcquisitionMeanDLP.options.drilldown.series = seriesDrilldown;
                if (plotAverageChoice == "mean") {
                    chartplotCTAcquisitionMeanDLP.series[0].setData(seriesData);
                }
                else if (plotAverageChoice == "median") {
                    chartplotCTAcquisitionMeanDLP.series[0].setData(seriesMedianData);
                }
                else {
                    chartplotCTAcquisitionMeanDLP.series[0].setData(seriesData);
                    chartplotCTAcquisitionMeanDLP.series[1].setData(seriesMedianData);
                }
                chartplotCTAcquisitionMeanDLP.redraw({duration: 1000});
            }
            else if(typeof plotCTAcquisitionMeanCTDI !== 'undefined') {
                var chartplotCTAcquisitionMeanCTDI = $('#histogramPlotCTDIdiv').highcharts();
                chartplotCTAcquisitionMeanCTDI.xAxis[0].setCategories(protocolNames);
                chartplotCTAcquisitionMeanCTDI.options.drilldown.series = series_drilldown_ctdi;
                if (plotAverageChoice == "mean") {
                    chartplotCTAcquisitionMeanCTDI.series[0].setData(series_data_ctdi);
                }
                else if (plotAverageChoice == "median") {
                    chartplotCTAcquisitionMeanCTDI.series[0].setData(series_median_data_ctdi);
                }
                else {
                    chartplotCTAcquisitionMeanCTDI.series[0].setData(series_data_ctdi);
                    chartplotCTAcquisitionMeanCTDI.series[1].setData(series_median_data_ctdi);
                }
                chartplotCTAcquisitionMeanCTDI.redraw({duration: 1000});
            }
            // End of populating the DLP and/or CTDI plot
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Acquisition frequency chart data start
            if(typeof plotCTAcquisitionFreq !== 'undefined') {
                //var urlStart = '/openrem/ct/?{% for field in filter.form %}{% if field.name != 'acquisition_protocol' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&acquisition_protocol=';
                var protocolPiechartData = new Array(protocolNames.length);
                for(i=0; i<protocolNames.length; i++) {
                    if(typeof plotCTAcquisitionFreq !== 'undefined') {
                        protocolPiechartData[i] = {name: protocolNames[i], y: parseInt(acq_summary[i].num_acq), url: urlStartAcq + protocolNames[i]};
                    }
                    else {
                        protocolPiechartData[i] = {name:protocolNames[i], y:parseInt(i), url:urlStartAcq+protocolNames[i]};
                    }
                }

                if(typeof plotCTAcquisitionFreq !== 'undefined') {
                    protocolPiechartData.sort(sort_by_y);
                }

                var protocolColours = getColours(protocolNames.length);
                for(i=0; i<protocolNames.length; i++) {
                    protocolPiechartData[i].color = protocolColours[i];
                }
            }

            if(typeof plotCTAcquisitionFreq !== 'undefined') {
                var chart = $('#piechartProtocolDIV').highcharts();
                chart.series[0].setData(protocolPiechartData);
                chart.redraw({ duration: 1000 });
            }
            // Acquisition frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DLP per study chart data start
            if( typeof plotCTStudyMeanDLP !== 'undefined' || typeof plotCTStudyFreq !== 'undefined' || typeof plotCTStudyMeanDLPOverTime !== 'undefined') {

                var study_summary = $.map(json.studySummary, function (el) {
                    return el;
                });

                var study_names = [];
                for (i = 0; i < study_summary.length; i++) {
                    study_names.push(study_summary[i].study_description);
                }
            }

            if(typeof plotCTStudyMeanDLP !== 'undefined') {
                
                var study_histogram_data = json.studyHistogramData;

                var study_counts = [];
                var study_bins = [];
                for (i = 0; i < study_names.length; i++) {
                    study_counts.push(study_histogram_data[i][0]);
                    study_bins.push(study_histogram_data[i][1]);
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var study_data = [];
                    for (i = 0; i < study_names.length; i++) {
                        study_data.push({
                            name: study_names[i],
                            y: study_summary[i].mean_dlp,
                            freq: study_summary[i].num_acq,
                            bins: study_bins[i],
                            tooltip: study_names[i] + '<br>' + study_summary[i].mean_dlp.toFixed(1) + ' mean<br>(n=' + study_summary[i].num_acq + ')',
                            drilldown: study_names[i]
                        });
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var study_data_median = [];
                    for (i = 0; i < study_names.length; i++) {
                        study_data_median.push({
                            name: study_names[i],
                            y: parseFloat(study_summary[i].median_dlp),
                            freq: study_summary[i].num_acq,
                            bins: study_bins[i],
                            tooltip: study_names[i] + '<br>' + parseFloat(study_summary[i].median_dlp).toFixed(1) + ' median<br>(n=' + study_summary[i].num_acq + ')',
                            drilldown: study_names[i]
                        });
                    }
                }

                temp = [];
                var series_drilldown_study = [];
                for (i = 0; i < study_names.length; i++) {
                    temp = [];
                    for (j = 0; j < study_counts[0].length; j++) {
                        temp.push([study_bins[i][j].toFixed(1).toString() + ' \u2264 x < ' + study_bins[i][j + 1].toFixed(1).toString(), study_counts[i][j]]);
                    }
                    series_drilldown_study.push({id: study_names[i], name: study_names[i], useHTML: true, data: temp});
                }

                var chartplotCTStudyMeanDLP = $('#histogramStudyPlotDIV').highcharts();
                chartplotCTStudyMeanDLP.xAxis[0].setCategories(study_names);
                chartplotCTStudyMeanDLP.options.drilldown.series = series_drilldown_study;
                if (plotAverageChoice == "mean") {
                    chartplotCTStudyMeanDLP.series[0].setData(study_data);
                }
                else if (plotAverageChoice == "median") {
                    chartplotCTStudyMeanDLP.series[0].setData(study_data_median);
                }
                else {
                    chartplotCTStudyMeanDLP.series[0].setData(study_data);
                    chartplotCTStudyMeanDLP.series[1].setData(study_data_median);
                }
                chartplotCTStudyMeanDLP.redraw({duration: 1000});
            }
            // DLP per study chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study frequency chart data start
            if(typeof plotCTStudyFreq !== 'undefined' || typeof plotCTStudyMeanDLPOverTime !== 'undefined') {
                //var var urlStart = '/openrem/ct/?{% for field in filter.form %}{% if field.name != 'study_description' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&study_description=';
                var study_piechart_data = new Array(study_names.length);
                for(i=0; i<study_names.length; i++) {
                    if(typeof plotCTStudyFreq !== 'undefined') {
                        study_piechart_data[i] = {name: study_names[i], y: parseInt(study_summary[i].num_acq), url: urlStartStudy + study_names[i]};
                    }
                    else {
                        study_piechart_data[i] = {name: study_names[i], y:parseInt(i), url:urlStartStudy+study_names[i]};
                    }
                }

                if(typeof plotCTStudyFreq !== 'undefined') {
                    study_piechart_data.sort(sort_by_y);
                }

                var study_colours = getColours(study_names.length);
                for(i=0; i<study_names.length; i++) {
                    study_piechart_data[i].color = study_colours[i];
                }
            }

            if(typeof plotCTStudyFreq !== 'undefined') {
                var chart = $('#piechartStudyDIV').highcharts();
                chart.series[0].setData(study_piechart_data);
                chart.redraw({ duration: 1000 });
            }
            // Study frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // DLP per request chart data start
            if(typeof plotCTRequestMeanDLP !== 'undefined' || typeof plotCTRequestFreq !== 'undefined') {

                var request_summary = $.map(json.requestSummary, function (el) {
                    return el;
                });

                var request_names = [];
                for (i = 0; i < request_summary.length; i++) {
                    request_names.push(request_summary[i].requested_procedure_code_meaning);
                }
            }

            if(typeof plotCTRequestMeanDLP !== 'undefined') {

                var request_histogram_data = json.requestHistogramData;

                var request_counts = [];
                var request_bins = [];
                for (i = 0; i < request_names.length; i++) {
                    request_counts.push(request_histogram_data[i][0]);
                    request_bins.push(request_histogram_data[i][1]);
                }

                if (plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    var request_data = [];
                    for (i = 0; i < request_names.length; i++) {
                        request_data.push({
                            name: request_names[i],
                            y: request_summary[i].mean_dlp,
                            freq: request_summary[i].num_req,
                            bins: request_bins[i],
                            tooltip: request_names[i] + '<br>' + request_summary[i].mean_dlp.toFixed(1) + ' mean<br>(n=' + request_summary[i].num_req + ')',
                            drilldown: request_names[i]
                        });
                    }
                }

                if (plotAverageChoice == "median" || plotAverageChoice == "both") {
                    var request_data_median = [];
                    for (i = 0; i < request_names.length; i++) {
                        request_data_median.push({
                            name: request_names[i],
                            y: parseFloat(request_summary[i].median_dlp),
                            freq: request_summary[i].num_req,
                            bins: request_bins[i],
                            tooltip: request_names[i] + '<br>' + parseFloat(request_summary[i].median_dlp).toFixed(1) + ' median<br>(n=' + request_summary[i].num_req + ')',
                            drilldown: request_names[i]
                        });
                    }
                }

                temp = [];
                var series_drilldown_request = [];
                for (i = 0; i < request_names.length; i++) {
                    temp = [];
                    for (j = 0; j < request_counts[0].length; j++) {
                        temp.push([request_bins[i][j].toFixed(1).toString() + ' \u2264 x < ' + request_bins[i][j + 1].toFixed(1).toString(), request_counts[i][j]]);
                    }
                    series_drilldown_request.push({id: request_names[i], name: request_names[i], useHTML: true, data: temp});
                }

                var chartplotCTRequestMeanDLP = $('#histogramRequestPlotDIV').highcharts();
                chartplotCTRequestMeanDLP.xAxis[0].setCategories(request_names);
                chartplotCTRequestMeanDLP.options.drilldown.series = series_drilldown_request;
                if (plotAverageChoice == "mean") {
                    chartplotCTRequestMeanDLP.series[0].setData(request_data);
                }
                else if (plotAverageChoice == "median") {
                    chartplotCTRequestMeanDLP.series[0].setData(request_data_median);
                }
                else {
                    chartplotCTRequestMeanDLP.series[0].setData(request_data);
                    chartplotCTRequestMeanDLP.series[1].setData(request_data_median);
                }
                chartplotCTRequestMeanDLP.redraw({duration: 1000});
            }
            // DLP per request chart data end
            //-------------------------------------------------------------------------------------

            //-------------------------------------------------------------------------------------
            // Request frequency chart data start
            if(typeof plotCTRequestFreq !== 'undefined') {
                //var var urlStart = '/openrem/ct/?{% for field in filter.form %}{% if field.name != 'request_description' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&request_description=';
                var request_piechart_data = new Array(request_names.length);
                for(i=0; i<request_names.length; i++) {
                    if(typeof plotCTRequestFreq !== 'undefined') {
                        request_piechart_data[i] = {name: request_names[i], y: parseInt(request_summary[i].num_req), url: urlStartReq + request_names[i]};
                    }
                    else {
                        request_piechart_data[i] = {name: request_names[i], y:parseInt(i), url:urlStartReq+request_names[i]};
                    }
                }

                if(typeof plotCTRequestFreq !== 'undefined') {
                    request_piechart_data.sort(sort_by_y);
                }

                var request_colours = getColours(request_names.length);
                for(i=0; i<request_names.length; i++) {
                    request_piechart_data[i].color = request_colours[i];
                }
            }

            if(typeof plotCTRequestFreq !== 'undefined') {
                var chart = $('#piechartRequestDIV').highcharts();
                chart.series[0].setData(request_piechart_data);
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
                var studiesPerWeekday = [];
                var dayTotal = 0;
                for (i = 0; i < 7; i++) {
                    dayTotal = 0;
                    for (j = 0; j < 24; j++) {
                        dayTotal = dayTotal + studies_per_hour_in_weekdays[i][j];
                    }
                    studiesPerWeekday[i] = dayTotal;
                }

                var hourColours = getColours(24);
                var dayColours = getColours(7);
                var studyWorkloadPieChartData = [];
                var seriesDrillDownPieChart = [];
                var tempTime;
                for (i = 0; i < 7; i++) {
                    temp = [];
                    for (j = 0; j < 24; j++) {
                        tempTime = "0" + j;
                        tempTime = tempTime.substr(tempTime.length-2);
                        temp.push({name: tempTime + ':00', y: studies_per_hour_in_weekdays[i][j], color: hourColours[j]});
                    }
                    studyWorkloadPieChartData.push({
                        name: dayNames[i],
                        y: studiesPerWeekday[i],
                        color: dayColours[i],
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
                chartplotDXStudyPerDayAndHour.redraw({duration: 1000});
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