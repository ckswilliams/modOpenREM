// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending.
function seriesSort(chartContainer, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chart.series[0].data, p, d);
        rebuildSeries(chartContainer);
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the index of the series to sort.
function twoSeriesSort(chartContainer, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        var s2 = (s == 0 ? 1 : 0);
        bubbleSort(chart.series[s].data, p, d);
        rebuildTwoSeries(chartContainer, s);
        bubbleSort(chart.series[s2].data, 'x', 1);
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart
function rebuildSeries(chartContainer) {
    var chart = $(chartContainer).highcharts();
    var newData = {};
    var newCategories = [];

    for (var i = 0; i < chart.series[0].data.length; i++) {
        newData.x = i;
        newData.y = chart.series[0].data[i].y;
        newData.category = chart.series[0].data[i].category;
        newData.drilldown = chart.series[0].data[i].drilldown;
        newData.name = chart.series[0].data[i].name;
        newData.freq = chart.series[0].data[i].freq;
        newCategories.push(chart.series[0].data[i].category);
        chart.series[0].data[i].update(newData, false);
    }
    chart.xAxis[0].categories = newCategories;
}

// chartContainer is the div that holds the HighChart; s is the index of the series to sort.
function rebuildTwoSeries(chartContainer, s) {
    var s2 = (s == 0 ? 1 : 0);
    var chart = $(chartContainer).highcharts();
    var newData = {};
    var newCategories = [];
    var i = 0;

    for (i = 0; i < chart.series[s].data.length; i++) {
        newData.index = chart.series[s].data[i].index;
        newData.x = i;
        newData.y = chart.series[s].data[i].y;
        newData.category = chart.series[s].data[i].category;
        newData.drilldown = chart.series[s].data[i].drilldown;
        newData.name = chart.series[s].data[i].name;
        newData.freq = chart.series[s].data[i].freq;
        chart.series[s].data[i].update(newData, false);
        newCategories.push(chart.series[s].data[i].category);
    }
    chart.xAxis[0].categories = newCategories;

    for (i = 0; i < chart.series[s2].data.length; i++) {
        var currentIndex = chart.series[s2].data[i].index;
        var found = false;

        var j = 0;
        while (found == false) {
            if (chart.series[s].data[j].index == currentIndex) {
                newData.index = i;
                newData.x = chart.series[s].data[j].x;
                newData.y = chart.series[s2].data[i].y;
                newData.category = chart.series[s2].data[i].category;
                newData.drilldown = chart.series[s2].data[i].drilldown;
                newData.name = chart.series[s2].data[i].name;
                newData.freq = chart.series[s2].data[i].freq;
                chart.series[s2].data[i].update(newData, false);
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