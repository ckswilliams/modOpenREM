$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Median DLP per study description';
    var bins = [];
    var name = '';

    var chartStudyDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramStudyPlotDIV',
            events: {
                drilldown: function (e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartStudyDLP.setTitle({text: drilldownTitle + e.point.name}, {text: '(n = ' + e.point.freq + ')'});
                    chartStudyDLP.yAxis[0].setTitle({text: 'Number'});
                    chartStudyDLP.xAxis[0].setTitle({text: 'DLP range (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setCategories([], true);
                    chartStudyDLP.tooltip.options.formatter = function (e) {
                        var linkText = 'study_dlp_min=' + bins[this.x] + '&study_dlp_max=' + bins[this.x + 1] + '&study_description=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?studyhist=1&' + linkText + tooltipFiltersStudy + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    chartStudyDLP.setTitle({text: defaultTitle}, {text: ''});
                    chartStudyDLP.yAxis[0].setTitle({text: 'Median DLP (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setTitle({text: 'Study description'});
                    chartStudyDLP.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartStudyDLP.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Median DLP per study description'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: 'Study description'
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
                text: 'Median DLP (mGy.cm)'
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
            name: 'Median DLP per study',
            data: []
        }],
        drilldown: {
            series: []
        }
    });
    switch(chartSorting) {
        case 'freq':
            seriesSort('#histogramStudyPlotDIV', 'freq', chartSortingDirection);
            break;
        case 'dlp':
            seriesSort('#histogramStudyPlotDIV', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#histogramStudyPlotDIV', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#histogramStudyPlotDIV', 'name', 1);
    }
});