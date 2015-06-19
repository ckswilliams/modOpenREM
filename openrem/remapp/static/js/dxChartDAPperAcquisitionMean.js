$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DAP per acquisition protocol';
var tooltipData = [2];

var chartDAPperAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'container',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (protocolNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartDAPperAcquisition.setTitle({ text: drilldownTitle + e.point.name + ' DAP values' }, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartDAPperAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartDAPperAcquisition.xAxis[0].setTitle({text:'DAP range (cGy.cm<sup>2</sup>)'});
                    chartDAPperAcquisition.xAxis[0].setCategories([], true);
                    chartDAPperAcquisition.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var linkText = 'acquisition_dap_min=' + (protocolBins[tooltipData[1]][this.x])/1000000 + '&acquisition_dap_max=' + (protocolBins[tooltipData[1]][this.x+1])/1000000 + '&acquisition_protocol=' + tooltipData[0];
                            xyArr.push('<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFilters + '">Click to view</a></td></tr></table>');
                        });
                        return xyArr.join('<br/>');
                    }
                },
                drillup: function(e) {
                    chartDAPperAcquisition.setTitle({ text: defaultTitle }, { text: '' });
                    chartDAPperAcquisition.yAxis[0].setTitle({text:'Mean DAP (cGy.cm<sup>2</sup>)'});
                    chartDAPperAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartDAPperAcquisition.xAxis[0].setCategories(protocolNames, true);
                    chartDAPperAcquisition.xAxis[0].update({labels:{rotation:90}});
                    chartDAPperAcquisition.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var index = protocolNames.indexOf(this.x);
                            xyArr.push(this.x + '<br/>' + this.y.toFixed(1) + ' cGy.cm<sup>2</sup>' + '<br/>(n=' + seriesDataN[index] + ')');
                        });
                        return xyArr.join('<br/>');
                    }
                }
            }
        },
        title: {
            text: 'Mean DAP per acquisition protocol'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: protocolNames,
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
                text: 'Mean DAP (cGy.cm<sup>2</sup>)'
            }
        },
        tooltip: {
            formatter: function () {
                var index = protocolNames.indexOf(this.x);
                var comment = this.x + '<br/>' + this.y.toFixed(1) + ' cGy.cm<sup>2</sup>' + '<br/>(n=' + seriesDataN[index] + ')';
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
            name: 'Mean DAP per acquisition protocol',
            data: seriesData
        }],
        drilldown: {
            series: seriesDrilldown
        }
    });
});

