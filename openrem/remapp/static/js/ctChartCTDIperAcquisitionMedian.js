$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Median CTDI<sub>vol</sub> per acquisition protocol';
    var bins = [];
    var name= '';

    var chartAcqCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotCTDIdiv',
            events: {
                drilldown: function (e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartAcqCTDI.setTitle({text: drilldownTitle + e.point.name}, {text: '(n = ' + e.point.freq + ')'});
                    chartAcqCTDI.yAxis[0].setTitle({text: 'Number'});
                    chartAcqCTDI.xAxis[0].setTitle({text: 'CTDI<sub>vol</sub> range (mGy)'});
                    chartAcqCTDI.xAxis[0].setCategories([], true);
                    chartAcqCTDI.tooltip.options.formatter = function (e) {
                        var linkText = 'acquisition_ctdi_min=' + bins[this.x] + '&acquisition_ctdi_max=' + bins[this.x + 1] + '&acquisition_protocol=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    chartAcqCTDI.setTitle({text: defaultTitle}, {text: ''});
                    chartAcqCTDI.yAxis[0].setTitle({text: 'Median CTDI<sub>vol</sub> (mGy)'});
                    chartAcqCTDI.xAxis[0].setTitle({text: 'Protocol name'});
                    chartAcqCTDI.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartAcqCTDI.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Median CTDI<sub>vol</sub> per acquisition protocol'
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
                text: 'Median CTDI<sub>vol</sub> (mGy)'
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
            name: 'Median CTDI<sub>vol</sub> per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            seriesSort('#histogramPlotCTDIdiv', 'freq', chartSortingDirection);
            break;
        case 'ctdi':
            seriesSort('#histogramPlotCTDIdiv', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#histogramPlotCTDIdiv', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#histogramPlotCTDIdiv', 'name', 1);
    }

});