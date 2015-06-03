$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean CTDI<sub>vol</sub> per acquisition protocol';
var tooltipData = [2];

var chartAcqCTDI = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramPlotCTDIdiv',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (protocolNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartAcqCTDI.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + seriesDataN[e.point.x] +')' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'Number'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'CTDI<sub>vol</sub> range (mGy)'});
                    chartAcqCTDI.xAxis[0].setCategories([], true);
                    chartAcqCTDI.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var linkText = 'acquisition_ctdi_min=' + protocolBinsCTDI[tooltipData[1]][this.x] + '&acquisition_ctdi_max=' + protocolBinsCTDI[tooltipData[1]][this.x+1] + '&acquisition_protocol=' + tooltipData[0];
                            xyArr.push('<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/ct/?acquisitionhist=1&' + linkText + tooltipFiltersAcqCTDI + '">Click to view</a></td></tr></table>');
                        });
                        return xyArr.join('<br/>');
                    }
                },
                drillup: function(e) {
                    chartAcqCTDI.setTitle({ text: defaultTitle }, { text: '' });
                    chartAcqCTDI.yAxis[0].setTitle({text:'Mean CTDI<sub>vol</sub> (mGy)'});
                    chartAcqCTDI.xAxis[0].setTitle({text:'Protocol name'});
                    chartAcqCTDI.xAxis[0].setCategories(protocolNames, true);
                    chartAcqCTDI.xAxis[0].update({labels:{rotation:90}});
                    chartAcqCTDI.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var index = protocolNames.indexOf(this.x);
                            xyArr.push(this.x + '<br/>' + this.y.toFixed(1) + ' mGy' + '<br/>(n=' + seriesDataN[index] + ')');
                        });
                        return xyArr.join('<br/>');
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean CTDI<sub>vol</sub> per acquisition protocol'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: protocolNames,
            title: {
                useHTML: true,
                text: 'Protocol name'
            },
            labels: {
                useHTML: true,
                rotation: 90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'Mean CTDI<sub>vol</sub> (mGy)'
            }
        },
        tooltip: {
            formatter: function () {
                var index = protocolNames.indexOf(this.x);
                var comment = this.x + '<br/>' + this.y.toFixed(1) + ' mGy' + '<br/>(n=' + seriesDataN[index] + ')';
                return comment;
            },
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            useHTML: true,
            name: 'Mean CTDI<sub>vol</sub> per acquisition protocol',
            data: seriesDataCTDI
        }],
        drilldown: {
            series: seriesDrilldownCTDI
        }
    });
});

