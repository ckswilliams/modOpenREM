$(function () {

var chartAcqFrequency = new Highcharts.Chart({
        chart: {
            renderTo: 'piechartProtocolDIV',
            plotBackgroundColor: null,
            plotBorderWidth: 1,
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
                allowPointSelect: false,
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
            data: protocolPiechartData
        }]
    });
});

