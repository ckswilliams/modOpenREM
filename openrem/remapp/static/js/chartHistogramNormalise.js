/*eslint security/detect-object-injection: "off" */

function normaliseHistograms(chartContainer) {
    var chart, histogramData, i, j, seriesMax;

    chart = $(chartContainer).highcharts();

    if (typeof chart.options.drilldown.normalise === "undefined") {chart.options.drilldown.normalise = false;}

    histogramData = [];

    for (i = 0; i < chart.options.drilldown.series.length; i++) {
        histogramData.push({
            id: chart.options.drilldown.series[i].id,
            name: chart.options.drilldown.series[i].name,
            useHTML: true,
            data: [],
            originalData: []
        });

        if (!chart.options.drilldown.normalise) {seriesMax = Math.max.apply(Math, chart.options.drilldown.series[i]["data"].map(function(v) {return v[1];}));}

        for (j = 0; j < chart.options.drilldown.series[i]["data"].length; j++) {
            histogramData[i]["originalData"].push(
                chart.options.drilldown.normalise ? chart.options.drilldown.series[i]["originalData"][j] : chart.options.drilldown.series[i]["data"][j][1]
            );

            histogramData[i]["data"].push([
                chart.options.drilldown.series[i]["data"][j][0],
                chart.options.drilldown.normalise ? histogramData[i]["originalData"][j] : histogramData[i]["originalData"][j] / seriesMax
            ]);
        }
    }

    chart.options.drilldown.series = histogramData;

    // Update the displayed chart if the user is viewing a histogram
    if (typeof chart.drilldownLevels != "undefined") {
        if (chart.drilldownLevels.length !== 0) {
            var index;

            chart.setTitle({
                text: chart.options.drilldown.normalise ? chart.title.textStr.substring(0, chart.title.textStr.indexOf(" (normalised)")) : chart.title.textStr + " (normalised)"
            }, false);

            chart.yAxis[0].update({
                title: {
                    text: chart.options.drilldown.normalise ? "Number" : "Normalised"
                },
                labels: {
                    format: chart.options.drilldown.normalise ? null : "{value:.2f}"
                },
                max: chart.options.drilldown.normalise ? null : 1.0
            }, false);

            for (i = 0; i < chart.series.length; i++) {

                // Find the index of histogramData that contains the matching id of the current series
                index = histogramData.map(function (element) {
                    return element.id;
                }).indexOf(chart.series[i].options.id);

                // Use the appropriate histogramData to update the series y values
                for (j = 0; j < chart.series[i].data.length; j++) {
                    chart.series[i].data[j].update({
                        y: histogramData[index].data[j][1]
                    }, false);
                }

                chart.redraw({duration: 1000});
            }
        }
    }

    chart.options.drilldown.normalise ? chart.options.drilldown.normalise = false : chart.options.drilldown.normalise = true;
}