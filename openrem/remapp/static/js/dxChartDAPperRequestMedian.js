$(function () {
    var drilldownTitle = 'Histogram of ';
    var defaultTitle   = 'Median DAP per requested procedure name';
    var bins = [];
    var name = '';


    var chartDAPperRequest = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'plotDXARequestMeanDAPContainer',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartDAPperRequest.setTitle({ text: drilldownTitle + e.point.name + ' DAP values' }, { text: '(n = ' + e.point.freq +')' });
                    chartDAPperRequest.yAxis[0].setTitle({text:'Number'});
                    chartDAPperRequest.xAxis[0].setTitle({text:'DAP range (cGy.cm<sup>2</sup>)'});
                    chartDAPperRequest.xAxis[0].setCategories([], true);
                    chartDAPperRequest.tooltip.options.formatter = function(e) {
                        var linkText = 'study_dap_min=' + bins[this.x] + '&study_dap_max=' + bins[this.x+1] + '&requested_procedure=' + name;
                        returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' exposures</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFiltersRequest + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartDAPperRequest.setTitle({ text: defaultTitle }, { text: '' });
                    chartDAPperRequest.yAxis[0].setTitle({text:'Median DAP (cGy.cm<sup>2</sup>)'});
                    chartDAPperRequest.xAxis[0].setTitle({text:'Requested procedure name'});
                    chartDAPperRequest.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.point.category;
                            }
                        }
                    }, true);
                    chartDAPperRequest.tooltip.options.formatter = function() {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'Median DAP per requested procedure name'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: 'Requested procedure name'
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
            name: 'Median DAP per requested procedure name',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            seriesSort('#plotDXARequestMeanDAPContainer', 'freq', chartSortingDirection);
            break;
        case 'dap':
            seriesSort('#plotDXARequestMeanDAPContainer', 'y', chartSortingDirection);
            break;
        case 'name':
            seriesSort('#plotDXARequestMeanDAPContainer', 'name', chartSortingDirection);
            break;
        default:
            seriesSort('#plotDXARequestMeanDAPContainer', 'name', 1);
    }

});

