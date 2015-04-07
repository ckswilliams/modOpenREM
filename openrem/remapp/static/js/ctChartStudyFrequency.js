$(function () {

var chartStudyFreq = new Highcharts.Chart({
        chart: {
            renderTo: 'piechartStudyDIV',
            plotBackgroundColor: null,
            plotBorderWidth: 1,//null,
            plotShadow: false
        },
        title: {
            text: ''
        },
        tooltip: {
            pointFormat: '{point.percentage:.1f} %<br/>n={point.y}'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    useHTML: true,
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} % (n={point.y})',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Study frequency',
            point: {
                events: {
                    click: function(e) {
                        location.href = e.point.url;
                        e.preventDefault();
                    }
                }
            },
            data: studyPiechartData
        }]
    });
});

