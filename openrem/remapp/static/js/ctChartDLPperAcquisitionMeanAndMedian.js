$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'DLP per acquisition protocol';
var tooltipData = [2];

var chartAcqDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDIV',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (protocolNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartAcqDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartAcqDLP.yAxis[0].setTitle({text:'Number'});
                    chartAcqDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setCategories([], true);
                    chartAcqDLP.tooltip.options.formatter = function(args) {
                        var linkText = 'acquisition_dlp_min=' + protocolBins[tooltipData[1]][this.x] + '&acquisition_dlp_max=' + protocolBins[tooltipData[1]][this.x+1] + '&acquisition_protocol=' + tooltipData[0];
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartAcqDLP.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqDLP.yAxis[0].setTitle({text:'DLP (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setTitle({text:'Protocol name'});
                    chartAcqDLP.xAxis[0].setCategories(protocolNames, true);
                    chartAcqDLP.xAxis[0].update({labels:{rotation:90}});
                    chartAcqDLP.tooltip.options.formatter = function(args) {
                        var this_point_index = this.series.data.indexOf(this.point);
                        if (this.series.name.indexOf('Mean') != -1) {
                            var this_series_label = ' mean DLP';
                            var this_series = args.chart.series[0];
                        }
                        else {
                            var this_series_label = ' median DLP';
                            var this_series = args.chart.series[1];
                        }
                        var this_point = this_series.data[this_point_index];
                        return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + seriesDataN[this_point_index] + ')';
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'DLP per acquisition protocol'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: protocolNames,
            title: {
                useHTML: true,
                text: 'Protocol name'
            },
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'DLP (mGy.cm)'
            }
        },
        tooltip: {
            formatter: function (args) {
                var this_point_index = this.series.data.indexOf(this.point);
                if (this.series.name.indexOf('Mean') != -1) {
                    var this_series_label = ' mean DLP';
                    var this_series = args.chart.series[0];
                }
                else {
                    var this_series_label = ' median DLP';
                    var this_series = args.chart.series[1];
                }
                var this_point = this_series.data[this_point_index];
                return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + seriesDataN[this_point_index] + ')';
            },
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0,
                borderWidth: 0
            }
        },
        series: [{
            useHTML: true,
            name: 'Mean DLP',
            data: seriesData
        }, {
            useHTML: true,
            name: 'Median DLP',
            data: seriesMedianData
        }],
        drilldown: {
            series: seriesDrilldown
        }
    });
});

