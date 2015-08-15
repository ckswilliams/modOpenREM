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
    var i, j;

    $.ajax({
        type: "GET",
        url: "/openrem/dx/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // this.url contains info about which charts need to be plotted
            var plotting_info = URLToArray(this.url);

            //-------------------------------------------------------------------------------------
            // DAP chart data start
            if( typeof plotDXAcquisitionMeanDAP !== 'undefined' || typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {

                var acq_summary = $.map(json.acquisitionSummary, function (el) {
                    return el;
                });

                protocolNames = $.map(json.acquisition_names, function (el) {
                    return el.acquisition_protocol;
                });
            }

            if(typeof plotDXAcquisitionMeanDAP !== 'undefined') {
                var acq_histogram_data = json.acquisitionHistogramData;

                protocolCounts = [];
                protocolBins = [];
                for (i = 0; i < protocolNames.length; i++) {
                    protocolCounts.push(acq_histogram_data[i][0]);
                    protocolBins.push(acq_histogram_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    seriesData = [];
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
                    seriesMedianData = [];
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

                var temp = [];
                seriesDrilldown = [];
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
                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionDAP.series[0].setData(seriesData);
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionDAP.series[0].setData(seriesMedianData);
                }
                else {
                    chartplotDXAcquisitionDAP.series[0].setData(seriesData);
                    chartplotDXAcquisitionDAP.series[1].setData(seriesMedianData);
                }
                chartplotDXAcquisitionDAP.redraw({ duration: 1000 });
            }
            // DAP chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // kVp chart data start
            if(typeof plotDXAcquisitionMeankVp !== 'undefined') {
                var acq_kVp_summary = $.map(json.acquisitionkVpSummary, function (el) {
                    return el;
                });

                var acq_histogram_kVp_data = json.acquisitionHistogramkVpData;

                protocolkVpNames = [];
                for (i = 0; i < acq_kVp_summary.length; i++) {
                    protocolkVpNames.push(acq_kVp_summary[i].acquisition_protocol);
                }

                protocolkVpCounts = [];
                protocolkVpBins = [];
                for (i = 0; i < protocolkVpNames.length; i++) {
                    protocolkVpCounts.push(acq_histogram_kVp_data[i][0]);
                    protocolkVpBins.push(acq_histogram_kVp_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    serieskVpData = [];
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
                    seriesMediankVpData = [];
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

                var temp = [];
                serieskVpDrilldown = [];
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
                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionMeankVp.series[0].setData(serieskVpData);
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionMeankVp.series[0].setData(seriesMediankVpData);
                }
                else {
                    chartplotDXAcquisitionMeankVp.series[0].setData(serieskVpData);
                    chartplotDXAcquisitionMeankVp.series[1].setData(seriesMediankVpData);
                }
                chartplotDXAcquisitionMeankVp.redraw({ duration: 1000 });
            }
            // kVp chart data end
            //-------------------------------------------------------------------------------------

            
            //-------------------------------------------------------------------------------------
            // mAs chart data start
            if(typeof plotDXAcquisitionMeanmAs !== 'undefined') {
                var acq_mAs_summary = $.map(json.acquisitionmAsSummary, function (el) {
                    return el;
                });

                var acq_histogram_mAs_data = json.acquisitionHistogrammAsData;

                protocolmAsNames = [];
                for (i = 0; i < acq_mAs_summary.length; i++) {
                    protocolmAsNames.push(acq_mAs_summary[i].acquisition_protocol);
                }

                protocolmAsCounts = [];
                protocolmAsBins = [];
                for (i = 0; i < protocolmAsNames.length; i++) {
                    protocolmAsCounts.push(acq_histogram_mAs_data[i][0]);
                    protocolmAsBins.push(acq_histogram_mAs_data[i][1]);
                }

                if(plotAverageChoice == "mean" || plotAverageChoice == "both") {
                    seriesmAsData = [];
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
                    seriesMedianmAsData = [];
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

                var temp = [];
                seriesmAsDrilldown = [];
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
                if(plotAverageChoice == "mean") {
                    chartplotDXAcquisitionMeanmAs.series[0].setData(seriesmAsData);
                }
                else if(plotAverageChoice == "median") {
                    chartplotDXAcquisitionMeanmAs.series[0].setData(seriesMedianmAsData);
                }
                else {
                    chartplotDXAcquisitionMeanmAs.series[0].setData(seriesmAsData);
                    chartplotDXAcquisitionMeanmAs.series[1].setData(seriesMedianmAsData);
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
                        protocolPiechartData[i] = {name: protocolNames[i], y: parseInt(acq_summary[i].num_acq), url: urlStart + protocolNames[i]};
                    }
                    else {
                        protocolPiechartData[i] = {name:protocolNames[i], y:parseInt(i), url:urlStart+protocolNames[i]};
                    }
                }

                if(typeof plotDXAcquisitionFreq !== 'undefined') {
                    protocolPiechartData.sort(sort_by_y);
                }

                protocolColours = getColours(protocolNames.length);
                for(i=0; i<protocolNames.length; i++) {
                    protocolPiechartData[i].color = protocolColours[i];
                }
            }

            if(typeof plotDXAcquisitionFreq !== 'undefined') {
                var chart = $('#piechartProtocolDIV').highcharts();
                chart.series[0].setData(protocolPiechartData);
                chart.redraw({ duration: 1000 });
            }
            // Acquisition frequency chart data end
            //-------------------------------------------------------------------------------------


            //-------------------------------------------------------------------------------------
            // Study workload chart data start
            if(typeof plotDXStudyPerDayAndHour !== 'undefined') {
                dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

                // A [7][24] list of integer values
                var studies_per_hour_in_weekdays = json.studiesPerHourInWeekdays;
                //var studiesPerHourEachWeekday = [];
                var studiesPerWeekday = [];
                var dayTotal = 0;
                for (i = 0; i < 7; i++) {
                    dayTotal = 0;
                    for (j = 0; j < 24; j++) {
                        //studiesPerHourEachWeekday.push(studies_per_hour_in_weekdays[i][j]);
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
            // DAP over time chart data start
            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average DAP values
            if(typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                var meanDAPOverTime, dateAxis, currentValue;

                if(plotAverageChoice == "mean") {
                    var acq_mean_dap_over_time = json.acquisitionMeanDAPoverTime;

                    dateAxis = [];
                    var tempDate;
                    for(i=0; i<acq_mean_dap_over_time[0].length; i++) {
                        tempDate = new Date(Date.parse(acq_mean_dap_over_time[0][i][0]));
                        tempDate = formatDate(tempDate);
                        dateAxis.push(tempDate);
                    }

                    var protocolLineColours =  new Array(protocolNames.length);
                    protocolPiechartData.sort(sort_by_name);
                    for(i=0; i<protocolNames.length; i++) {
                        protocolLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);

                    var date_after, date_before;
                    meanDAPOverTime = [];
                    for(i=0; i<acq_mean_dap_over_time.length; i++) {
                        temp = [];
                        for(j=0; j<acq_mean_dap_over_time[0].length; j++) {
                            tempDate = new Date(Date.parse(acq_mean_dap_over_time[i][j][0]));
                            date_after = formatDate(tempDate);
                            date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                            currentValue = acq_mean_dap_over_time[i][j][1];
                            if(currentValue == 0) currentValue = null;

                            temp.push({y:currentValue, url: urlStart+protocolNames[i]+'&date_after='+date_after+'&date_before='+date_before});
                        }
                        meanDAPOverTime.push({name: protocolNames[i], color: protocolLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp,});
                    }

                    var chartDXAcquisitionMeanDAPOverTime = $('#AcquisitionMeanDAPOverTimeDIV').highcharts();
                    chartDXAcquisitionMeanDAPOverTime.xAxis[0].setCategories(dateAxis);
                    for(i=0; i<meanDAPOverTime.length; i++) {
                        chartDXAcquisitionMeanDAPOverTime.addSeries(meanDAPOverTime[i]);
                    }
                    chartDXAcquisitionMeanDAPOverTime.redraw({duration: 1000});
                }
                else {
                    var acq_median_dap_over_time = json.acquisitionMedianDAPoverTime;
                    var medianDAPOverTime;

                    dateAxis = [];
                    var tempDate;
                    for(i=0; i<acq_median_dap_over_time[0].length; i++) {
                        tempDate = new Date(Date.parse(acq_median_dap_over_time[0][i][0]));
                        tempDate = formatDate(tempDate);
                        dateAxis.push(tempDate);
                    }

                    var protocolLineColours =  new Array(protocolNames.length);
                    protocolPiechartData.sort(sort_by_name);
                    for(i=0; i<protocolNames.length; i++) {
                        protocolLineColours[i] = protocolPiechartData[i].color;
                    }
                    protocolPiechartData.sort(sort_by_y);

                    var date_after, date_before;
                    medianDAPOverTime = [];
                    for(i=0; i<acq_median_dap_over_time.length; i++) {
                        temp = [];
                        for(j=0; j<acq_median_dap_over_time[0].length; j++) {
                            tempDate = new Date(Date.parse(acq_median_dap_over_time[i][j][0]));
                            date_after = formatDate(tempDate);
                            date_before = formatDate(new Date((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).setDate((new Date ((tempDate).setMonth((tempDate).getMonth()+1))).getDate()-1)));

                            currentValue = parseFloat( acq_median_dap_over_time[i][j][1]);
                            if(currentValue == 0) currentValue = null;

                            temp.push({y:currentValue, url: urlStart+protocolNames[i]+'&date_after='+date_after+'&date_before='+date_before});
                        }
                        medianDAPOverTime.push({name: protocolNames[i], color: protocolLineColours[i], marker:{enabled:true}, point:{events: {click: function(e) {location.href = e.point.url; e.preventDefault();}}}, data: temp});
                    }

                    var chartDXAcquisitionMeanDAPOverTime = $('#AcquisitionMeanDAPOverTimeDIV').highcharts();
                    chartDXAcquisitionMeanDAPOverTime.xAxis[0].setCategories(dateAxis);
                    for(i=0; i<medianDAPOverTime.length; i++) {
                        chartDXAcquisitionMeanDAPOverTime.addSeries(medianDAPOverTime[i]);
                    }
                    chartDXAcquisitionMeanDAPOverTime.redraw({duration: 1000});
                }
            }
            // DAP over time chart data end
            //-------------------------------------------------------------------------------------
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem getting the chart data for initial page view" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }
    });
    return false;
});