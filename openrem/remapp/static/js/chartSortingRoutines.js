// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the series index to sort: the rest are then sorted to match.
function anySeriesSort(chartContainer, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(chart.series.length != 0) {
        if (typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {

            // Create an array to hold each series
            var chartDataNew = [];
            for (var i = 0; i < chart.series.length; i++) {
                chartDataNew.push([]);

                for (var j = 0; j < chart.series[0].data.length; j++) {
                    chartDataNew[i].push({
                        name: chart.series[i].data[j].name,
                        y: chart.series[i].data[j].y,
                        x: chart.series[i].data[j].j,
                        freq: chart.series[i].data[j].freq,
                        drilldown: chart.series[i].data[j].drilldown,
                        category: chart.series[i].data[j].name,
                        tooltip: chart.series[i].data[j].tooltip,
                        bins: chart.series[i].data[j].bins,
                        total_counts: chart.series[i].data[j].total_counts,
                        avg_value: chart.series[i].data[j].avg_value
                    });
                }
            }

            bubbleSort(chartDataNew[0], p, d);
            rebuildAnySeries(chartContainer, chartDataNew, s);
            for (i = 1; i < chart.series.length; i++) {
                bubbleSort(chartDataNew[i], 'x', 1);
            }
            chart.xAxis[0].isDirty = true;
            chart.yAxis[0].isDirty = true;
            chart.redraw({duration: 1000});
        }
    }
}


// chartContainer is the div that holds the HighChart; s is the index of the series to sort.
function rebuildAnySeries(chartContainer, chartData, s) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var i, j, k;

    for (i = 0; i < chartData[0].length; i++) {
        newCategories.push(chartData[0][i].name);
        chart.series[s].data[i].update({
            name: chartData[0][i].name,
            y: chartData[0][i].y,
            x: i,
            freq: chartData[0][i].freq,
            drilldown: chartData[0][i].drilldown,
            category: chartData[0][i].name,
            tooltip: chartData[0][i].tooltip,
            bins: chartData[0][i].bins,
            total_counts: chartData[0][i].total_counts,
            avg_value: chartData[0][i].avg_value
        }, false);
    }
    chart.xAxis[0].categories = newCategories;
    chart.xAxis[0].options.categories = newCategories;
    chart.xAxis[0].userOptions.categories = newCategories;
    chart.options.xAxis[0].categories = newCategories;
    chart.userOptions.xAxis.categories = newCategories;


    for (i = 0; i < chartData[0].length; i++) {
        for (k = 0; k < chartData.length; k++) {
            if (k != s) {
                var found = false;
                j = 0;
                while (found == false) {
                    if (chartData[k][i].name == chartData[0][j].name) {
                        chart.series[k].data[j].update({
                            index: j,
                            name: chartData[k][i].name,
                            y: chartData[k][i].y,
                            x: j,
                            freq: chartData[k][i].freq,
                            drilldown: chartData[k][i].drilldown,
                            category: chartData[k][i].category,
                            tooltip: chartData[k][i].tooltip,
                            bins: chartData[k][i].bins,
                            total_counts: chartData[k][i].total_counts,
                            avg_value: chartData[k][i].avg_value
                        }, false);
                        found = true;
                    }
                    else {
                        j++;
                    }
                }
            }
        }
    }
}


// a is an array of objects; p is the property to sort on; d is the direction of sort: 1 for ascending, anything else
// for descending.
function bubbleSort(a, p, d) {
    var swapped, temp;
    do {
        swapped = false;
        for (var i=0; i < a.length-1; i++) {
            if (d == 1) {
                if (a[i][p] > a[i + 1][p]) {
                    temp = a[i];
                    a[i] = a[i + 1];
                    a[i + 1] = temp;
                    swapped = true;
                }
            }
            else {
                if (a[i][p] < a[i + 1][p]) {
                    temp = a[i];
                    a[i] = a[i + 1];
                    a[i + 1] = temp;
                    swapped = true;
                }
            }
        }
    } while (swapped);
}