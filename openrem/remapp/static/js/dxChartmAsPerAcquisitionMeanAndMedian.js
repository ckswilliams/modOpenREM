$(function () {
    var drilldownmAsTitle = 'Histogram of ';
    var defaultmAsTitle   = 'mAs per acquisition protocol';
    var bins = [];
    var name = '';

    var chartmAsPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeanmAs',
            events: {
                drilldown: function(ee) {
                    bins = ee.point.bins;
                    name = (ee.point.name).replace('&amp;', '%26');
                    chartmAsPerAcquisition.setTitle({ text: drilldownmAsTitle + ee.point.name + ' mAs values' }, { text: '(n = ' + ee.point.freq +')' });
                    chartmAsPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartmAsPerAcquisition.xAxis[0].setTitle({text:'mAs range'});
                    chartmAsPerAcquisition.xAxis[0].setCategories([], true);
                    chartmAsPerAcquisition.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_mas_min=' + ([this.x])*1000 + '&acquisition_mas_max=' + ([this.x+1])*1000 + '&acquisition_protocol=' + name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFiltersmAs + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(ee) {
                    chartmAsPerAcquisition.setTitle({ text: defaultmAsTitle }, { text: '' });
                    chartmAsPerAcquisition.yAxis[0].setTitle({text:'mAs'});
                    chartmAsPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartmAsPerAcquisition.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartmAsPerAcquisition.tooltip.options.formatter = function(args) {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'mAs per acquisition protocol',
            useHTML: true
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: [],
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
                text: 'mAs'
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
            name: 'Mean mAs per acquisition protocol',
            data: []
        }, {
            name: 'Median mAs per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });
    switch(chartSorting) {
        case 'freq':
            twoSeriesSort('#chartAcquisitionMeanmAs', 'freq', chartSortingDirection, 0);
            break;
        case 'dap':
            twoSeriesSort('#chartAcquisitionMeanmAs', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            twoSeriesSort('#chartAcquisitionMeanmAs', 'name', chartSortingDirection, 0);
            break;
        default:
            twoSeriesSort('#chartAcquisitionMeanmAs', 'name', chartSortingDirection, 0);
    }
});