(function (H) {
        //DATALABELS
        H.wrap(H.Series.prototype, 'drawDataLabels', function (proceed) {
var css = this.chart.options.drilldown.activeDataLabelStyle;
            proceed.call(this);

            css.textDecoration = 'none';
            css.fontWeight = 'normal';
            css.cursor = 'default';
            css.color = 'blue';


            H.each(this.points, function (point) {

                if (point.drilldown && point.dataLabel) {
                    point.dataLabel
                        .css(css)
                        .on('click', function () {
                        return false;
                    });
                }
            });
        });

        //For X-axis labels
        H.wrap(H.Point.prototype, 'init', function (proceed, series, options, x) {
            var point = proceed.call(this, series, options, x),
                chart = series.chart,
                tick = series.xAxis && series.xAxis.ticks[x],
                tickLabel = tick && tick.label;
            console.log("series");
            console.log(series);

            if (point.drilldown) {

                // Add the click event to the point label
                H.addEvent(point, 'click', function () {
                    point.doDrilldown;
                });

                // Make axis labels clickable
                if (tickLabel) {
                    if (!tickLabel._basicStyle) {
                        tickLabel._basicStyle = tickLabel.element.getAttribute('style');
                    }
                    tickLabel.addClass('highcharts-drilldown-axis-label')
                        .css({
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