$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'DLP per study description';
var tooltipData = [2];

var chartStudyDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramStudyPlotDIV',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (studyNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartStudyDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + studySeriesDataN[e.point.x] +')' });
                    chartStudyDLP.yAxis[0].setTitle({text:'Number'});
                    chartStudyDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setCategories([], true);
                    chartStudyDLP.tooltip.options.formatter = function(args) {
                        var linkText = 'study_dlp_min=' + studyBins[tooltipData[1]][this.x] + '&study_dlp_max=' + studyBins[tooltipData[1]][this.x+1] + '&study_description=' + tooltipData[0];
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?studyhist=1&' + linkText + tooltipFiltersStudy + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartStudyDLP.setTitle({ text: defaultTitle }, { text: '' });
                    chartStudyDLP.yAxis[0].setTitle({text:'DLP (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setTitle({text:'Study description'});
                    chartStudyDLP.xAxis[0].setCategories(studyNames, true);
                    chartStudyDLP.xAxis[0].update({labels:{rotation:90}});
                    chartStudyDLP.tooltip.options.formatter = function(args) {
                        var this_point_index = this.series.data.indexOf(this.point);
                        if (this.series.name.indexOf('Mean') != -1) {
                            var this_series_label = ' mean DLP';
                            var this_series = args.chart.series[0];
                        }
                        else {
                            var this_series_label = ' median DLP';
                            var this_series = args.chart.series[1];
                        }
                        var this_point = this_series.data[this_point_index];
                        return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + studySeriesDataN[this_point_index] + ')';
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'DLP per study description'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: studyNames,
            title: {
                useHTML: true,
                text: 'Study description'
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
                var this_point_index = this.series.data.indexOf(this.point);
                if (this.series.name.indexOf('Mean') != -1) {
                    var this_series_label = ' mean DLP';
                    var this_series = args.chart.series[0];
                }
                else {
                    var this_series_label = ' median DLP';
                    var this_series = args.chart.series[1];
                }
                var this_point = this_series.data[this_point_index];
                return this.point.name + '<br/>' + this_point.y.toFixed(1) + this_series_label + '<br/>(n = ' + studySeriesDataN[this_point_index] + ')';
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
            name: 'Mean DLP per study description',
            data: studySeriesData
        }, {
            useHTML: true,
            name: 'Median DLP per study description',
            data: studySeriesMedianData
        }],
        drilldown: {
            series: studySeriesDrilldown
        }
    });
});

