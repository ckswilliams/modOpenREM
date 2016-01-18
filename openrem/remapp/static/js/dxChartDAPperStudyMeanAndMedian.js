$(function () {
var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'DAP per study description';
var bins = [];
var name = '';

var chartDAPperStudy = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'plotDXStudyMeanDAPContainer',
            events: {
                drilldown: function(e) {
                    bins = e.point.bins;
                    name = (e.point.name).replace('&amp;', '%26');
                    chartDAPperStudy.setTitle({ text: drilldownTitle + e.point.name + ' DAP values' }, { text: '(n = ' + e.point.freq +')' });
                    chartDAPperStudy.yAxis[0].setTitle({text:'Number'});
                    chartDAPperStudy.xAxis[0].setTitle({text:'DAP range (cGy.cm<sup>2</sup>)'});
                    chartDAPperStudy.xAxis[0].setCategories([], true);
                    chartDAPperStudy.tooltip.options.formatter = function(e) {
                        var linkText = 'study_dap_min=' + bins[this.x] + '&study_dap_max=' + bins[this.x+1] + '&study_description=' + name;
                        var returnValue = '<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/dx/?acquisitionhist=1&' + linkText + tooltipFiltersStudy + '">Click to view</a></td></tr></table>';
                        return returnValue;
                    }
                },
                drillup: function(e) {
                    chartDAPperStudy.setTitle({ text: defaultTitle }, { text: '' });
                    chartDAPperStudy.yAxis[0].setTitle({text:'DAP (cGy.cm<sup>2</sup>)'});
                    chartDAPperStudy.xAxis[0].setTitle({text:'Study description'});
                    chartDAPperStudy.xAxis[0].update({
                        categories: {
                            formatter: function (args) {
                                return this.value;
                            }
                        }
                    });
                    chartDAPperStudy.tooltip.options.formatter = function(args) {
                        return this.point.tooltip;
                    }
                }
            }
        },
        title: {
            text: 'DAP per study description'
        },
        legend: {
            enabled: true
        },
        xAxis: {
            categories: [1,2,3,4,5],
            title: {
                useHTML: true,
                text: 'Study description'
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
                text: 'DAP (cGy.cm<sup>2</sup>)'
            }
        },
        tooltip: {
            formatter: function (args) {
                return this.point.tooltip;
            },

            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Mean DAP per study description',
            data: []
        }, {
            name: 'Median DAP per study description',
            data: []
        }],
        drilldown: {
            series: []
        }
    });

    switch(chartSorting) {
        case 'freq':
            anySeriesSort('#plotDXStudyMeanDAPContainer', 'freq', chartSortingDirection, 0);
            break;
        case 'dap':
            anySeriesSort('#plotDXStudyMeanDAPContainer', 'y', chartSortingDirection, 0);
            break;
        case 'name':
            anySeriesSort('#plotDXStudyMeanDAPContainer', 'name', chartSortingDirection, 0);
            break;
        default:
            anySeriesSort('#plotDXStudyMeanDAPContainer', 'name', chartSortingDirection, 0);
    }

});

