$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DLP and CTDI<sub>vol</sub> per acquisition protocol';
var tooltipData = [2];

var chartAcqDLPandCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDLPandCTDIdiv',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = protocolNames[e.point.x];
                    tooltipData[1] = e.point.x;
                    parentSeriesIndex = e.point.series.index;
                    var this_series_title = e.point.series.index == 0 ? ' DLP' : ' CTDI<sub>vol</sub>';
                    chartAcqDLPandCTDI.setTitle({ text: drilldownTitle + e.point.name + this_series_title}, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartAcqDLPandCTDI.yAxis[0].setTitle({text:'Number'});
                    chartAcqDLPandCTDI.xAxis[0].setTitle({text:e.point.series.index == 0 ? 'DLP range (mGy.cm)' : 'CTDI<sub>vol</sub> range (mGy)'});
                    chartAcqDLPandCTDI.xAxis[0].setCategories([], true);
                    chartAcqDLPandCTDI.tooltip.options.formatter = function(args) {
                        if (parentSeriesIndex  == 0) {
                            var linkText = 'acquisition_dlp_min=' + protocolBins[tooltipData[1]][this.x] + '&acquisition_dlp_max=' + protocolBins[tooltipData[1]][this.x + 1] + '&acquisition_protocol=' + tooltipData[0];
                            var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/hist/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>';
                        }
                        else {
                            returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr></table>';
                        }
                        return returnValue;
                    };
                    chartAcqDLPandCTDI.yAxis[1].update({
                        labels: {
                            enabled: false
                        },
                        title: {
                            text: null
                        }
                    });
                },
                drillup: function(e) {
                    chartAcqDLPandCTDI.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqDLPandCTDI.yAxis[0].setTitle({text:'DLP (mGy.cm)'});
                    chartAcqDLPandCTDI.yAxis[1].setTitle({text:'CTDI<sub>vol</sub> (mGy)'});
                    chartAcqDLPandCTDI.xAxis[0].setTitle({text:''});
                    chartAcqDLPandCTDI.xAxis[0].setCategories(protocolNames, true);
                    chartAcqDLPandCTDI.xAxis[0].update({labels:{rotation:90}});
                    chartAcqDLPandCTDI.tooltip.options.formatter = function(args) {
                        var this_point_index = this.series.data.indexOf( this.point );
                        var this_series_index = 0;//this.series.index;
                        var that_series_index = 1;//this.series.index == 0 ? 1 : 0; // assuming 2 series
                        var this_series = args.chart.series[this_series_index];
                        var that_series = args.chart.series[that_series_index];
                        var this_point = this_series.data[this_point_index];
                        var that_point = that_series.data[this_point_index];
                        var this_series_label = ' mGy.cm DLP';//this.series.index == 0 ? ' mGy.cm DLP' : ' mGy CTDI<sub>vol</sub>';
                        var that_series_label = ' mGy CTDI<sub>vol</sub>';//this.series.index == 0 ? ' mGy CTDI<sub>vol</sub>' : ' mGy.cm DLP';
                        return this.point.name +
                            '<br/>' + this_point.y.toFixed(1) + this_series_label +
                            '<br/>' + that_point.y.toFixed(1) + that_series_label +
                            '<br/>(n = ' + seriesDataN[this_point_index] + ')';
                    };
                    chartAcqDLPandCTDI.yAxis[1].update({
                        labels: {
                            enabled: true
                        },
                        title: {
                            text: 'CTDI<sub>vol</sub> (mGy)'
                        }
                    });

                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean DLP and CTDI<sub>vol</sub> per acquisition protocol'
        },
        xAxis: {
            title: {
                useHTML: true
            },
            categories: protocolNames,
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: [{
            min: 0,
            title: {
                text: 'DLP (mGy.cm)'
            }
        }, {
            title: {
                useHTML: true,
                text: 'CTDI<sub>vol</sub> (mGy)'
            },
            opposite: true
        }],
        tooltip: {
            useHTML: true,
            formatter: function(args) {
                var this_point_index = this.series.data.indexOf( this.point );
                var this_series_index = 0;//this.series.index;
                var that_series_index = 1;//this.series.index == 0 ? 1 : 0; // assuming 2 series
                var this_series = args.chart.series[this_series_index];
                var that_series = args.chart.series[that_series_index];
                var this_point = this_series.data[this_point_index];
                var that_point = that_series.data[this_point_index];
                var this_series_label = ' mGy.cm DLP';//this.series.index == 0 ? ' mGy.cm DLP' : ' mGy CTDI<sub>vol</sub>';
                var that_series_label = ' mGy CTDI<sub>vol</sub>';//this.series.index == 0 ? ' mGy CTDI<sub>vol</sub>' : ' mGy.cm DLP';
                return this.point.name +
                    '<br/>' + this_point.y.toFixed(1) + this_series_label +
                    '<br/>' + that_point.y.toFixed(1) + that_series_label +
                    '<br/>(n = ' + seriesDataN[this_point_index] + ')';
            }
        },
        plotOptions: {
            column: {
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean DLP per acquisition protocol',
            data: seriesData
        }, {
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesDataCTDI,
            yAxis: 1
        }],
        drilldown: {
            series: (seriesDrilldown).concat(seriesDrilldownCTDI)
        },
        legend: {
            useHTML: true,
            align: 'center',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 0,
            x: 0,
            y: 40
        }
    });
});

