$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle   = 'Median DAP per acquisition protocol';
    var bins = [];
    var name = '';


    var chartDAPperAcquisition = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'container',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartDAPperAcquisition.setTitle({ text: drilldownTitle + e.point.name + ' DAP values' }, { text: '(n = ' + e.point.freq +')' });
                    chartDAPperAcquisition.yAxis[0].setTitle({text:'Number'});
                    chartDAPperAcquisition.xAxis[0].setTitle({text:'DAP range (cGy.cm<sup>2</sup>)'});
                    chartDAPperAcquisition.xAxis[0].setCategories([], true);
                    chartDAPperAcquisition.tooltip.options.formatter = function(e) {
                        var linkText = 'acquisition_dap_min=' + (bins[this.x])/1000000 + '&acquisition_dap_max=' + (bins[this.x+1])/1000000 + '&acquisition_protocol=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFilters + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartDAPperAcquisition.setTitle({ text: defaultTitle }, { text: '' });
                    chartDAPperAcquisition.yAxis[0].setTitle({text:'Median DAP (cGy.cm<sup>2</sup>)'});
                    chartDAPperAcquisition.xAxis[0].setTitle({text:'Protocol name'});
                    chartDAPperAcquisition.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartDAPperAcquisition.tooltip.options.formatter = function() {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'Median DAP per acquisition protocol'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: 'Protocol name'
            },
            labels: {
                useHTML: true,
                rotation:90
            }
        },
        yAxis: {
            min: 0,
            title: {
                useHTML: true,
                text: 'Median DAP (cGy.cm<sup>2</sup>)'
            }
        },
        tooltip: {
            formatter: function () {
                return this.point.tooltip;
            },
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Median DAP per acquisition protocol',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            seriesSort('#container', 'freq', chartSortingDirection);
            break;
        case 'dap':
            seriesSort('#container', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#container', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#container', 'name', 1);
    }

});

