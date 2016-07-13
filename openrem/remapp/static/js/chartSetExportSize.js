function chartSetExportSize(chartDivName) {
    var chartContainer = $('#'+chartDivName).highcharts();
    chartContainer.options.exporting.sourceWidth = $(window).width();
    chartContainer.options.exporting.sourceHeight = $(window).height();
}