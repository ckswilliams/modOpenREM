/*global anySeriesSort, formatDate, sortByName, sortByY*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */
/*eslint object-shorthand: "off" */

/**
 * Function to replace missing category names with the word "Blank"
 * @param names -  an array of category names
 */
function replaceBlankNames(names) {
    var listOfBlankIndicators = ["", null];
    var i, j;
    for (i = 0; i < listOfBlankIndicators.length; i++) {
        for (j = 0; j < names.length; j++) {
            if (names[j] === listOfBlankIndicators[i]) {
                names[j] = "Blank";
            }
        }
    }
    return names;
}


function sortChartDataToDefault(sortingField, sortingDirection, chartDiv) {
    switch(sortingField) {
        case "freq":
            anySeriesSort("#"+chartDiv, "totalCounts", sortingDirection, 0);
            break;
        case "dlp":
            anySeriesSort("#"+chartDiv, "avgValue", sortingDirection, 0);
            break;
        case "ctdi":
            anySeriesSort("#"+chartDiv, "avgValue", sortingDirection, 0);
            break;
        case "dap":
            anySeriesSort("#"+chartDiv, "avgValue", sortingDirection, 0);
            break;
        case "name":
            anySeriesSort("#"+chartDiv, "name", sortingDirection, 0);
            break;
        default:
            anySeriesSort("#"+chartDiv, "name", 1, 0);
    }
}


function updateWorkloadChart(workloadData, chartDiv, colourScale) {
    var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var dayTotal = 0;
    var weekTotal = 0;
    var workloadSeriesData = [];
    var drilldownSeriesData = [];
    var tempTime, i, j, temp;
    for (i = 0; i < 7; i++) {
        dayTotal = 0;
        temp = [];
        for (j = 0; j < 24; j++) {
            dayTotal += workloadData[i][j];
            weekTotal += workloadData[i][j];
            tempTime = "0" + j;
            tempTime = tempTime.substr(tempTime.length-2);
            temp.push({name: tempTime + ":00", y: workloadData[i][j], color: colourScale(j/(23)).hex()});
        }
        workloadSeriesData.push({
            name: dayNames[i],
            y: dayTotal,
            color: colourScale(i/(6)).hex(),
            drilldown: dayNames[i]
        });
        drilldownSeriesData.push({
            id: dayNames[i],
            name: dayNames[i],
            useHTML: true,
            type: "pie",
            data: temp
        });
    }

    var chart = $("#"+chartDiv).highcharts();
    chart.title.textStr = chart.title.textStr + "<br>(n = " + weekTotal + ")";
    chart.options.chart.mainTitleText = chart.title.textStr;
    chart.options.drilldown.series = drilldownSeriesData;
    chart.series[0].setData(workloadSeriesData);
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();
    chart.redraw({duration: 1000});
}


function updateOverTimeChart(nameList, overTimeData, seriesColours, urlStart, chartDiv) {
    var dateAxis, currentValue, tempDate, dateAfter, dateBefore, temp, i, j;
    var chart = $("#"+chartDiv).highcharts();

    // Replace all items in nameList that match an item in blankIndicators with "Blank"
    nameList = replaceBlankNames(nameList);

    dateAxis = [];
    for (i = 0; i < overTimeData[0].length; i++) {
        tempDate = new Date(Date.parse(overTimeData[0][i][0]));
        tempDate = formatDate(tempDate);
        dateAxis.push(tempDate);
    }
    chart.xAxis[0].setCategories(dateAxis);

    for (i = 0; i < overTimeData.length; i++) {
        temp = [];
        for (j = 0; j < overTimeData[0].length; j++) {
            tempDate = new Date(Date.parse(overTimeData[i][j][0]));
            dateAfter = formatDate(tempDate);
            dateBefore = formatDate(new Date((new Date((tempDate).setMonth((tempDate).getMonth() + 1))).setDate((new Date((tempDate).setMonth((tempDate).getMonth() + 1))).getDate() - 1)));

            currentValue = parseFloat(overTimeData[i][j][1]);
            if (currentValue === 0 || isNaN(currentValue)) {currentValue = null;}

            temp.push({
                y: currentValue,
                url: encodeURI(urlStart + nameList[i] + "&date_after=" + dateAfter + "&date_before=" + dateBefore)
            });
        }

        chart.addSeries({
            name: nameList[i],
            color: seriesColours[i],
            marker: {enabled: true},
            point: {
                events: {
                    click: function (e) {
                        location.href = e.point.url;
                        e.preventDefault();
                    }
                }
            },
            data: temp
        });
    }

    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();
    chart.redraw({duration: 1000});
}


