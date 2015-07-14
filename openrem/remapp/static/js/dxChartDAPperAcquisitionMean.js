$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DAP per acquisition protocol';
var tooltipData = [2];
var originalData = seriesData;

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
            data: $.extend(true, [], originalData), // use copy
        }],
        drilldown: {
            series: seriesDrilldown
        }
    });

    $('#sortAscY').click(function() {
        bubbleSort(originalData, "y", 1);
        rebuildSeries();
    });

    $('#sortDesY').click(function() {
        bubbleSort(originalData, "y", -1);
        rebuildSeries();
    });

    $('#sortAscFreq').click(function() {
        bubbleSort(originalData, "freq", 1);
        rebuildSeries();
    });

    $('#sortDesFreq').click(function() {
        bubbleSort(originalData, "freq", -1);
        rebuildSeries();
    });

    $('#sortAscAlph').click(function() {
        bubbleSort(originalData, "name", 1);
        rebuildSeries();
    });

    $('#sortDesAlph').click(function() {
        bubbleSort(originalData, "name", -1);
        rebuildSeries();
    });

    function rebuildSeries() {
            var newData = {};
            var newCategories = [],
                newPoints = [],
                data = $.extend(true, [], originalData),
                point;

            for (var i = 0; i < data.length; i++) {
                point = data[i];
                newCategories.push(point.name);
                chartDAPperAcquisition.series[0].data[i].update({
                    name: point.name,
                    y: point.y,
                    x: i,
                    freq: point.freq,
                    drilldown: point.drilldown,
                    category: point.name
                }, false);
            }
            chartDAPperAcquisition.xAxis[0].categories = newCategories;
            chartDAPperAcquisition.redraw({ duration: 1000 });
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
});

