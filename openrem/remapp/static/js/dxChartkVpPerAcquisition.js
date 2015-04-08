$(function () {

var drilldownkVpTitle = 'Histogram of ';
var defaultkVpTitle   = 'Mean kVp per acquisition protocol';
var tooltipkVpData = [1];

var chartkVpPerAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeankVp',
            events: {
                drilldown: function(ee) {
                    tooltipkVpData[0] = ee.point.x;
                    chartkVpPerAcquisition.setTitle({ text: drilldownkVpTitle + ee.point.name + ' kVp values' }, { text: '(n = ' + serieskVpDataN[ee.point.x] +')' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'kVp range'});
                    chartkVpPerAcquisition.xAxis[0].setCategories([], true);
                    chartkVpPerAcquisition.xAxis[0].update({labels:{rotation:0}});
                    chartkVpPerAcquisition.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var linkText = tooltipkVpData[0];
                            xyArr.push('<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr></table>');
                        });
                        return xyArr.join('<br/>');
                    }
                },
                drillup: function(ee) {
                    chartkVpPerAcquisition.setTitle({ text: defaultkVpTitle }, { text: '' });
                    chartkVpPerAcquisition.yAxis[0].setTitle({text:'Mean kVp'});
                    chartkVpPerAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartkVpPerAcquisition.xAxis[0].setCategories(protocolkVpNames, true);
                    chartkVpPerAcquisition.xAxis[0].update({labels:{rotation:90}});
                    chartkVpPerAcquisition.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var index = protocolkVpNames.indexOf(this.x);
                            xyArr.push(this.x + '<br/>' + this.y.toFixed(1) + ' kVp' + '<br/>(n=' + serieskVpDataN[index] + ')');
                        });
                        return xyArr.join('<br/>');
                    }
                }
            }
        },
        title: {
            text: 'Mean kVp per acquisition protocol'
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
                text: 'Mean kVp'
            }
        },
        tooltip: {
            formatter: function () {
                var index = protocolkVpNames.indexOf(this.x);
                var comment = this.x + '<br/>' + this.y.toFixed(1) + ' kVp' + '<br/>(n=' + serieskVpDataN[index] + ')';
                return comment;
            },
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean kVp per acquisition protocol',
            data: serieskVpData
        }],
        drilldown: {
            series: serieskVpDrilldown
        }
    });
});

