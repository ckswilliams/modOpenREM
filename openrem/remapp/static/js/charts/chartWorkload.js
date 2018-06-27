/*global Highcharts*/
/*eslint no-undef: "error"*/
/*eslint object-shorthand: "off" */

function chartWorkload(renderDiv, categoryType) {

    var chart = new Highcharts.Chart({
        exporting: {
            fallbackToExportServer: false
        },
        chart: {
            renderTo: renderDiv,
            mainTitleText: categoryType + " per<br>day of the week",
            plotBackgroundColor: null,
            plotShadow: false,
            events: {
                drilldown: function(e) {
                    this.viewData(false, false, true);
                    this.setTitle({ text: categoryType + " per hour,<br>"+e.point.name+" (n="+e.point.y+")", align:"left", verticalAlign:"top", y:50, x:50 });
                },
                drillup: function() {
                    this.viewData(false, false, true);
                    this.setTitle({ text: this.options.chart.mainTitleText, align:"center", verticalAlign:"middle", y:40, x:0 });
                }
            }
        },
        title: {
            text: categoryType + " per<br>day of the week",
            align: "center",
            verticalAlign: "middle",
            y: 40
        },
        tooltip: {
            pointFormat: "{point.percentage:.1f} %<br/>n={point.y}"
        },
        plotOptions: {
            pie: {
                allowPointSelect: false,
                cursor: "pointer",
                dataLabels: {
                    useHTML: true,
                    enabled: true,
                    format: "<b>{point.name}</b>: {point.percentage:.1f} % (n={point.y})",
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || "black"
                    }
                }
            }
        },
        series: [{
            type: "pie",
            name: categoryType + " per weekday",
            startAngle:-90,
            endAngle:90,
            center: ["50%","75%"],
            innerSize: "50%",
            data: []
        }],
        drilldown: {
            series:[]
        }
    });
}