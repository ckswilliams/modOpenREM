function normaliseHistograms(chartContainer) {
    var chart, histogram_data, i, j, series_max;

    chart = $(chartContainer).highcharts();

    if (typeof chart.options.drilldown.normalise == 'undefined') chart.options.drilldown.normalise = false;

    histogram_data = [];

    for (i = 0; i < chart.options.drilldown.series.length; i++) {
        histogram_data.push({
            id: chart.options.drilldown.series[i].id,
            name: chart.options.drilldown.series[i].name,
            useHTML: true,
            data: [],
            original_data: []
        });

        if (!chart.options.drilldown.normalise) series_max = Math.max.apply(Math, chart.options.drilldown.series[i]["data"].map(function(v) {return v[1];}));

        for (j = 0; j < chart.options.drilldown.series[i]["data"].length; j++) {
            histogram_data[i]["original_data"].push(
                chart.options.drilldown.normalise ? chart.options.drilldown.series[i]["original_data"][j] : chart.options.drilldown.series[i]["data"][j][1]
            );

            histogram_data[i]["data"].push([
                chart.options.drilldown.series[i]["data"][j][0],
                chart.options.drilldown.normalise ? histogram_data[i]["original_data"][j] : histogram_data[i]["original_data"][j] / series_max
            ]);
        }
    }

    chart.options.drilldown.series = histogram_data;

    // Update the displayed chart if the user is viewing a histogram
    if (typeof chart.drilldownLevels != "undefined") {
        if (chart.drilldownLevels.length != 0) {
            var index;

            chart.setTitle({
                text: chart.options.drilldown.normalise ? chart.title.textStr.substring(0, chart.title.textStr.indexOf(' (normalised)')) : chart.title.textStr + ' (normalised)'
            }, false);

            chart.yAxis[0].update({
                title: {
                    text: chart.options.drilldown.normalise ? 'Number' : 'Normalised'
                },
                labels: {
                    format: chart.options.drilldown.normalise ? null : '{value:.2f}'
                },
                max: chart.options.drilldown.normalise ? null : 1.0
            }, false);

            for (i = 0; i < chart.series.length; i++) {

                // Find the index of histogram_data that contains the matching id of the current series
                index = histogram_data.map(function (element) {
                    return element.id;
                }).indexOf(chart.series[i].options.id);

                // Use the appropriate histogram_data to update the series y values
                for (j = 0; j < chart.series[i].data.length; j++) {
                    chart.series[i].data[j].update({
                        y: histogram_data[index].data[j][1]
                    }, false);
                }

                chart.redraw({duration: 1000});
            }
        }
    }

    chart.options.drilldown.normalise ? chart.options.drilldown.normalise = false : chart.options.drilldown.normalise = true;
}