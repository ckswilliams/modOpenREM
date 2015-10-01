$(function () {
    var drilldownmAsTitle = 'Histogram of ';
    var defaultmAsTitle   = 'Median mAs per acquisition protocol';
    var bins = [];
    var name = '';

    var chartmAsPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeanmAs',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartmAsPerAcquisition.setTitle({ text: drilldownmAsTitle + e.point.name + ' mAs values' }, { text: '(n = ' + e.point.freq +')' });
                    chartmAsPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartmAsPerAcquisition.xAxis[0].setTitle({text:'mAs range'});
                    chartmAsPerAcquisition.xAxis[0].setCategories([], true);
                    chartmAsPerAcquisition.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_mas_min=' + (bins[this.x])*1000 + '&acquisition_mas_max=' + (bins[this.x+1])*1000 + '&acquisition_protocol=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFiltersmAs + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartmAsPerAcquisition.setTitle({ text: defaultmAsTitle }, { text: '' });
                    chartmAsPerAcquisition.yAxis[0].setTitle({text:'Median mAs'});
                    chartmAsPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartmAsPerAcquisition.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartmAsPerAcquisition.tooltip.options.formatter = function() {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'Median mAs per acquisition protocol',
            useHTML: true
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
                rotation:90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'Median mAs'
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
            name: 'Median mAs per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });
    switch(chartSorting) {
        case 'freq':
            seriesSort('#chartAcquisitionMeanmAs', 'freq', chartSortingDirection);
            break;
        case 'dap':
            seriesSort('#chartAcquisitionMeanmAs', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#chartAcquisitionMeanmAs', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#chartAcquisitionMeanmAs', 'name', 1);
    }
});