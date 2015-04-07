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
        legend: {
            enabled: false
        },
        xAxis: {
            categories: protocolNames,
            //title: {
            //    useHTML: true,
            //    text: 'Protocol name'
            //},
            labels: {
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
                text: 'CTDIvol (mGy)'
            },
            opposite: true
        }],
        tooltip: {
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                //pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean DLP per acquisition protocol',
            data: seriesData,
            //pointPadding: 0.2,
            //pointPlacement: 0.1
        }, {
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesDataCTDI,
            //pointPadding: 0.2,
            //pointPlacement: -0.1,
            yAxis: 1
        }],
        legend: {
            align: 'center',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 0,
            x: 0,
            y: 30
        }
    });
});

