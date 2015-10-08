$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Median DLP and CTDI<sub>vol</sub> per acquisition protocol';
    var bins = [];
    var name = '';

    var chartAcqDLPandCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDLPandCTDIdiv',
            events: {
                drilldown: function (e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    var parentSeriesName = e.point.series.name;
                    var this_series_title = parentSeriesName.indexOf('DLP') != -1 ? ' DLP' : ' CTDI<sub>vol</sub>';
                    chartAcqDLPandCTDI.setTitle({text: ''});
                    chartAcqDLPandCTDI.yAxis[0].setTitle({text: 'Number'});
                    if (parentSeriesName.indexOf('DLP') != -1) {
                        chartAcqDLPandCTDI.xAxis[0].setTitle({text: 'DLP range (mGy.cm)'});
                    }
                    if (parentSeriesName.indexOf('CTDI') != -1) {
                        chartAcqDLPandCTDI.xAxis[1].setTitle({text: 'CTDI<sub>vol</sub> range (mGy)'});
                    }
                    chartAcqDLPandCTDI.xAxis[0].setCategories([], true);
                    chartAcqDLPandCTDI.tooltip.options.formatter = function (e) {
                        if (this.series.name.indexOf('DLP') != -1) {
                            var linkText = 'acquisition_dlp_min=' + bins[this.x] + '&acquisition_dlp_max=' + bins[this.x + 1] + '&acquisition_protocol=' + name;
                            var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>';
                        }
                        else {
                            var linkText = 'acquisition_ctdi_min=' + bins[this.x] + '&acquisition_ctdi_max=' + bins[this.x + 1] + '&acquisition_protocol=' + name;
                            var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>';
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
                drillup: function (e) {
                    chartAcqDLPandCTDI.setTitle({text: defaultTitle}, {text: ''});
                    chartAcqDLPandCTDI.yAxis[0].setTitle({text: 'DLP (mGy.cm)'});
                    chartAcqDLPandCTDI.yAxis[1].setTitle({text: 'CTDI<sub>vol</sub> (mGy)'});
                    chartAcqDLPandCTDI.xAxis[0].setTitle({text: ''});
                    chartAcqDLPandCTDI.xAxis[1].setTitle({text: ''});
                    chartAcqDLPandCTDI.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartAcqDLPandCTDI.tooltip.options.formatter = function (args) {
                        return this.point.tooltip;
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
            text: 'Median DLP and CTDI<sub>vol</sub> per acquisition protocol'
        },
        xAxis: [{
            categories: [1,2,3,4,5],
            title: {
                useHTML: true
            },
            type: 'category',
            labels: {
                useHTML: true,
                rotation: 90
            }
        }, {
            title: {
                useHTML: true
            },
            type: 'category',
            opposite: true,
            labels: {
                useHTML: true,
                rotation: 90
            }
        }],
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
            formatter: function (args) {
                return this.point.tooltip;
            }
        },
        plotOptions: {
            column: {
                borderWidth: 0
            }
        },
        series: [{
            name: 'Median DLP',
            data: []
        }, {
            name: 'Median CTDI<sub>vol</sub>',
            data: [],
            yAxis: 1
        }],
        drilldown: {
            series: [],//(seriesDrilldown).concat(seriesDrilldownCTDI),
            activeAxisLabelStyle: null
        },
        legend: {
            useHTML: true,
            align: 'left',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 0,
            x: 100,
            y: 120
        }
    });

    switch(chartSorting) {
        case 'freq':
            twoSeriesSort('#histogramPlotDLPandCTDIdiv', 'freq', chartSortingDirection, 0);
            break;
        case 'dlp':
            twoSeriesSort('#histogramPlotDLPandCTDIdiv', 'y', chartSortingDirection, 0);
            break;
        case 'ctdi':
            twoSeriesSort('#histogramPlotDLPandCTDIdiv', 'y', chartSortingDirection, 1);
            break;
        case 'name':
            twoSeriesSort('#histogramPlotDLPandCTDIdiv', 'name', chartSortingDirection, 0);
            break;
        default:
            twoSeriesSort('#histogramPlotDLPandCTDIdiv', 'name', chartSortingDirection, 0);
    }

});