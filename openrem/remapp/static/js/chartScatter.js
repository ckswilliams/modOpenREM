function chartScatter(default_title, render_div, x_axis_title, y_axis_title) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            zoomType: 'xy',
            type: 'column',
            renderTo: render_div
        },
        title: {
            useHTML: true,
            text: default_title
        },
        legend: {
            enabled: true
        },
        xAxis: {
            min: 0,
            max: 100,
            gridLineWidth: 1,
            title: {
                useHTML: true,
                text: x_axis_title
            }
        },
        yAxis: {
            min: 0,
            max: 100,
            minPadding: 0,
            maxPadding: 0,
            title: {
                useHTML: true,
                text: y_axis_title
            },
            labels: {
                format: '{value:.1f}'
            }

        },
        series: []
    });
}