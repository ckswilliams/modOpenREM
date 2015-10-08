$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Mean DLP per acquisition protocol';
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
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    chartAcqDLP.setTitle({text: defaultTitle}, {text: ''});
                    chartAcqDLP.yAxis[0].setTitle({text: 'Mean DLP (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setTitle({text: 'Protocol name'});
                    chartAcqDLP.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartAcqDLP.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean DLP per acquisition protocol'
        },
        legend: {
            enabled: false
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
                text: 'Mean DLP (mGy.cm)'
            }
        },
        tooltip: {
            formatter: function () {
                return this.point.tooltip;
            },
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            useHTML: true,
            name: 'Mean DLP per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            seriesSort('#histogramPlotDIV', 'freq', chartSortingDirection);
            break;
        case 'dlp':
            seriesSort('#histogramPlotDIV', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#histogramPlotDIV', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#histogramPlotDIV', 'name', 1);
    }

});