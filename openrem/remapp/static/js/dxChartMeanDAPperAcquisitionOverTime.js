$(function () {
var chartAcquisitionMeanDAPOverTime = new Highcharts.Chart({
        chart: {
            renderTo: 'AcquisitionMeanDAPOverTimeDIV',
            zoomType: 'x'
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}<br/>{point.y:.1f} cGy.cm<sup>2</sup>',
            useHTML: true
        },
        xAxis: {
            categories: dateAxis,
            labels: {
                rotation:90
            }
        },
        yAxis: {
            title: {
                text: 'Mean DAP (cGy.cm<sup>2</sup>)',
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
            borderWidth: 0
        },
        series: meanDAPOverTime
    });
});

