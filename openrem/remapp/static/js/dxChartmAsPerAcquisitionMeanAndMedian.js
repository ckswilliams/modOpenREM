$(function () {
    var defaultmAsTitle   = 'mAs per acquisition protocol';
    var bins = [];
    var name = '';

    var chartmAsPerAcquisition = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            type: 'column',
            renderTo: 'chartAcquisitionMeanmAs',
            events: {
                drilldown: function(e) {
                    $('.mas-hist-norm-btn').css('display','inline-block');
                    $('.mas-instructions').css('display','none');
                    if (chartFullScreen == true) updateFullScreen($('#'+this.renderTo.id).parent().parent()[0].id, this.renderTo.id);

                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');

                    if (typeof this.options.drilldown.normalise == 'undefined') this.options.drilldown.normalise = false;

                    var drilldownTitle;
                    if (!e.points) drilldownTitle = 'Histogram of '; else drilldownTitle = 'Histograms of ';
                    drilldownTitle += e.point.name + ' mAs values';
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
                            text:'mAs range'
                        },
                        categories: []
                    }, false);
                    this.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_mas_min=' + (bins[this.x])*1000 + '&acquisition_mas_max=' + (bins[this.x+1])*1000 + '&acquisition_protocol=' + name;
                        if (this.series.name != 'All systems') linkText += '&display_name=' + this.series.name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFiltersmAs + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    $('.mas-hist-norm-btn').css('display','none');
                    $('.mas-instructions').css('display','inline-block');
                    if (chartFullScreen == true) updateFullScreen($('#'+this.renderTo.id).parent().parent()[0].id, this.renderTo.id);

                    this.setTitle({
                        text: defaultmAsTitle
                    });
                    this.yAxis[0].update({
                        title: {
                            text:'mAs'
                        },
                        max: null,
                        labels: {
                            format: null
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text:'Protocol name'
                        },
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    });
                    this.tooltip.options.formatter = function() {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: defaultmAsTitle
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: [],
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
                text: 'mAs'
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