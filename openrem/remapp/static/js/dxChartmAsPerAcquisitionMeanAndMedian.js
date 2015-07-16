$(function () {

var drilldownmAsTitle = 'Histogram of ';
var defaultmAsTitle   = 'mAs per acquisition protocol';
var tooltipmAsData = [2];

var chartmAsPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeanmAs',
            events: {
                drilldown: function(ee) {
                    tooltipmAsData[0] = (protocolmAsNames[ee.point.x]).replace('&amp;', '%26');
                    tooltipmAsData[1] = ee.point.x;
                    chartmAsPerAcquisition.setTitle({ text: drilldownmAsTitle + ee.point.name + ' mAs values' }, { text: '(n = ' + seriesmAsDataN[ee.point.x] +')' });
                    chartmAsPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartmAsPerAcquisition.xAxis[0].setTitle({text:'mAs range'});
                    chartmAsPerAcquisition.xAxis[0].setCategories([], true);
                    chartmAsPerAcquisition.tooltip.options.formatter = function(args) {
                        var linkText = 'acquisition_mas_min=' + (protocolmAsBins[tooltipmAsData[1]][this.x])*1000 + '&acquisition_mas_max=' + (protocolmAsBins[tooltipmAsData[1]][this.x+1])*1000 + '&acquisition_protocol=' + tooltipmAsData[0];
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
            text: 'mAs per acquisition protocol'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: protocolmAsNames,
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
            name: 'Mean mAs',
            data: seriesmAsData
        }, {
            name: 'Median mAs',
            data: seriesMedianmAsData
        }],
        drilldown: {
            series: seriesmAsDrilldown
        }
    });
});

