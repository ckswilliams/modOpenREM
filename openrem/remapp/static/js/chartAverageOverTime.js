function chartAverageOverTime(render_div, value_label, value_units, avg_label) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            renderTo: render_div,
            zoomType: 'x'
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}<br/>{point.y:.1f} ' + value_units
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
                text: avg_label + ' ' + value_label + (value_units != '' ? ' ('+ value_units +')' : ''),
                useHTML: true
            },
            floor: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0,
            useHTML: true
        },
        series: []
    });
}