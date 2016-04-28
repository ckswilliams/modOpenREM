function chartSetExportSize(chartDivName) {
    var chartContainer = $('#'+chartDivName).highcharts();
    chartContainer.setSize($('#'+chartDivName).width(), $('#'+chartDivName).height());
    chartContainer.options.exporting.sourceWidth = $(window).width();
    chartContainer.options.exporting.sourceHeight = $(window).height();
}