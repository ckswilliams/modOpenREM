$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Mean DLP per requested procedure type';
    var bins = [];
    var name = '';

    var chartRequestDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramRequestPlotDIV',
            events: {
                drilldown: function (e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartRequestDLP.setTitle({text: drilldownTitle + e.point.name}, {text: '(n = ' + e.point.freq + ')'});
                    chartRequestDLP.yAxis[0].setTitle({text: 'Number'});
                    chartRequestDLP.xAxis[0].setTitle({text: 'DLP range (mGy.cm)'});
                    chartRequestDLP.xAxis[0].setCategories([], true);
                    chartRequestDLP.tooltip.options.formatter = function (e) {
                        var linkText = 'study_dlp_min=' + bins[this.x] + '&study_dlp_max=' + bins[this.x + 1] + '&requested_procedure=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?requesthist=1&' + linkText + tooltipFiltersRequest + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    chartRequestDLP.setTitle({text: defaultTitle}, {text: ''});
                    chartRequestDLP.yAxis[0].setTitle({text: 'Mean DLP (mGy.cm)'});
                    chartRequestDLP.xAxis[0].setTitle({text: 'Requested procedure'});
                    chartRequestDLP.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartRequestDLP.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean DLP per requested procedure type'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: 'Requested procedure type'
            },
            labels: {
                useHTML: true,
                rotation: 90
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
            useHTML: true,
            name: 'Mean DLP per requested procedure',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            seriesSort('#histogramRequestPlotDIV', 'freq', chartSortingDirection);
            break;
        case 'dlp':
            seriesSort('#histogramRequestPlotDIV', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#histogramRequestPlotDIV', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#histogramRequestPlotDIV', 'name', 1);
    }

});