$(function () {
    var chartStudyWorkload = new Highcharts.Chart({
        chart: {
            renderTo: 'piechartStudyWorkloadDIV',
            plotBackgroundColor: null,
            plotShadow: false,
            events: {
                drilldown: function(e) {
                    chartStudyWorkload.setTitle({ text: 'Studies per hour,<br>'+e.point.name, align:'left', verticalAlign:'top', y:50, x:50 });
                },
                drillup: function(e) {
                    chartStudyWorkload.setTitle({ text: 'Studies per<br>day of the week', align:'center', verticalAlign:'middle', y:70, x:0 });
                }
            }
        },
        title: {
            text: 'Studies per<br>day of the week',
            align: 'center',
            verticalAlign: 'middle',
            y: 70
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
            startAngle:-90,
            endAngle:90,
            center: ['50%','75%'],
            innerSize: '50%',
            data: []
        }],
        drilldown: {
            series:[]
        }
    });
});