/*global Highcharts*/
/*eslint no-undef: "error"*/
/*eslint object-shorthand: "off" */

function chartFrequency(renderDiv, seriesName) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            renderTo: renderDiv,
            plotBackgroundColor: null,
            plotShadow: false
        },
        title: {
            text: ""
        },
        tooltip: {
            pointFormat: "{point.percentage:.1f} %<br/>n={point.y}"
        },
        plotOptions: {
            pie: {
                allowPointSelect: false,
                cursor: "pointer",
                dataLabels: {
                    useHTML: true,
                    enabled: true,
                    format: "<b>{point.name}</b>: {point.percentage:.1f} % (n={point.y})",
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || "black"
                    }
                },
                turboThreshold: 5000 // Greater than the 1000 default to enable large data series to be plotted
            }
        },
        series: [{
            type: "pie",
            name: seriesName,
            point: {
                events: {
                    click: function(e) {
                        location.href = e.point.url;
                        e.preventDefault();
                    }
                }
            },
            data: []
        }]
    });
}