function chartAverageAndHistogram(default_title, norm_btn_class, instr_class, render_div,
                                  value_label, value_units, avg_label, cat_label, cat_counter,
                                  fld_min, fld_max, fld_multiplier, fld_cat_name,
                                  tooltip_filters, href_start) {
    var bins = [];
    var name = '';

    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        lang: {
            drillUpText: '◁ Back to ' + default_title.charAt(0).toLowerCase() + default_title.slice(1)
        },
        chart: {
            type: 'column',
            zoomType: 'x',
            resetZoomButton: {
                theme: {
                    display: 'none'
                }
            },
            renderTo: render_div,
            events: {
                drilldown: function (e) {
                    $(norm_btn_class).css('display','inline-block');
                    $(instr_class).css('display','none');
                    this.viewData(false, false, true);

                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');

                    if (typeof this.options.drilldown.normalise == 'undefined') this.options.drilldown.normalise = false;

                    var drilldownTitle;
                    if (!e.points) drilldownTitle = 'Histogram of '; else drilldownTitle = 'Histograms of ';
                    drilldownTitle += e.point.name + ' ' + value_label + ' values';
                    if (this.options.drilldown.normalise) drilldownTitle += ' (normalised)';

                    this.setTitle({
                        text: drilldownTitle
                    }, false);
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
                            text: value_label + ' range (' + value_units + ')'
                        },
                        categories: [],
                        max: (typeof(e.seriesOptions) !== 'undefined') ? e.seriesOptions.data.length - 1 : this.xAxis[0].max
                    }, false);
                    this.tooltip.options.formatter = function (e) {
                        var linkText = fld_min + '=' + (bins[this.x])*fld_multiplier + '&' + fld_max + '=' + (bins[this.x + 1])*fld_multiplier + '&' + fld_cat_name + '=' + name;
                        if (this.series.name != 'All systems') linkText += '&display_name=' + this.series.name;

                        var value_to_write;
                        if (e.chart.options.drilldown.normalise) {
                            for (var i=0; i<e.chart.options.drilldown.series.length; i++) {
                                if (e.chart.options.drilldown.series[i].id == this.series.name + name) {
                                    var max_value = Math.max.apply(Math, e.chart.options.drilldown.series[i].original_data.map(function(v) {return v;}));
                                }
                            }
                            value_to_write = max_value * this.y;
                        } else {
                            value_to_write = this.y;
                        }
                        return '<table style="text-align: center"><tr><td>' + value_to_write.toFixed(0) + ' ' + cat_counter + '</td></tr><tr><td><a href="' + href_start + linkText + tooltip_filters + '">Click to view</a></td></tr></table>';
                    };
                },
                drillup: function (e) {
                    $(norm_btn_class).css('display','none');
                    $(instr_class).css('display','block');
                    this.viewData(false, false, true);

                    this.setTitle({
                        text: default_title
                    }, false);
                    this.yAxis[0].update({
                        title: {
                            text: avg_label + ' ' + value_label + ' (' + value_units + ')'
                        },
                        max: null,
                        labels: {
                            format: null
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: cat_label
                        },
                        categories: {
                            formatter: function () {
                                return this.point.category;
                            }
                        },
                        max: e.seriesOptions.data.length - 1
                    }, false);
                    this.tooltip.options.formatter = function () {
                        return this.point.tooltip;
                    };
                }
            }
        },
        title: {
            useHTML: true,
            text: default_title
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: cat_label
            },
            labels: {
                useHTML: true,
                rotation: 90
            },
            minRange: 1,
            min: 0
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: avg_label + ' ' + value_label + ' (' + value_units + ')'
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
                borderColor: '#999999',
                turboThreshold: 5000 // Greater than the 1000 default to enable large data series to be plotted
            }
        },
        series: [],
        drilldown: {
            series: []
        }
    });
}