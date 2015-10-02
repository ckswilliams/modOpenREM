$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle   = 'DLP per requested procedure type';
    var bins = [];
    var name = '';

    var chartRequestDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramRequestPlotDIV',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartRequestDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + e.point.freq +')' });
                    chartRequestDLP.yAxis[0].setTitle({text:'Number'});
                    chartRequestDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartRequestDLP.xAxis[0].setCategories([], true);
                    chartRequestDLP.tooltip.options.formatter = function(e) {
                        var linkText = 'study_dlp_min=' + bins[this.x] + '&study_dlp_max=' + bins[this.x+1] + '&requested_procedure=' + name;
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
            categories: [1,2,3,4,5],
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
            name: 'Mean DLP per requested procedure',
            data: []
        }, {
            useHTML: true,
            name: 'Median DLP per requested procedure',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            twoSeriesSort('#histogramRequestPlotDIV', 'freq', chartSortingDirection, 0);
            break;
        case 'dlp':
            twoSeriesSort('#histogramRequestPlotDIV', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            twoSeriesSort('#histogramRequestPlotDIV', 'name', chartSortingDirection, 0);
            break;
        default:
            twoSeriesSort('#histogramRequestPlotDIV', 'name', chartSortingDirection, 0);
    }

});