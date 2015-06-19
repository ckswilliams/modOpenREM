$(function () {

var drilldownkVpTitle = 'Histogram of ';
var defaultkVpTitle   = 'kVp per acquisition protocol';
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
                    chartkVpPerAcquisition.tooltip.options.formatter = function(args) {
                        var linkText = 'acquisition_kvp_min=' + protocolkVpBins[tooltipkVpData[1]][this.x] + '&acquisition_kvp_max=' + protocolkVpBins[tooltipkVpData[1]][this.x+1] + '&acquisition_protocol=' + tooltipkVpData[0];
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFilterskVp + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(ee) {
                    chartkVpPerAcquisition.setTitle({ text: defaultkVpTitle }, { text: '' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'kVp'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartkVpPerAcquisition.xAxis[0].setCategories(protocolkVpNames, true);
                    chartkVpPerAcquisition.xAxis[0].update({labels:{rotation:90}});
                    chartkVpPerAcquisition.tooltip.options.formatter = function(args) {
                        var this_point_index = this.series.data.indexOf(this.point);
                        if (this.series.name.indexOf('Mean') != -1) {
                            var this_series_label = ' mean kVp';
                            var this_series = args.chart.series[0];
                        }
                        else {
                            var this_series_label = ' median kVp';
                            var this_series = args.chart.series[1];
                        }
                        var this_point = this_series.data[this_point_index];
                        return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + serieskVpDataN[this_point_index] + ')';
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
                var this_point_index = this.series.data.indexOf(this.point);
                if (this.series.name.indexOf('Mean') != -1) {
                    var this_series_label = ' mean kVp';
                    var this_series = args.chart.series[0];
                }
                else {
                    var this_series_label = ' median kVp';
                    var this_series = args.chart.series[1];
                }
                var this_point = this_series.data[this_point_index];
                return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + serieskVpDataN[this_point_index] + ')';
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
            name: 'Mean kVp per acquisition protocol',
            data: serieskVpData
        }, {
            name: 'Median kVp per acquisition protocol',
            data: seriesMediankVpData
        }],
        drilldown: {
            series: serieskVpDrilldown
        }
    });
});

