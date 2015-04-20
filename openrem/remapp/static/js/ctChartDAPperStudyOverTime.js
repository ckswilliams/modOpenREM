$(function () {
var chartWeeklyStudyMeanDLP = new Highcharts.Chart({
        chart: {
            renderTo: 'linechartWeeklyStudyMeanDIV',
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
            minTickInterval: 4,
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: {
            title: {
                text: 'Mean DLP over the week (mGy.cm)'
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
        series: meanDLPperWeek
    });
});

