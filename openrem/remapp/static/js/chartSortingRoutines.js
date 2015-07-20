// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending.
function seriesSort(chartContainer, chartData, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        //bubbleSort(chart.series[0].data, p, d);
        bubbleSort(chartData, p, d);
        rebuildSeries(chartContainer, chartData);
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the index of the series to sort.
function twoSeriesSort(chartContainer, chartData, chartData2, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chartData, p, d);
        rebuildTwoSeries(chartContainer, chartData, chartData2, s);
        bubbleSort(chartData2, 'x', 1);
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart; p is the property to sort on; d is the direction of sort: 1 for
// ascending, anything else for descending; s is the index of the series to sort.
function fourSeriesSort(chartContainer, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        if (s == 0) {
            s2 = 1; s3 = 2; s4 = 3;
        }
        else if (s == 1) {
            s2 = 0; s3 = 2; s4 = 3;
        }
        else if (s == 2) {
            s2 = 0; s3 = 1; s4 = 3;
        }
        else {
            s2 = 0; s3 = 1; s4 = 2;
        }
        bubbleSort(chart.series[s].data, p, d);
        rebuildFourSeries(chartContainer, s);
        bubbleSort(chart.series[s2].data, 'x', 1);
        bubbleSort(chart.series[s3].data, 'x', 1);
        bubbleSort(chart.series[s4].data, 'x', 1);
        chart.redraw({ duration: 1000 });
    }
}

// chartContainer is the div that holds the HighChart
function rebuildSeries(chartContainer, chartData) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var data = $.extend(true, [], chartData);
    var point;

    for (var i = 0; i < data.length; i++) {
        point = data[i];
        newCategories.push(point.name);
        chart.series[0].data[i].update({
            name: point.name,
            y: point.y,
            x: i,
            freq: point.freq,
            drilldown: point.drilldown,
            category: point.name,
            tooltip: point.tooltip
        }, false);
    }
    chart.xAxis[0].categories = newCategories;
}

// chartContainer is the div that holds the HighChart; s is the index of the series to sort.
function rebuildTwoSeries(chartContainer, chartData, chartData2, s) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var data = $.extend(true, [], chartData);
    var data2 = $.extend(true, [], chartData2);
    var point;
    var i = 0;

    var s2 = (s == 0 ? 1 : 0);

    for (i = 0; i < data.length; i++) {
        point = data[i];
        newCategories.push(point.name);
        chart.series[s].data[i].update({
            name: point.name,
            y: point.y,
            x: i,
            freq: point.freq,
            drilldown: point.drilldown,
            category: point.name,
            tooltip: point.tooltip
        }, false);
    }
    chart.xAxis[0].categories = newCategories;

    for (i = 0; i < data2.length; i++) {
        var found = false;

        var j = 0;
        while (found == false) {
            if (data2[i].name == data[j].name) {
                point = data2[i];
                chart.series[s2].data[i].update({
                    index: j,
                    name: point.name,
                    y: point.y,
                    x: j,
                    freq: point.freq,
                    drilldown: point.drilldown,
                    category: point.category,
                    tooltip: point.tooltip
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
function rebuildFourSeries(chartContainer, s) {
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
        newData.tooltip = chart.series[s].data[i].tooltip;
        newCategories.push(chart.series[s].data[i].name);
        chart.series[s].data[i].update(newData, false);
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
                newData.tooltip = chart.series[s2].data[i].tooltip;
                chart.series[s2].data[i].update(newData, false);
                found = true;
            }
            else {
                j++;
            }
        }

        var currentIndex = chart.series[s3].data[i].index;
        var found = false;
        var j = 0;
        while (found == false) {
            if (chart.series[s].data[j].index == currentIndex) {
                newData.index = i;
                newData.x = chart.series[s].data[j].x;
                newData.y = chart.series[s3].data[i].y;
                newData.category = chart.series[s3].data[i].category;
                newData.drilldown = chart.series[s3].data[i].drilldown;
                newData.name = chart.series[s3].data[i].name;
                newData.freq = chart.series[s3].data[i].freq;
                newData.tooltip = chart.series[s3].data[i].tooltip;
                chart.series[s3].data[i].update(newData, false);
                found = true;
            }
            else {
                j++;
            }
        }

        var currentIndex = chart.series[s4].data[i].index;
        var found = false;
        var j = 0;
        while (found == false) {
            if (chart.series[s].data[j].index == currentIndex) {
                newData.index = i;
                newData.x = chart.series[s].data[j].x;
                newData.y = chart.series[s4].data[i].y;
                newData.category = chart.series[s4].data[i].category;
                newData.drilldown = chart.series[s4].data[i].drilldown;
                newData.name = chart.series[s4].data[i].name;
                newData.freq = chart.series[s4].data[i].freq;
                newData.tooltip = chart.series[s4].data[i].tooltip;
                chart.series[s4].data[i].update(newData, false);
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