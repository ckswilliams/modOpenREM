$(function () {
    var defaultTitle   = 'DLP per requested procedure type';
    var bins = [];
    var name = '';

    var chartRequestDLP = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            type: 'column',
            renderTo: 'histogramRequestPlotDIV',
            events: {
                drilldown: function(e) {
                    $('.req-hist-norm-btn').css('display','inline-block');
                    $('.req-instructions').css('display','none');

                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');

                    if (typeof this.options.drilldown.normalise == 'undefined') this.options.drilldown.normalise = false;

                    var drilldownTitle;
                    if (!e.points) drilldownTitle = 'Histogram of '; else drilldownTitle = 'Histograms of ';
                    drilldownTitle += e.point.name + ' DLP values';
                    if (this.options.drilldown.normalise) drilldownTitle += ' (normalised)';

                    this.setTitle({
                        text: drilldownTitle
                    });
                    this.yAxis[0].update({
                        title: {
                            text: (this.options.drilldown.normalise ? 'Normalised' : 'Number')
                        },
                        max: (this.options.drilldown.normalise ? 1.0 : null),
                        labels: {
                            format: (this.options.drilldown.normalise ? '{value:.2f}' : null)
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: 'DLP range (mGy.cm)'
                        },
                        categories: []
                    }, false);
                    this.tooltip.options.formatter = function(e) {
                        var linkText = 'study_dlp_min=' + bins[this.x] + '&study_dlp_max=' + bins[this.x+1] + '&requested_procedure=' + name;
                        if (this.series.name != 'All systems') linkText += '&display_name=' + this.series.name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?requesthist=1&' + linkText + tooltipFiltersRequest + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    $('.req-hist-norm-btn').css('display','none');
                    $('.req-instructions').css('display','inline-block');

                    this.setTitle({
                        text: defaultTitle
                    });
                    this.yAxis[0].update({
                        title: {
                            text: 'DLP (mGy.cm)'
                        },
                        max: null,
                        labels: {
                            format: null
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: 'Requested procedure'
                        },
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    this.tooltip.options.formatter = function(args) {
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
                borderWidth: 1,
                borderColor: '#999999'
            }
        },
        series: [],
        drilldown: {
            series: []
        }
    });
});