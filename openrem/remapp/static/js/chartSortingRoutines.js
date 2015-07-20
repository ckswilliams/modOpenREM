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
function fourSeriesSort(chartContainer, chartData, chartData2, chartData3, chartData4, p, d, s) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chartData, p, d);
        rebuildFourSeries(chartContainer, chartData, chartData2, chartData3, chartData4, s);
        bubbleSort(chartData2, 'x', 1);
        bubbleSort(chartData3, 'x', 1);
        bubbleSort(chartData4, 'x', 1);
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
function rebuildFourSeries(chartContainer, chartData, chartData2, chartData3, chartData4, s) {
    var chart = $(chartContainer).highcharts();
    var newCategories = [];
    var data = $.extend(true, [], chartData);
    var data2 = $.extend(true, [], chartData2);
    var data3 = $.extend(true, [], chartData3);
    var data4 = $.extend(true, [], chartData4);
    var point;
    var i = 0;

    for (i = 0; i < data.length; i++) {
        point = data[i];
        newCategories.push(point.name);
        chart.series[s[0]].data[i].update({
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



    for (i = 0; i < data.length; i++) {
        var found = false;
        var j = 0;
        while (found == false) {
            if (data2[i].name == data[j].name) {
                point = data2[i];
                chart.series[s[1]].data[i].update({
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

        var found = false;
        var j = 0;
        while (found == false) {
            if (data3[i].name == data[j].name) {
                point = data3[i];
                chart.series[s[2]].data[i].update({
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

        var found = false;
        var j = 0;
        while (found == false) {
            if (data4[i].name == data[j].name) {
                point = data4[i];
                chart.series[s[3]].data[i].update({
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