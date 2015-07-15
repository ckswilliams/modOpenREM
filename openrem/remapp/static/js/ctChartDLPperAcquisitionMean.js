//$(function () {

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

    function seriesSort(chartContainer, p, d) {
        var chart = $(chartContainer).highcharts();
        if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "object") {
            bubbleSort(chart.series[0].data, p, d);
            rebuildSeries(chartContainer);
        }
    }

    function rebuildSeries(chartContainer) {
        var chart = $(chartContainer).highcharts();
        var newData = {};
        var newCategories = [];

        for (var i = 0; i < chart.series[0].data.length; i++) {
            newData.x = i;
            newData.y = chart.series[0].data[i].y;
            newData.category = chart.series[0].data[i].category;
            newData.drilldown = chart.series[0].data[i].drilldown;
            newData.name = chart.series[0].data[i].name;
            newData.freq = chart.series[0].data[i].freq;
            newCategories.push(chart.series[0].data[i].category);
            chart.series[0].data[i].update(newData, false);
        }
        chart.xAxis[0].categories = newCategories;
        chart.redraw({ duration: 1000 });
    }

    function bubbleSort(a, p, d) {
        var swapped;
        do {
            swapped = false;
            for (var i=0; i < a.length-1; i++) {
                if (d == 1) {
                    if (a[i][p] > a[i + 1][p]) {
                        var temp = a[i];
                        a[i] = a[i + 1];
                        a[i + 1] = temp;
                        swapped = true;
                    }
                }
                else {
                    if (a[i][p] < a[i + 1][p]) {
                        var temp = a[i];
                        a[i] = a[i + 1];
                        a[i + 1] = temp;
                        swapped = true;
                    }
                }
            }
        } while (swapped);
    }
//});