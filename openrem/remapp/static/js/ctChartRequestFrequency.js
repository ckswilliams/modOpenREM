$(function () {

var chartRequestFreq = new Highcharts.Chart({
        chart: {
            renderTo: 'piechartRequestDIV',
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
            name: 'Requested procedure frequency',
            point: {
                events: {
                    click: function(e) {
                        var linkText = 'requested_procedure=' + (this.name).replace('&amp;', '%26');
                        location.href = '/openrem/ct/?requestfreq=1&' + linkText + tooltipFiltersRequest;
                        e.preventDefault();
                    }
                }
            },
            data: requestPiechartData
        }]
    });
});