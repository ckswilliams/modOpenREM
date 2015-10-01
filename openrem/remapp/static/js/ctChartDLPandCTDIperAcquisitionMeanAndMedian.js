$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'DLP and CTDI<sub>vol</sub> per acquisition protocol';
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
            text: 'DLP and CTDI<sub>vol</sub> per acquisition protocol'
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
                pointPadding: 0,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean DLP',
            data: [],
            color: '#2b8cbe',
            pointPlacement: -0.02
        }, {
            name: 'Median DLP',
            data: [],
            color: '#7bccc4',
            pointPlacement: -0.02,
        }, {
            name: 'Mean CTDI<sub>vol</sub>',
            data: [],
            color: '#d7301f',
            pointPlacement: 0.02,
            yAxis: 1
        }, {
            name: 'Median CTDI<sub>vol</sub>',
            data: [],
            color: '#fdcc8a',
            pointPlacement: 0.02,
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
            y: 120,
            width: 120,
            itemWidth: 110,
            itemStyle: {
              width:100
            }
        }
    });

    switch(chartSorting) {
        case 'freq':
            fourSeriesSort('#histogramPlotDLPandCTDIdiv', 'freq', chartSortingDirection, [0,1,2,3]);
            break;
        case 'dlp':
            fourSeriesSort('#histogramPlotDLPandCTDIdiv', 'y', chartSortingDirection, [0,1,2,3]);
            break;
        case 'ctdi':
            fourSeriesSort('#histogramPlotDLPandCTDIdiv', 'y', chartSortingDirection, [2,3,0,1]);
            break;
        case 'name':
            fourSeriesSort('#histogramPlotDLPandCTDIdiv', 'name', chartSortingDirection, [0,1,2,3]);
            break;
        default:
            fourSeriesSort('#histogramPlotDLPandCTDIdiv', 'name', chartSortingDirection, [0,1,2,3]);
    }

});
