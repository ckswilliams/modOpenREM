/*global Highcharts, hideSeriesButtons, resetSeriesButtons*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */
/*eslint object-shorthand: "off" */

function chartAverageAndHistogram(defaultTitle, normBtnClass, instrClass, renderDiv,
                                  valueLabel, valueUnits, avgLabel, catLabel, catCounter,
                                  fldMin, fldMax, fldMultiplier, fldCatName,
                                  tooltipFilters, hrefStart, hideBtnStub) {
    var bins = [];
    var name = "";

    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        lang: {
            drillUpText: "◁ Back to " + defaultTitle.charAt(0).toLowerCase() + defaultTitle.slice(1)
        },
        chart: {
            type: "column",
            zoomType: "x",
            resetZoomButton: {
                theme: {
                    display: "none"
                }
            },
            renderTo: renderDiv,
            events: {
                drilldown: function (e) {
                    $(normBtnClass).css("display","inline-block");
                    $(instrClass).css("display","none");
                    this.viewData(false, false, true);

                    bins = e.point.bins;
                    name = (e.point.name).replace("&amp;", "%26");

                    if (typeof this.options.drilldown.normalise === "undefined") {this.options.drilldown.normalise = false;}

                    var drilldownTitle;
                    if (!e.points) {
                        drilldownTitle = "Histogram of ";
                        hideSeriesButtons(hideBtnStub);
                    }
                    else {
                        drilldownTitle = "Histograms of ";
                    }
                    drilldownTitle += e.point.name + " " + valueLabel + " values";
                    if (this.options.drilldown.normalise) {drilldownTitle += " (normalised)";}

                    this.setTitle({
                        text: drilldownTitle
                    }, false);
                    this.yAxis[0].update({
                        title: {
                            text: (this.options.drilldown.normalise ? "Normalised" : "Number")
                        },
                        max: (this.options.drilldown.normalise ? 1.0 : null),
                        labels: {
                            format: (this.options.drilldown.normalise ? "{value:.2f}" : null)
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: valueLabel + " range (" + valueUnits + ")"
                        },
                        categories: [],
                        max: (typeof(e.seriesOptions) !== "undefined") ? e.seriesOptions.data.length - 1 : this.xAxis[0].max
                    }, false);
                    this.tooltip.options.formatter = function (e) {
                        var valueToWrite;
                        var maxValue;
                        if (e.chart.options.drilldown.normalise) {
                            for (var i=0; i<e.chart.options.drilldown.series.length; i++) {
                                if (e.chart.options.drilldown.series[i].id === this.series.name + name) {
                                    maxValue = Math.max.apply(Math, e.chart.options.drilldown.series[i].originalData.map(function(v) {return v;}));
                                }
                            }
                            valueToWrite = maxValue * this.y;
                        } else {
                            valueToWrite = this.y;
                        }
                        if (hrefStart !== 0) {
                            var linkText = fldMin + "=" + (bins[this.x])*fldMultiplier + "&" + fldMax + "=" + (bins[this.x + 1])*fldMultiplier + "&" + fldCatName + "=" + name;
                            if (this.series.name !== "All systems") {
                                linkText += "&display_name=" + this.series.name;
                            }
                            return "<table style='text-align: center'><tr><td>" + valueToWrite.toFixed(0) + " " + catCounter + "</td></tr><tr><td><a href='" + encodeURI(hrefStart + linkText + tooltipFilters).replace("+", encodeURIComponent("+")) + "'>Click to view</a></td></tr></table>";
                        } else {
                            return "<table style='text-align: center'><tr><td>" + valueToWrite.toFixed(0) + " " + catCounter + "</td></tr></table>";
                        }
                    };
                },
                drillup: function (e) {
                    $(normBtnClass).css("display","none");
                    $(instrClass).css("display","block");
                    this.viewData(false, false, true);

                    if (this.series.length > 2) {
                        resetSeriesButtons(hideBtnStub);
                    }

                    this.setTitle({
                        text: defaultTitle
                    }, false);
                    this.yAxis[0].update({
                        title: {
                            text: avgLabel + " " + valueLabel + " (" + valueUnits + ")"
                        },
                        max: null,
                        labels: {
                            format: null
                        }
                    }, false);
                    this.xAxis[0].update({
                        title: {
                            text: catLabel
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
            text: defaultTitle
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: catLabel
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
                text: avgLabel + " " + valueLabel + " (" + valueUnits + ")"
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
                borderColor: "#999999",
                turboThreshold: 5000 // Greater than the 1000 default to enable large data series to be plotted
            }
        },
        series: [],
        drilldown: {
            series: []
        }
    });
}
