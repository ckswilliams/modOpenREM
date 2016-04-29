function chartScatter(default_title, render_div, x_axis_title, y_axis_title) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            zoomType: 'xy',
            type: 'column',
            renderTo: render_div,
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
            }
        },
        series: [{
            type: 'scatter',
            name: 'All systems',
            color: 'rgba(152,0,67,0.1)',
            data: [],
            marker: {
                radius: 1
            },
            tooltip: {
                followPointer: false,
                pointFormat: '[{point.x:.1f}, {point.y:.1f}]'
            }
        }]
    });
}