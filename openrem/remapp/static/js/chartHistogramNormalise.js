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

    chart.options.drilldown.normalise ? chart.options.drilldown.normalise = false : chart.options.drilldown.normalise = true;
}