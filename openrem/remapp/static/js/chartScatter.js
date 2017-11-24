/*global Highcharts*/
/*eslint no-undef: "error"*/

function chartScatter(defaultTitle, renderDiv, xAxisTitle, yAxisTitle) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            zoomType: "xy",
            type: "column",
            renderTo: renderDiv
        },
        title: {
            useHTML: true,
            text: defaultTitle
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            series: {
                boostThreshold: 1
            }
        },
        boost: {
            seriesThreshold: 2,
            useGPUTranslations: true,
            usePreAllocated: true
        },
        xAxis: {
            min: 0,
            max: 100,
            gridLineWidth: 1,
            title: {
                useHTML: true,
                text: xAxisTitle
            }
        },
        yAxis: {
            min: 0,
            max: 100,
            minPadding: 0,
            maxPadding: 0,
            title: {
                useHTML: true,
                text: yAxisTitle
            },
            labels: {
                format: "{value:.1f}"
            }

        },
        series: []
    });
}