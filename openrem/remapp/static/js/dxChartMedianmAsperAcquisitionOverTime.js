$(function () {
    var chartAcquisitionMedianmAsOverTime = new Highcharts.Chart({
        chart: {
            renderTo: 'AcquisitionMeanmAsOverTimeDIV',
            zoomType: 'x'
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}<br/>{point.y:.1f} mAs',
            useHTML: true
        },
        xAxis: {
            categories: [1,2,3,4,5],
            labels: {
                rotation:90
            }
        },
        yAxis: {
            title: {
                text: 'Median mAs',
                useHTML: true
            },
            floor: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0,
            useHTML: true
        },
        series: []
    });
});