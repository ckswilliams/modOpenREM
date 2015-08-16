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
                    seriesData = []; // This must be a global variable for the chart sorting routines to work
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
                    seriesMedianData = []; // This must be a global variable for the chart sorting routines to work
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
                    series_data_ctdi = []; // This must be a global variable for the chart sorting routines to work
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
                    series_median_data_ctdi = []; // This must be a global variable for the chart sorting routines to work
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

            
            // Use above DLP and CTDI data to populate the 1, 2 or 4 series as appropriate
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
                    chartplotCTAcquisitionMeanDLPandCTDI.series[0].setData(series_median_data_ctdi);
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
            else {
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