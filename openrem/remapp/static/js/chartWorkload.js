function chartWorkload(render_div, category_type) {
    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            renderTo: render_div,
            plotBackgroundColor: null,
            plotShadow: false,
            events: {
                drilldown: function(e) {
                    this.viewData(false, false, true);
                    this.setTitle({ text: category_type + ' per hour,<br>'+e.point.name, align:'left', verticalAlign:'top', y:50, x:50 });
                },
                drillup: function() {
                    this.viewData(false, false, true);
                    this.setTitle({ text: category_type + ' per<br>day of the week', align:'center', verticalAlign:'middle', y:70, x:0 });
                }
            }
        },
        title: {
            text: category_type + ' per<br>day of the week',
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
            name: category_type + ' per weekday',
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
}