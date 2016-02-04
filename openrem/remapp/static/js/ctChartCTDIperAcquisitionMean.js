$(function () {
    var defaultTitle = 'Mean CTDI<sub>vol</sub> per acquisition protocol type';
    var bins = [];
    var name = '';

    var chartAcquisitionDLP = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            type: 'column',
            renderTo: 'histogramAcquisitionPlotCTDIdiv',
            events: {
                drilldown: function (e) {
                    $('.acq-hist-norm-btn').css('display','inline-block');

                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');

                    if (typeof this.options.drilldown.normalise == 'undefined') this.options.drilldown.normalise = false;

                    var drilldownTitle;
                    if (!e.points) drilldownTitle = 'Histogram of '; else drilldownTitle = 'Histograms of ';
                    drilldownTitle += e.point.name + ' CTDI<sub>vol</sub> values';
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
                            text: 'CTDI<sub>vol</sub> range (mGy.cm)'
                        },
                        categories: []
                    }, false);
                    this.tooltip.options.formatter = function (e) {
                        var linkText = 'acquisition_ctdi_min=' + bins[this.x] + '&acquisition_ctdi_max=' + bins[this.x + 1] + '&acquisition_protocol=' + name;
                        if (this.series.name != 'All systems') linkText += '&display_name=' + this.series.name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function (e) {
                    $('.acq-hist-norm-btn').css('display','none');

                    this.setTitle({
                        text: defaultTitle
                    });
                    this.yAxis[0].update({
                        title: {
                            text: 'Mean CTDI<sub>vol</sub> (mGy.cm)'
                        },
                        max: null,
                        labels: {
                            format: null
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: 'Acquisition protocol'
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
                text: 'Acquisition protocol type'
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
                text: 'Mean CTDI<sub>vol</sub> (mGy.cm)'
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

    switch(chartSorting) {
        case 'freq':
            anySeriesSort('#histogramAcquisitionPlotCTDIdiv', 'freq', chartSortingDirection, 0);
            break;
        case 'ctdi':
            anySeriesSort('#histogramAcquisitionPlotCTDIdiv', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            anySeriesSort('#histogramAcquisitionPlotCTDIdiv', 'name', chartSortingDirection, 0);
            break;
        default:
            anySeriesSort('#histogramAcquisitionPlotCTDIdiv', 'name', 1, 0);
    }

});