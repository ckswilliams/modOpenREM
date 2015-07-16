$(function () {

var drilldownkVpTitle = 'Histogram of ';
var defaultkVpTitle   = 'Median kVp per acquisition protocol';
var tooltipkVpData = [2];

var chartkVpPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeankVp',
            events: {
                drilldown: function(ee) {
                    tooltipkVpData[0] = (protocolkVpNames[ee.point.x]).replace('&amp;', '%26');
                    tooltipkVpData[1] = ee.point.x;
                    chartkVpPerAcquisition.setTitle({ text: drilldownkVpTitle + ee.point.name + ' kVp values' }, { text: '(n = ' + serieskVpDataN[ee.point.x] +')' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'kVp range'});
                    chartkVpPerAcquisition.xAxis[0].setCategories([], true);
                    chartkVpPerAcquisition.tooltip.options.formatter = function() {
                        var linkText = 'acquisition_kvp_min=' + protocolkVpBins[tooltipkVpData[1]][this.x] + '&acquisition_kvp_max=' + protocolkVpBins[tooltipkVpData[1]][this.x+1] + '&acquisition_protocol=' + tooltipkVpData[0];
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFilterskVp + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(ee) {
                    chartkVpPerAcquisition.setTitle({ text: defaultkVpTitle }, { text: '' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'Median kVp'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartkVpPerAcquisition.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartkVpPerAcquisition.tooltip.options.formatter = function() {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'Median kVp per acquisition protocol'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: protocolkVpNames,
            title: {
                useHTML: true,
                text: 'Protocol name'
            },
            labels: {
                rotation:90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'Median kVp'
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
            name: 'Median kVp',
            data: seriesMediankVpData
        }],
        drilldown: {
            series: serieskVpDrilldown
        }
    });
});

