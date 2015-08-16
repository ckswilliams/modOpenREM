$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle   = 'CTDI<sub>vol</sub> per acquisition protocol';
    var bins = [];
    var name = '';

    var chartAcqCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotCTDIdiv',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartAcqCTDI.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + e.point.freq +')' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'Number'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'CTDI<sub>vol</sub> range (mGy)'});
                    chartAcqCTDI.xAxis[0].setCategories([], true);
                    chartAcqCTDI.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_ctdi_min=' + bins[this.x] + '&acquisition_ctdi_max=' + bins[this.x+1] + '&acquisition_protocol=' + name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartAcqCTDI.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'CTDI<sub>vol</sub> (mGy)'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'Protocol name'});
                    chartAcqCTDI.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartAcqCTDI.tooltip.options.formatter = function(args) {
                        return this.point.tooltip;
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
                text: 'CTDI<sub>vol</sub> (mGy)'
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
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: []
        }, {
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
            twoSeriesSort('#histogramPlotCTDIdiv', 'freq', chartSortingDirection, 0);
            break;
        case 'ctdi':
            twoSeriesSort('#histogramPlotCTDIdiv', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            twoSeriesSort('#histogramPlotCTDIdiv', 'name', chartSortingDirection, 0);
            break;
        default:
            twoSeriesSort('#histogramPlotCTDIdiv', 'name', chartSortingDirection, 0);
    }

});