/*global Highcharts*/
/*eslint no-undef: "error"*/

function chartAverageOverTime(renderDiv, valueLabel, valueUnits, avgLabel) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            renderTo: renderDiv,
            zoomType: "x"
        },
        plotOptions: {
            line: {
                turboThreshold: 5000 // Greater than the 1000 default to enable large data series to be plotted
            }
        },
        title: {
            text: ""
        },
        tooltip: {
            pointFormat: "{series.name}<br/>{point.y:.1f} " + valueUnits
        },
        xAxis: {
            categories: [1,2,3,4,5],
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: {
            title: {
                text: avgLabel + " " + valueLabel + (valueUnits !== "" ? " ("+ valueUnits +")" : ""),
                useHTML: true
            },
            floor: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: "#808080"
            }]        },
        legend: {
            layout: "vertical",
            align: "right",
            verticalAlign: "middle",
            borderWidth: 0,
            useHTML: true
        },
        series: []
    });
}