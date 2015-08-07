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

            if( typeof plotDXAcquisitionMeanDAP !== 'undefined' || typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {

                var acq_summary = $.map(json.acquisitionSummary, function (el) {
                    return el;
                });

                protocolNames = $.map(json.acquisition_names, function (el) {
                    return el.acquisition_protocol;
                });

                seriesDataN = [];
                for (i = 0; i < protocolNames.length; i++) {
                    seriesDataN.push(acq_summary[i].num_acq);
                }
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

                var chartplotMeanMedianOrBoth = $('#container').highcharts();
                if(plotAverageChoice == "mean") {
                    chartplotMeanMedianOrBoth.series[0].setData(seriesData);
                    chartplotMeanMedianOrBoth.xAxis[0].setCategories(protocolNames);
                    chartplotMeanMedianOrBoth.options.drilldown.series = seriesDrilldown;
                    chartplotMeanMedianOrBoth.redraw({ duration: 1000 });
                }
                else if(plotAverageChoice == "median") {
                    chartplotMeanMedianOrBoth.series[0].setData(seriesMedianData);
                    chartplotMeanMedianOrBoth.xAxis[0].setCategories(protocolNames);
                    chartplotMeanMedianOrBoth.options.drilldown.series = seriesDrilldown;
                    chartplotMeanMedianOrBoth.redraw({ duration: 1000 });
                }
                else {
                    chartplotMeanMedianOrBoth.series[0].setData(seriesData);
                    chartplotMeanMedianOrBoth.series[1].setData(seriesMedianData);
                    chartplotMeanMedianOrBoth.xAxis[0].setCategories(protocolNames);
                    chartplotMeanMedianOrBoth.options.drilldown.series = seriesDrilldown;
                    chartplotMeanMedianOrBoth.redraw({ duration: 1000 });
                }
            }

            if(typeof plotDXAcquisitionFreq !== 'undefined' || typeof plotDXAcquisitionMeanDAPOverTime !== 'undefined') {
                //var urlStart = '/openrem/dx/?{% for field in filter.form %}{% if field.name != 'acquisition_protocol' and field.name != 'o' and field.value %}&{{ field.name }}={{ field.value }}{% endif %}{% endfor %}&acquisition_protocol=';
                var protocolPiechartData = new Array(protocolNames.length);
                for(i=0; i<protocolNames.length; i++) {
                    if(typeof plotDXAcquisitionFreq !== 'undefined') {
                        protocolPiechartData[i] = {name: protocolNames[i], y: parseInt(seriesDataN[i]), url: urlStart + protocolNames[i]};
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


            // [num acq protocols] lists of 2-element arrays.
            // Element 0 contains a 20-element array of counts
            // Element 1 contains a 21-element array of bin boundaries
            if("acquisitionHistogramkVpData" in json) {
                var acq_histogram_kVp_data = json.acquisitionHistogramkVpData;
            }
            if("acquisitionHistogrammAsData" in json) {
                var acq_histogram_mAs_data = json.acquisitionHistogrammAsData;
            }

            // A [num acq protocols] list of objects with acquisition_protocol, mean_dap, median_dap and num_acq properties
            if("acquisitionkVpSummary" in json) {
                var acq_kVp_summary = $.map(json.acquisitionkVpSummary, function (el) {
                    return el;
                });
            }
            if("acquisitionmAsSummary" in json) {
                var acq_mAs_summary = $.map(json.acquisitionmAsSummary, function (el) {
                    return el;
                });
            }

            // A [7][24] list of integer values
            if("studiesPerHourInWeekdays" in json) {
                var studies_per_hour_in_weekdays = json.studiesPerHourInWeekdays;
            }

            // A [num acq protocols][num time periods] list of 2-element arrays containing datetime and average DAP values
            if("acquisitionMeanDAPoverTime" in json) {
                var acq_mean_dap_over_time = json.acquisitionMeanDAPoverTime;
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