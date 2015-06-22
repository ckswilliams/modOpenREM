$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'CTDI<sub>vol</sub> per acquisition protocol';
var tooltipData = [2];

var chartAcqCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotCTDIdiv',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (protocolNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartAcqCTDI.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'Number'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'CTDI<sub>vol</sub> range (mGy)'});
                    chartAcqCTDI.xAxis[0].setCategories([], true);
                    chartAcqCTDI.tooltip.options.formatter = function(args) {
                        var linkText = 'acquisition_ctdi_min=' + protocolBinsCTDI[tooltipData[1]][this.x] + '&acquisition_ctdi_max=' + protocolBinsCTDI[tooltipData[1]][this.x+1] + '&acquisition_protocol=' + tooltipData[0];
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartAcqCTDI.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'CTDI<sub>vol</sub> (mGy)'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'Protocol name'});
                    chartAcqCTDI.xAxis[0].setCategories(protocolNames, true);
                    chartAcqCTDI.xAxis[0].update({labels:{rotation:90}});
                    chartAcqCTDI.tooltip.options.formatter = function(args) {
                        var this_point_index = this.series.data.indexOf(this.point);
                        if (this.series.name.indexOf('Mean') != -1) {
                            var this_series_label = ' mean CTDI';
                            var this_series = args.chart.series[0];
                        }
                        else {
                            var this_series_label = ' median CTDI';
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
            text: 'CTDI<sub>vol</sub> per acquisition protocol'
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
                rotation: 90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'CTDI<sub>vol</sub> (mGy)'
            }
        },
        tooltip: {
            formatter: function (args) {
                var this_point_index = this.series.data.indexOf(this.point);
                if (this.series.name.indexOf('Mean') != -1) {
                    var this_series_label = ' mean CTDI';
                    var this_series = args.chart.series[0];
                }
                else {
                    var this_series_label = ' median CTDI';
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
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesDataCTDI
        }, {
            useHTML: true,
            name: 'Median CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesMedianDataCTDI
        }],
        drilldown: {
            series: seriesDrilldownCTDI
        }
    });
});

