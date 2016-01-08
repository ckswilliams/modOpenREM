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
                    this.setTitle({
                        text: drilldownTitle + e.point.name
                    });
                    this.yAxis[0].update({
                        title: {
                            text: 'Number'
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: 'DLP range (mGy.cm)'
                        },
                        categories: []
                    }, false);
                    this.tooltip.options.formatter = function (e) {
                        var linkText = 'study_dlp_min=' + bins[this.x] + '&study_dlp_max=' + bins[this.x + 1] + '&requested_procedure=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?requesthist=1&' + linkText + tooltipFiltersRequest + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    this.setTitle({
                        text: defaultTitle
                    });
                    this.yAxis[0].update({
                        title: {
                            text: 'Mean DLP (mGy.cm)'
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: 'Requested procedure'
                        },
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    });
                    this.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: defaultTitle
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
        series: [],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            anySeriesSort('#histogramRequestPlotDIV', 'freq', chartSortingDirection, 0);
            break;
        case 'dlp':
            anySeriesSort('#histogramRequestPlotDIV', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            anySeriesSort('#histogramRequestPlotDIV', 'name', chartSortingDirection, 0);
            break;
        default:
            anySeriesSort('#histogramRequestPlotDIV', 'name', 1, 0);
    }

});