function updateFrequencyChart(nameList, systemList, summaryData, urlStart, chartDiv, colourScale) {
    var piechartData = new Array(nameList.length);
    var dataCounts = 0;
    var i, j;

    // Replace all items in nameList that match an item in blankIndicators with "Blank"
    nameList = replaceBlankNames(nameList);

    for (i = 0; i < nameList.length; i++) {
        dataCounts = 0;
        for (j = 0; j < systemList.length; j++) {
            dataCounts += parseInt(summaryData[j][i].num);
        }
        piechartData[i] = {
            name: nameList[i],
            y: dataCounts,
            url: encodeURI(urlStart + nameList[i])
        };
    }

    piechartData.sort(sortByName);
    piechartData.sort(sortByY);

    var colourMax = nameList.length === 1 ? nameList.length : nameList.length - 1;

    for (i = 0; i < nameList.length; i++) {
        piechartData[i].color = colourScale(i / colourMax).hex();
    }

    var chart = $("#"+chartDiv).highcharts();
    chart.series[0].setData(piechartData);
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();

    chart.redraw({duration: 1000});
}


function updateAverageChart(nameList, systemList, summaryData, histogramData, averageChoice, chartDiv, colourScale) {
    var dataCounts = []; while(dataCounts.push([]) < systemList.length);
    var dataBins = []; while(dataBins.push([]) < systemList.length);
    var totalCountsPerName = [];
    var currentCounts;
    var averageValuePerName = [];
    var currentValue;
    var calcHistograms = typeof histogramData !== "undefined";
    var i, j, k;

    // Replace all items in nameList that match an item in blankIndicators with "Blank"
    nameList = replaceBlankNames(nameList);

    // Calculate counts per name and average value per name. These are used to sort the chart series by.
    if(calcHistograms) {
        for (j = 0; j < nameList.length; j++) {
            currentCounts = 0;
            currentValue = 0;
            for (i = 0; i < systemList.length; i++) {
                (dataCounts[i]).push(histogramData[i][j][0]);
                (dataBins[i]).push(histogramData[i][j][1]);
                if (summaryData[i][j].num === null) {summaryData[i][j].num = 0;}
                currentCounts += parseFloat(summaryData[i][j].num);
                if (averageChoice === "mean") {
                    if (summaryData[i][j].mean === null) {summaryData[i][j].mean = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].mean);
                }
                else if (averageChoice === "median") {
                    if (summaryData[i][j].median === null) {summaryData[i][j].median = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].median);
                }
                else {
                    if (summaryData[i][j].mean === null) {summaryData[i][j].mean = 0;}
                    if (summaryData[i][j].median === null) {summaryData[i][j].median = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].mean);
                }
            }
            totalCountsPerName.push(currentCounts);
            averageValuePerName.push(currentValue / currentCounts);
        }
    }
    else {
        for (j = 0; j < nameList.length; j++) {
            currentCounts = 0;
            currentValue = 0;
            for (i = 0; i < systemList.length; i++) {
                if (summaryData[i][j].num === null) {summaryData[i][j].num = 0;}
                currentCounts += parseFloat(summaryData[i][j].num);
                if (averageChoice === "mean") {
                    if (summaryData[i][j].mean === null) {summaryData[i][j].mean = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].mean);
                }
                else if (averageChoice === "median") {
                    if (summaryData[i][j].median === null) {summaryData[i][j].median = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].median);
                }
                else {
                    if (summaryData[i][j].mean === null) {summaryData[i][j].mean = 0;}
                    if (summaryData[i][j].median === null) {summaryData[i][j].median = 0;}
                    currentValue += parseFloat(summaryData[i][j].num) * parseFloat(summaryData[i][j].mean);
                }
            }
            totalCountsPerName.push(currentCounts);
            averageValuePerName.push(currentValue / currentCounts);
        }
    }

    if (averageChoice === "mean" || averageChoice === "both") {
        var meanData = []; while(meanData.push([]) < systemList.length);
        for (i = 0; i < systemList.length; i++) {
            for (j = 0; j < nameList.length; j++) {
                (meanData[i]).push({
                    name: nameList[j],
                    y: parseFloat(summaryData[i][j].mean),
                    freq: summaryData[i][j].num,
                    bins: dataBins[i][j],
                    tooltip: systemList[i] + "<br>" + nameList[j] + "<br>" + parseFloat(summaryData[i][j].mean).toFixed(1) + " mean<br>(n=" + summaryData[i][j].num + ")",
                    drilldown: calcHistograms ? systemList[i]+nameList[j] : null,
                    totalCounts: totalCountsPerName[j],
                    avgValue: averageValuePerName[j]
                });
            }
        }
    }

    if (averageChoice === "median" || averageChoice === "both") {
        var medianData = []; while(medianData.push([]) < systemList.length);
        for (i = 0; i < systemList.length; i++) {
            for (j = 0; j < nameList.length; j++) {
                (medianData[i]).push({
                    name: nameList[j],
                    y: parseFloat(summaryData[i][j].median),
                    freq: summaryData[i][j].num,
                    bins: dataBins[i][j],
                    tooltip: systemList[i] + "<br>" + nameList[j] + "<br>" + parseFloat(summaryData[i][j].median).toFixed(1) + " median<br>(n=" + summaryData[i][j].num + ")",
                    drilldown: calcHistograms ? systemList[i]+nameList[j] : null,
                    totalCounts: totalCountsPerName[j],
                    avgValue: averageValuePerName[j]
                });
            }
        }
    }

    if (calcHistograms) {
        var temp;
        var drilldownSeries = [];
        for (i = 0; i < systemList.length; i++) {
            for (j = 0; j < nameList.length; j++) {
                temp = [];
                for (k = 0; k < dataCounts[i][0].length; k++) {
                    temp.push([dataBins[i][j][k].toFixed(1).toString() + " \u2264 x < " + dataBins[i][j][k + 1].toFixed(1).toString(), dataCounts[i][j][k]]);
                }
                drilldownSeries.push({
                    id: systemList[i] + nameList[j],
                    name: systemList[i],
                    useHTML: true,
                    data: temp
                });
            }
        }
    }

    var chart = $("#"+chartDiv).highcharts();
    chart.xAxis[0].update({
        categories: nameList,
        min: 0,
        max: nameList.length - 1
    }, false);
    if (calcHistograms) {chart.options.drilldown.series = drilldownSeries;}
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();

    var colourMax;
    if (averageChoice === "mean") {
        colourMax = systemList.length === 1 ? systemList.length : systemList.length - 1;
        for (i = 0; i < systemList.length; i++) {
            if (chart.series.length > i) {
                chart.series[i].update({
                    name: systemList[i],
                    data: meanData[i],
                    color: colourScale(i/colourMax).hex()
                });
            }
            else {
                chart.addSeries({
                    name: systemList[i],
                    data: meanData[i],
                    color: colourScale(i/colourMax).hex()
                });
            }
        }
    }
    else if (averageChoice === "median") {
        colourMax = systemList.length === 1 ? systemList.length : systemList.length - 1;
        for (i = 0; i < systemList.length; i++) {
            if (chart.series.length > i) {
                chart.series[i].update({
                    name: systemList[i],
                    data: medianData[i],
                    color: colourScale(i/colourMax).hex()
                });
            }
            else {
                chart.addSeries({
                    name: systemList[i],
                    data: medianData[i],
                    color: colourScale(i/colourMax).hex()
                });
            }
        }
    }
    else {
        colourMax = systemList.length;
        var currentSeries = 0;
        for (i = 0; i < (systemList.length)*2; i+=2) {
            if (chart.series.length > i+1) {
                chart.series[i].update({
                    name: systemList[currentSeries] + " (mean)",
                    data: meanData[currentSeries],
                    color: colourScale(i/(colourMax*2-1)).hex()
                });
                chart.series[i+1].update({
                    name: systemList[currentSeries] + " (median)",
                    data: medianData[currentSeries],
                    color: colourScale((i+1)/(colourMax*2-1)).hex()
                });
            }
            else {
                chart.addSeries({
                    name: systemList[currentSeries] + " (mean)",
                    data: meanData[currentSeries],
                    color: colourScale(i/(colourMax*2-1)).hex()
                });
                chart.addSeries({
                    name: systemList[currentSeries] + " (median)",
                    data: medianData[currentSeries],
                    color: colourScale((i+1)/(colourMax*2-1)).hex()
                });
            }
            currentSeries++;
        }
    }
    chart.redraw({duration: 1000});
}


