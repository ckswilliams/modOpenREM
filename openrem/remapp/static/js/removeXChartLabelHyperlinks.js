(function (H) {
    H.wrap(H.Point.prototype, 'init', function (proceed, series, options, x) {
        var point = proceed.call(this, series, options, x),
            chart = series.chart,
            tick = series.xAxis && series.xAxis.ticks[x],
            tickLabel = tick && tick.label;

        if (point.drilldown) {

            // Add the click event to the point label
            H.addEvent(point, 'click', function () {
                point.doDrilldown();
            });

            // Make axis labels click-able
            if (tickLabel) {
                if (!tickLabel._basicStyle) {
                    tickLabel._basicStyle = tickLabel.element.getAttribute('style');
                }
                tickLabel.addClass('highcharts-drilldown-axis-label')          .css({
                    'text-decoration': 'none',
                    'font-weight': 'normal',
                    'cursor': 'auto'
                    })
                    .on('click', function () {
                    if (point.doDrilldown) {
                        return false;
                    }
                });

            }
        } else if (tickLabel && tickLabel._basicStyle) {
        }

        return point;
    });
})(Highcharts);
