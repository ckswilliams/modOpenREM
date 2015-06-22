$(function () {
var chartStudyMeanDLPOverTime = new Highcharts.Chart({
        chart: {
            renderTo: 'studyMeanDLPOverTimeDIV',
            zoomType: 'x'
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{series.name}<br/>{point.y:.0f} mGy.cm'
        },
        xAxis: {
            categories: dateAxis,
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: {
            title: {
                text: 'Mean DLP (mGy.cm)'
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
        series: meanDLPOverTime
    });
});

