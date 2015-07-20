$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle   = 'DLP per requested procedure type';
    var tooltipData = [2];

    var chartRequestDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramRequestPlotDIV',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (requestNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartRequestDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + requestSeriesDataN[e.point.x] +')' });
                    chartRequestDLP.yAxis[0].setTitle({text:'Number'});
                    chartRequestDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartRequestDLP.xAxis[0].setCategories([], true);
                    chartRequestDLP.tooltip.options.formatter = function(args) {
                        var linkText = 'study_dlp_min=' + requestBins[tooltipData[1]][this.x] + '&study_dlp_max=' + requestBins[tooltipData[1]][this.x+1] + '&requested_procedure=' + tooltipData[0];
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?requesthist=1&' + linkText + tooltipFiltersRequest + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartRequestDLP.setTitle({ text: defaultTitle }, { text: '' });
                    chartRequestDLP.yAxis[0].setTitle({text:'DLP (mGy.cm)'});
                    chartRequestDLP.xAxis[0].setTitle({text:'Requested procedure'});
                    chartRequestDLP.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartRequestDLP.tooltip.options.formatter = function(args) {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'DLP per requested procedure type'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: requestNames,
            title: {
                useHTML: true,
                text: 'Requested procedure type'
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
                text: 'DLP (mGy.cm)'
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
            useHTML: true,
            name: 'Mean DLP',
            data: $.extend(true, [], requestSeriesData)
        }, {
            useHTML: true,
            name: 'Median DLP',
            data: $.extend(true, [], requestSeriesMedianData)
        }],
        drilldown: {
            series: requestSeriesDrilldown
        }
    });
});