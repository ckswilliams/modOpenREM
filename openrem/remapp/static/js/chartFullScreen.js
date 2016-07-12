var chartStartHeight = 0;
var chartStartFooterHeight = 0;
var chartFullScreen = false;

function enterFullScreen(div_id, chart_div) {
    if (chartFullScreen == false) {
        chartStartHeight = document.getElementById(chart_div).clientHeight;
        chartStartFooterHeight = document.getElementById(div_id).clientHeight - chartStartHeight;
        document.getElementById(chart_div).style.height = $(window).height() - chartStartFooterHeight + 'px';
        chartFullScreen = true;
    }
    else {
        document.getElementById(chart_div).style.height = chartStartHeight + 'px';
        chartFullScreen = false;
    }

    $('#'+div_id).toggleClass('fullscreen');

    var chart_div_element = $('#'+chart_div);
    var chart = chart_div_element.highcharts();
    chart.setSize(chart_div_element.width(), chart_div_element.height());
}


function fitChartToDiv(chart_div) {
    var chart_div_element = $('#'+chart_div);
    if (chart_div_element.width() && chart_div_element.height()) {
        var chart = chart_div_element.highcharts();
        chart.setSize(chart_div_element.width(), chart_div_element.height());
    }
}