/**
 * Function to update the data of an OpenREM HighCharts scatter plot
 * @param scatterData - an array[i][j][2] of x-y data pairs; i is a series with j pairs of data
 * @param maxValues - an array[2] containing the maximum x and y values in scatterData
 * @param chartDiv - the HTML DIV that contains the HighChart
 * @param systemList - an array[i] of series names
 * @param xAxisUnit - the x-axis units to use for the tooltip
 * @param yAxisUnit - the y-axis units to use for the tooltip
 * @param tooltipDp -  an array[2] containing the number of decimal places to use for the x and y data in the tooltip
 * @param colourScale - the chroma.js colour scale to use
 */
function updateScatterChart(scatterData, maxValues, chartDiv, systemList, xAxisUnit, yAxisUnit, tooltipDp, colourScale) {
    var chart = $("#"+chartDiv).highcharts();
    var colourMax = systemList.length;
    var i;
    var tooltipPointFormat;

    tooltipPointFormat = "{point.x:." + tooltipDp[0] + "f} " + xAxisUnit + "<br>{point.y:." + tooltipDp[1] + "f} " + yAxisUnit;
    for (i = 0; i < systemList.length; i++) {
        if (chart.series.length > i) {
            chart.series[i].update({
                type: "scatter",
                name: systemList[i],
                data: scatterData[i],
                color: colourScale(i/colourMax).alpha(0.5).css(),
                marker: {
                    radius: 2
                },
                tooltip: {
                    followPointer: false,
                    pointFormat: tooltipPointFormat
                }
            });
        }
        else {
            chart.addSeries({
                type: "scatter",
                name: systemList[i],
                data: scatterData[i],
                color: colourScale(i/colourMax).alpha(0.5).css(),
                marker: {
                    radius: 2
                },
                tooltip: {
                    followPointer: false,
                    pointFormat: tooltipPointFormat
                }
            });
        }

    }

    chart.xAxis[0].update({
        max: maxValues[0]
    });
    chart.yAxis[0].update({
        max: maxValues[1]
    });
    chart.redraw({duration: 1000});
}
