$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'DLP per acquisition protocol';
    var bins = [];
    var name = '';

    var chartAcqDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDIV',
            events: {
                drilldown: function (e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartAcqDLP.setTitle({text: drilldownTitle + e.point.name}, {text: '(n = ' + e.point.freq + ')'});
                    chartAcqDLP.yAxis[0].setTitle({text: 'Number'});
                    chartAcqDLP.xAxis[0].setTitle({text: 'DLP range (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setCategories([], true);
                    chartAcqDLP.tooltip.options.formatter = function (e) {
                        var linkText = 'acquisition_dlp_min=' + bins[this.x] + '&acquisition_dlp_max=' + bins[this.x + 1] + '&acquisition_protocol=' + name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    chartAcqDLP.setTitle({text: defaultTitle}, {text: ''});
                    chartAcqDLP.yAxis[0].setTitle({text: 'DLP (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setTitle({text: 'Protocol name'});
                    chartAcqDLP.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartAcqDLP.tooltip.options.formatter = function (args) {
                        return this.point.tooltip;
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
            categories: [1,2,3,4,5],
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
                text: 'DLP (mGy.cm)'
            }
        },
        tooltip: {
            formatter: function (args) {
                return this.point.tooltip;
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
            name: 'Mean DLP per acquisition protocol',
            data: []
        }, {
            useHTML: true,
            name: 'Median DLP per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            twoSeriesSort('#histogramPlotDIV', 'freq', chartSortingDirection, 0);
            break;
        case 'dlp':
            twoSeriesSort('#histogramPlotDIV', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            twoSeriesSort('#histogramPlotDIV', 'name', chartSortingDirection, 0);
            break;
        default:
            twoSeriesSort('#histogramPlotDIV', 'name', chartSortingDirection, 0);
    }

});