$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DLP and CTDI<sub>vol</sub> per acquisition protocol';
var tooltipData = [2];

var chartAcqDLPandCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotDLPandCTDIdiv'
        },
        title: {
            useHTML: true,
            text: 'Mean DLP and CTDI<sub>vol</sub> per acquisition protocol'
        },
        xAxis: {
            categories: protocolNames,
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: [{
            min: 0,
            title: {
                text: 'DLP (mGy.cm)'
            }
        }, {
            title: {
                useHTML: true,
                text: 'CTDI<sub>vol</sub> (mGy)'
            },
            opposite: true
        }],
        tooltip: {
            useHTML: true,
            formatter: function(args) {
                var this_point_index = this.series.data.indexOf( this.point );
                var this_series_index = this.series.index;
                var that_series_index = this.series.index == 0 ? 1 : 0; // assuming 2 series
                var this_series = args.chart.series[this_series_index];
                var that_series = args.chart.series[that_series_index];
                var this_point = this_series.data[this_point_index];
                var that_point = that_series.data[this_point_index];
                var this_series_label = this.series.index == 0 ? ' mGy.cm DLP' : ' mGy CTDI<sub>vol</sub>';
                var that_series_label = this.series.index == 0 ? ' mGy CTDI<sub>vol</sub>' : ' mGy.cm DLP';
                return this.point.name +
                    '<br/>' + this_point.y.toFixed(1) + this_series_label +
                    '<br/>' + that_point.y.toFixed(1) + that_series_label;
            }
        },
        plotOptions: {
            column: {
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean DLP per acquisition protocol',
            data: seriesData
        }, {
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesDataCTDI,
            yAxis: 1
        }],
        drilldown: {
            series: (seriesDrilldown).concat(seriesDrilldownCTDI)
        },
        legend: {
            useHTML: true,
            align: 'center',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 0,
            x: 0,
            y: 30
        }
    });
});

