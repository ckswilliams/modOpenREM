$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle = 'Median DLP per study description';
    var tooltipData = [2];

    var chartStudyDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramStudyPlotDIV',
            events: {
                drilldown: function (e) {
                    tooltipData[0] = (studyNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartStudyDLP.setTitle({text: drilldownTitle + e.point.name}, {text: '(n = ' + studySeriesDataN[e.point.x] + ')'});
                    chartStudyDLP.yAxis[0].setTitle({text: 'Number'});
                    chartStudyDLP.xAxis[0].setTitle({text: 'DLP range (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setCategories([], true);
                    chartStudyDLP.tooltip.options.formatter = function () {
                        var linkText = 'study_dlp_min=' + studyBins[tooltipData[1]][this.x] + '&study_dlp_max=' + studyBins[tooltipData[1]][this.x + 1] + '&study_description=' + tooltipData[0];
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
            categories: studyNames,
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
            name: 'Median DLP',
            data: studySeriesMedianData
        }],
        drilldown: {
            series: studySeriesDrilldown
        }
    });
});