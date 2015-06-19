$(function () {

var drilldownTitle = 'Histogram of ';
var defaultTitle   = 'Mean DLP per study description';
var tooltipData = [2];

var chartStudyDLP = new Highcharts.Chart({
        chart: {
            type: 'column',
            renderTo: 'histogramStudyPlotDIV',
            events: {
                drilldown: function(e) {
                    tooltipData[0] = (studyNames[e.point.x]).replace('&amp;', '%26');
                    tooltipData[1] = e.point.x;
                    chartStudyDLP.setTitle({ text: drilldownTitle + e.point.name}, { text: '(n = ' + studySeriesDataN[e.point.x] +')' });
                    chartStudyDLP.yAxis[0].setTitle({text:'Number'});
                    chartStudyDLP.xAxis[0].setTitle({text:'DLP range (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setCategories([], true);
                    chartStudyDLP.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var linkText = 'study_dlp_min=' + studyBins[tooltipData[1]][this.x] + '&study_dlp_max=' + studyBins[tooltipData[1]][this.x+1] + '&study_description=' + tooltipData[0];
                            xyArr.push('<table style="text-align: center"><tr><td>' + this.y.toFixed(0) + ' studies</td></tr><tr><td><a href="/openrem/ct/?studyhist=1&' + linkText + tooltipFiltersStudy + '">Click to view</a></td></tr></table>');
                        });
                        return xyArr.join('<br/>');
                    }
                },
                drillup: function(e) {
                    chartStudyDLP.setTitle({ text: defaultTitle }, { text: '' });
                    chartStudyDLP.yAxis[0].setTitle({text:'Mean DLP (mGy.cm)'});
                    chartStudyDLP.xAxis[0].setTitle({text:'Study description'});
                    chartStudyDLP.xAxis[0].setCategories(studyNames, true);
                    chartStudyDLP.xAxis[0].update({labels:{rotation:90}});
                    chartStudyDLP.tooltip.options.formatter = function() {
                        var xyArr=[];
                        $.each(this.points,function(){
                            var index = studyNames.indexOf(this.x);
                            xyArr.push(this.x + '<br/>' + this.y.toFixed(1) + ' mGy.cm' + '<br/>(n=' + studySeriesDataN[index] + ')');
                        });
                        return xyArr.join('<br/>');
                    }
                }
            }
        },
        title: {
            useHTML: true,
            text: 'Mean DLP per study description'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: studyNames,
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
                text: 'Mean DLP (mGy.cm)'
            }
        },
        tooltip: {
            formatter: function () {
                var index = studyNames.indexOf(this.x);
                var comment = this.x + '<br/>' + this.y.toFixed(1) + ' mGy.cm' + '<br/>(n=' + studySeriesDataN[index] + ')';
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
            name: 'Mean DLP per study description',
            data: studySeriesData
        }],
        drilldown: {
            series: studySeriesDrilldown
        }
    });
});

