$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DLP per acquisition protocol';
var tooltipData = [2];

var chartAcqDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDIV',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (protocolNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartAcqDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartAcqDLP.yAxis[0].setTitle({text:'Number'});
                    chartAcqDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setCategories([], true);
                    chartAcqDLP.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var linkText = 'acquisition_dlp_min=' + protocolBins[tooltipData[1]][this.x] + '&acquisition_dlp_max=' + protocolBins[tooltipData[1]][this.x+1] + '&acquisition_protocol=' + tooltipData[0];
                            xyArr.push('<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcq + '">Click to view</a></td></tr></table>');
                        });
                        return xyArr.join('<br/>');
                    }
                },
                drillup: function(e) {
                    chartAcqDLP.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqDLP.yAxis[0].setTitle({text:'Mean DLP (mGy.cm)'});
                    chartAcqDLP.xAxis[0].setTitle({text:'Protocol name'});
                    chartAcqDLP.xAxis[0].setCategories(protocolNames, true);
                    chartAcqDLP.xAxis[0].update({labels:{rotation:90}});
                    chartAcqDLP.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var index = protocolNames.indexOf(this.x);
                            xyArr.push(this.x + '<br/>' + this.y.toFixed(1) + ' mGy.cm' + '<br/>(n=' + seriesDataN[index] + ')');
                        });
                        return xyArr.join('<br/>');
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean DLP per acquisition protocol'
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
                text: 'Mean DLP (mGy.cm)'
            }
        },
        tooltip: {
            formatter: function () {
                var index = protocolNames.indexOf(this.x);
                var comment = this.x + '<br/>' + this.y.toFixed(1) + ' mGy.cm' + '<br/>(n=' + seriesDataN[index] + ')';
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
            useHTML: true,
            name: 'Mean DLP',
            data: seriesData
        }],
        drilldown: {
            series: seriesDrilldown
        }
    });

    $('#sortAscY').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.y < a.y;
		});
        rebuildSeries();
    });

    $('#sortDesY').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.y > a.y;
		});
        rebuildSeries();
    });

    $('#sortAscFreq').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.freq < a.freq;
		});
        rebuildSeries();
    });

    $('#sortDesFreq').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.freq > a.freq;
		});
        rebuildSeries();
    });

    $('#sortAscAlph').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.category < a.category;
		});
        rebuildSeries();
    });

    $('#sortDesAlph').click(function() {
		chartAcqDLP.series[0].data.sort(function(a, b) {
			return b.category > a.category;
		});
        rebuildSeries();
    });

    function rebuildSeries() {
        var newData = {};
        var newCategories = [];

        for (var i = 0; i < chartAcqDLP.series[0].data.length; i++) {
            newData.x = i;
            newData.y = chartAcqDLP.series[0].data[i].y;
            newData.category = chartAcqDLP.series[0].data[i].category;
            newData.drilldown = chartAcqDLP.series[0].data[i].drilldown;
            newData.name = chartAcqDLP.series[0].data[i].name;
            newData.freq = chartAcqDLP.series[0].data[i].freq;
            newCategories.push(chartAcqDLP.series[0].data[i].category);
            chartAcqDLP.series[0].data[i].update(newData, false);
        }
        chartAcqDLP.xAxis[0].categories = newCategories;
        chartAcqDLP.redraw({ duration: 1000 });
    }
});

