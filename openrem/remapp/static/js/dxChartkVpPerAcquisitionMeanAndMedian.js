$(function () {
var drilldownkVpTitle = 'Histogram of ';
var defaultkVpTitle   = 'kVp per acquisition protocol';
var bins = [];
var name = '';

var chartkVpPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeankVp',
            events: {
                drilldown: function(ee) {
                    bins = ee.point.bins;
                    name = (ee.point.name).replace('&amp;', '%26');
                    chartkVpPerAcquisition.setTitle({ text: drilldownkVpTitle + ee.point.name + ' kVp values' }, { text: '(n = ' + ee.point.freq +')' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'kVp range'});
                    chartkVpPerAcquisition.xAxis[0].setCategories([], true);
                    chartkVpPerAcquisition.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_kvp_min=' + bins[this.x] + '&acquisition_kvp_max=' + bins[this.x+1] + '&acquisition_protocol=' + name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFilterskVp + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(ee) {
                    chartkVpPerAcquisition.setTitle({ text: defaultkVpTitle }, { text: '' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'kVp'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartkVpPerAcquisition.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartkVpPerAcquisition.tooltip.options.formatter = function(args) {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'kVp per acquisition protocol'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: protocolkVpNames,
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
                text: 'kVp'
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
            name: 'Mean kVp',
            data: serieskVpData
        }, {
            name: 'Median kVp',
            data: $.extend(true, [], seriesMediankVpData)
        }],
        drilldown: {
            series: serieskVpDrilldown
        }
    });
});

