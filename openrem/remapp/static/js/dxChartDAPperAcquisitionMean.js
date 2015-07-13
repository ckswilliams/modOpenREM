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

    $('#sortAscY').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.y < a.y;
		});
        rebuildSeries();
    });

    $('#sortDesY').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.y > a.y;
		});
        rebuildSeries();
    });

    $('#sortAscFreq').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.freq < a.freq;
		});
        rebuildSeries();
    });

    $('#sortDesFreq').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.freq > a.freq;
		});
        rebuildSeries();
    });

    $('#sortAscAlph').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.category < a.category;
		});
        rebuildSeries();
    });

    $('#sortDesAlph').click(function() {
		chartDAPperAcquisition.series[0].data.sort(function(a, b) {
			return b.category > a.category;
		});
        rebuildSeries();
    });

    function rebuildSeries() {
        var newData = {};
        var newCategories = [];

        for (var i = 0; i < chartDAPperAcquisition.series[0].data.length; i++) {
            newData.x = i;
            newData.y = chartDAPperAcquisition.series[0].data[i].y;
            newData.category = chartDAPperAcquisition.series[0].data[i].category;
            newData.drilldown = chartDAPperAcquisition.series[0].data[i].drilldown;
            newData.name = chartDAPperAcquisition.series[0].data[i].name;
            newData.freq = chartDAPperAcquisition.series[0].data[i].freq;
            newCategories.push(chartDAPperAcquisition.series[0].data[i].category);
            chartDAPperAcquisition.series[0].data[i].update(newData, false);
        }
        chartDAPperAcquisition.xAxis[0].categories = newCategories;
        chartDAPperAcquisition.redraw({ duration: 1000 });
    }
});

