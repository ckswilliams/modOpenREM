// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending.
function seriesSort(chartContainer, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        var chartDataNew = [];
        for (var i = 0; i < chart.series[0].data.length; i++) {
            chartDataNew.push({
                name: chart.series[0].data[i].name,
                y: chart.series[0].data[i].y,
                x: chart.series[0].data[i].i,
                freq: chart.series[0].data[i].freq,
                drilldown: chart.series[0].data[i].drilldown,
                category: chart.series[0].data[i].name,
                tooltip: chart.series[0].data[i].tooltip,
                bins: chart.series[0].data[i].bins
            });
        }
        bubbleSort(chartDataNew, p, d);
        rebuildSeries(chartContainer, chartDataNew);
        chart.yAxis[0].isDirty = true;
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the index of the series to sort.
function twoSeriesSort(chartContainer, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        var series_index_to_sort, other_series_index;
        if (s==0) {
            series_index_to_sort = 0;
            other_series_index = 1;
        }
        else {
            series_index_to_sort = 1;
            other_series_index = 0;
        }
        var chartDataNew0 = [];
        for (var i = 0; i < chart.series[series_index_to_sort].data.length; i++) {
            chartDataNew0.push({
                name: chart.series[series_index_to_sort].data[i].name,
                y: chart.series[series_index_to_sort].data[i].y,
                x: chart.series[series_index_to_sort].data[i].i,
                freq: chart.series[series_index_to_sort].data[i].freq,
                drilldown: chart.series[series_index_to_sort].data[i].drilldown,
                category: chart.series[series_index_to_sort].data[i].name,
                tooltip: chart.series[series_index_to_sort].data[i].tooltip,
                bins: chart.series[series_index_to_sort].data[i].bins
            });
        }
        var chartDataNew1 = [];
        for (var i = 0; i < chart.series[other_series_index].data.length; i++) {
            chartDataNew1.push({
                name: chart.series[other_series_index].data[i].name,
                y: chart.series[other_series_index].data[i].y,
                x: chart.series[other_series_index].data[i].i,
                freq: chart.series[other_series_index].data[i].freq,
                drilldown: chart.series[other_series_index].data[i].drilldown,
                category: chart.series[other_series_index].data[i].name,
                tooltip: chart.series[other_series_index].data[i].tooltip,
                bins: chart.series[other_series_index].data[i].bins
            });
        }
        bubbleSort(chartDataNew0, p, d);
        rebuildTwoSeries(chartContainer, chartDataNew0, chartDataNew1, s);
        bubbleSort(chartDataNew1, 'x', 1);
        chart.yAxis[0].isDirty = true;
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the index of the series to sort.
function fourSeriesSort(chartContainer, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {

        var chartDataNew0 = [];
        for (var i = 0; i < chart.series[s[0]].data.length; i++) {
            chartDataNew0.push({
                name: chart.series[s[0]].data[i].name,
                y: chart.series[s[0]].data[i].y,
                x: chart.series[s[0]].data[i].i,
                freq: chart.series[s[0]].data[i].freq,
                drilldown: chart.series[s[0]].data[i].drilldown,
                category: chart.series[s[0]].data[i].name,
                tooltip: chart.series[s[0]].data[i].tooltip,
                bins: chart.series[s[0]].data[i].bins
            });
        }
        var chartDataNew1 = [];
        for (var i = 0; i < chart.series[s[1]].data.length; i++) {
            chartDataNew1.push({
                name: chart.series[s[1]].data[i].name,
                y: chart.series[s[1]].data[i].y,
                x: chart.series[s[1]].data[i].i,
                freq: chart.series[s[1]].data[i].freq,
                drilldown: chart.series[s[1]].data[i].drilldown,
                category: chart.series[s[1]].data[i].name,
                tooltip: chart.series[s[1]].data[i].tooltip,
                bins: chart.series[s[1]].data[i].bins
            });
        }
        var chartDataNew2 = [];
        for (var i = 0; i < chart.series[s[2]].data.length; i++) {
            chartDataNew2.push({
                name: chart.series[s[2]].data[i].name,
                y: chart.series[s[2]].data[i].y,
                x: chart.series[s[2]].data[i].i,
                freq: chart.series[s[2]].data[i].freq,
                drilldown: chart.series[s[2]].data[i].drilldown,
                category: chart.series[s[2]].data[i].name,
                tooltip: chart.series[s[2]].data[i].tooltip,
                bins: chart.series[s[2]].data[i].bins
            });
        }
        var chartDataNew3 = [];
        for (var i = 0; i < chart.series[s[3]].data.length; i++) {
            chartDataNew3.push({
                name: chart.series[s[3]].data[i].name,
                y: chart.series[s[3]].data[i].y,
                x: chart.series[s[3]].data[i].i,
                freq: chart.series[s[3]].data[i].freq,
                drilldown: chart.series[s[3]].data[i].drilldown,
                category: chart.series[s[3]].data[i].name,
                tooltip: chart.series[s[3]].data[i].tooltip,
                bins: chart.series[s[3]].data[i].bins
            });
        }

        bubbleSort(chartDataNew0, p, d);
        rebuildFourSeries(chartContainer, chartDataNew0, chartDataNew1, chartDataNew2, chartDataNew3, s);
        bubbleSort(chartDataNew1, 'x', 1);
        bubbleSort(chartDataNew2, 'x', 1);
        bubbleSort(chartDataNew3, 'x', 1);
        chart.yAxis[0].isDirty = true;
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart
function rebuildSeries(chartContainer, chartData) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    for (var i = 0; i < chartData.length; i++) {
        newCategories.push(chartData[i].name);
        chart.series[0].data[i].update({
            name: chartData[i].name,
            y: chartData[i].y,
            x: i,
            freq: chartData[i].freq,
            drilldown: chartData[i].drilldown,
            category: chartData[i].name,
            tooltip: chartData[i].tooltip,
            bins: chartData[i].bins
        }, false);
    }
    chart.xAxis[0].categories = newCategories;
}

// chartContainer is the div that holds the HighChart; s is the index of the series to sort.
function rebuildTwoSeries(chartContainer, chartData, chartData2, s) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var i = 0;
    var s2 = (s == 0 ? 1 : 0);

    for (i = 0; i < chartData.length; i++) {
        newCategories.push(chartData[i].name);
        chart.series[s].data[i].update({
            name: chartData[i].name,
            y: chartData[i].y,
            x: i,
            freq: chartData[i].freq,
            drilldown: chartData[i].drilldown,
            category: chartData[i].name,
            tooltip: chartData[i].tooltip,
            bins: chartData[i].bins
        }, false);
    }
    chart.xAxis[0].categories = newCategories;

    for (i = 0; i < chartData2.length; i++) {
        var found = false;

        var j = 0;
        while (found == false) {
            if (chartData2[i].name == chartData[j].name) {
                chart.series[s2].data[j].update({
                    index: j,
                    name: chartData2[i].name,
                    y: chartData2[i].y,
                    x: j,
                    freq: chartData2[i].freq,
                    drilldown: chartData2[i].drilldown,
                    category: chartData2[i].category,
                    tooltip: chartData2[i].tooltip,
                    bins: chartData2[i].bins
                }, false);
                found = true;
            }
            else {
                j++;
            }
        }
    }
}

// chartContainer is the div that holds the HighChart; s is the index of the series to sort.
function rebuildFourSeries(chartContainer, chartData, chartData2, chartData3, chartData4, s) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var i = 0;

    for (i = 0; i < chartData.length; i++) {
        newCategories.push(chartData[i].name);
        chart.series[s[0]].data[i].update({
            name: chartData[i].name,
            y: chartData[i].y,
            x: i,
            freq: chartData[i].freq,
            drilldown: chartData[i].drilldown,
            category: chartData[i].name,
            tooltip: chartData[i].tooltip,
            bins: chartData[i].bins
        }, false);
    }
    chart.xAxis[0].categories = newCategories;



    for (i = 0; i < chartData2.length; i++) {
        var found = false;
        var j = 0;
        while (found == false) {
            if (chartData2[i].name == chartData[j].name) {
                chart.series[s[1]].data[j].update({
                    index: j,
                    name: chartData2[i].name,
                    y: chartData2[i].y,
                    x: j,
                    freq: chartData2[i].freq,
                    drilldown: chartData2[i].drilldown,
                    category: chartData2[i].category,
                    tooltip: chartData2[i].tooltip,
                    bins: chartData2[i].bins
                }, false);
                found = true;
            }
            else {
                j++;
            }
        }

        var found = false;
        var j = 0;
        while (found == false) {
            if (chartData3[i].name == chartData[j].name) {
                chart.series[s[2]].data[j].update({
                    index: j,
                    name: chartData3[i].name,
                    y: chartData3[i].y,
                    x: j,
                    freq: chartData3[i].freq,
                    drilldown: chartData3[i].drilldown,
                    category: chartData3[i].category,
                    tooltip: chartData3[i].tooltip,
                    bins: chartData3[i].bins
                }, false);
                found = true;
            }
            else {
                j++;
            }
        }

        var found = false;
        var j = 0;
        while (found == false) {
            if (chartData4[i].name == chartData[j].name) {
                chart.series[s[3]].data[j].update({
                    index: j,
                    name: chartData4[i].name,
                    y: chartData4[i].y,
                    x: j,
                    freq: chartData4[i].freq,
                    drilldown: chartData4[i].drilldown,
                    category: chartData4[i].category,
                    tooltip: chartData4[i].tooltip,
                    bins: chartData4[i].bins
                }, false);
                found = true;
            }
            else {
                j++;
            }
        }
    }
}

// a is an array of objects; p is the property to sort on; d is the direction of sort: 1 for ascending, anything else
// for descending.
function bubbleSort(a, p, d) {
    var swapped;
    do {
        swapped = false;
        for (var i=0; i < a.length-1; i++) {
            if (d == 1) {
                if (a[i][p] > a[i + 1][p]) {
                    var temp = a[i];
                    a[i] = a[i + 1];
                    a[i + 1] = temp;
                    swapped = true;
                }
            }
            else {
                if (a[i][p] < a[i + 1][p]) {
                    var temp = a[i];
                    a[i] = a[i + 1];
                    a[i + 1] = temp;
                    swapped = true;
                }
            }
        }
    } while (swapped);
}