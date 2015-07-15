function seriesSort(chartContainer, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chart.series[0].data, p, d);
        rebuildSeries(chartContainer);
    }
}

function twoSeriesSort(chartContainer, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chart.series[0].data, p, d);
        rebuildTwoSeries(chartContainer);
        bubbleSort(chart.series[1].data, 'x', 1);
        chart.redraw({ duration: 1000 });
    }
}

function twoSeriesSortB(chartContainer, p, d) {
    var chart = $(chartContainer).highcharts();
    if(typeof chart.series[0].chart.drilldownLevels == "undefined" || typeof chart.series[0].chart.series[0].drilldownLevel == "Object" || chart.series[0].chart.drilldownLevels.length == 0) {
        bubbleSort(chart.series[1].data, p, d);
        rebuildTwoSeriesB(chartContainer);
        bubbleSort(chart.series[0].data, 'x', 1);
        chart.redraw({ duration: 1000 });
    }
}

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
        newCategories.push(chart.series[0].data[i].name);
        chart.series[0].data[i].update(newData, false);
    }
    chart.xAxis[0].categories = newCategories;
    chart.redraw({ duration: 1000 });
}

function rebuildTwoSeries(chartContainer) {
    var chart = $(chartContainer).highcharts();
    var newData = {};
    var newCategories = [];
    var i = 0;

    for (i = 0; i < chart.series[0].data.length; i++) {
        newData.index = chart.series[0].data[i].index;
        newData.x = i;
        newData.y = chart.series[0].data[i].y;
        newData.category = chart.series[0].data[i].category;
        newData.drilldown = chart.series[0].data[i].drilldown;
        newData.name = chart.series[0].data[i].name;
        newData.freq = chart.series[0].data[i].freq;
        chart.series[0].data[i].update(newData, false);
        newCategories.push(chart.series[0].data[i].name);
    }
    chart.xAxis[0].categories = newCategories;

    for (i = 0; i < chart.series[1].data.length; i++) {
        var currentIndex = chart.series[1].data[i].index;
        var found = false;

        var j = 0;
        while (found == false) {
            if (chart.series[0].data[j].index == currentIndex) {
                newData.index = i;
                newData.x = chart.series[0].data[j].x;
                newData.y = chart.series[1].data[i].y;
                newData.category = chart.series[1].data[i].category;
                newData.drilldown = chart.series[1].data[i].drilldown;
                newData.name = chart.series[1].data[i].name;
                newData.freq = chart.series[1].data[i].freq;
                chart.series[1].data[i].update(newData, false);
                found = true;
            }
            else {
                j++;
            }
        }
    }
}

function rebuildTwoSeriesB(chartContainer) {
    var chart = $(chartContainer).highcharts();
    var newData = {};
    var newCategories = [];
    var i = 0;

    for (i = 0; i < chart.series[1].data.length; i++) {
        newData.index = chart.series[1].data[i].index;
        newData.x = i;
        newData.y = chart.series[1].data[i].y;
        newData.category = chart.series[1].data[i].category;
        newData.drilldown = chart.series[1].data[i].drilldown;
        newData.name = chart.series[1].data[i].name;
        newData.freq = chart.series[1].data[i].freq;
        chart.series[1].data[i].update(newData, false);
        newCategories.push(chart.series[1].data[i].name);
    }
    chart.xAxis[0].categories = newCategories;

    for (i = 0; i < chart.series[0].data.length; i++) {
        var currentIndex = chart.series[0].data[i].index;
        var found = false;

        var j = 0;
        while (found == false) {
            if (chart.series[1].data[j].index == currentIndex) {
                newData.index = i;
                newData.x = chart.series[1].data[j].x;
                newData.y = chart.series[0].data[i].y;
                newData.category = chart.series[0].data[i].category;
                newData.drilldown = chart.series[0].data[i].drilldown;
                newData.name = chart.series[0].data[i].name;
                newData.freq = chart.series[0].data[i].freq;
                chart.series[0].data[i].update(newData, false);
                found = true;
            }
            else {
                j++;
            }
        }
    }
}

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