function sortChartDataToDefault(sorting_field, sorting_direction, chart_div) {
    switch(sorting_field) {
        case 'freq':
            anySeriesSort('#'+chart_div, 'total_counts', sorting_direction, 0);
            break;
        case 'dlp':
            anySeriesSort('#'+chart_div, 'avg_value', sorting_direction, 0);
            break;
        case 'ctdi':
            anySeriesSort('#'+chart_div, 'avg_value', sorting_direction, 0);
            break;
        case 'dap':
            anySeriesSort('#'+chart_div, 'avg_value', sorting_direction, 0);
            break;
        case 'name':
            anySeriesSort('#'+chart_div, 'name', sorting_direction, 0);
            break;
        default:
            anySeriesSort('#'+chart_div, 'name', 1, 0);
    }
}


function updateWorkloadChart(workload_data, chart_div, colour_scale) {
    var day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var day_total = 0;
    var workload_series_data = [];
    var drilldown_series_data = [];
    var temp_time, i, j, temp;
    for (i = 0; i < 7; i++) {
        day_total = 0;
        temp = [];
        for (j = 0; j < 24; j++) {
            day_total += workload_data[i][j];
            temp_time = "0" + j;
            temp_time = temp_time.substr(temp_time.length-2);
            temp.push({name: temp_time + ':00', y: workload_data[i][j], color: colour_scale(j/(23)).hex()});
        }
        workload_series_data.push({
            name: day_names[i],
            y: day_total,
            color: colour_scale(i/(6)).hex(),
            drilldown: day_names[i]
        });
        drilldown_series_data.push({
            id: day_names[i],
            name: day_names[i],
            useHTML: true,
            type: 'pie',
            data: temp
        });
    }

    var chart = $('#'+chart_div).highcharts();
    chart.options.drilldown.series = drilldown_series_data;
    chart.series[0].setData(workload_series_data);
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();
    chart.redraw({duration: 1000});
}


function updateOverTimeChart(name_list, over_time_data, series_colours, url_start, chart_div) {
    var date_axis, current_value, temp_date, date_after, date_before, temp, i, j;
    var chart = $('#'+chart_div).highcharts();

    var index = name_list.indexOf(null);
    if (index !== -1) name_list[index] = "Blank";

    date_axis = [];
    for (i = 0; i < over_time_data[0].length; i++) {
        temp_date = new Date(Date.parse(over_time_data[0][i][0]));
        temp_date = formatDate(temp_date);
        date_axis.push(temp_date);
    }
    chart.xAxis[0].setCategories(date_axis);

    for (i = 0; i < over_time_data.length; i++) {
        temp = [];
        for (j = 0; j < over_time_data[0].length; j++) {
            temp_date = new Date(Date.parse(over_time_data[i][j][0]));
            date_after = formatDate(temp_date);
            date_before = formatDate(new Date((new Date((temp_date).setMonth((temp_date).getMonth() + 1))).setDate((new Date((temp_date).setMonth((temp_date).getMonth() + 1))).getDate() - 1)));

            current_value = parseFloat(over_time_data[i][j][1]);
            if (current_value == 0 || isNaN(current_value)) current_value = null;

            temp.push({
                y: current_value,
                url: url_start + name_list[i] + '&date_after=' + date_after + '&date_before=' + date_before
            });
        }

        chart.addSeries({
            name: name_list[i],
            color: series_colours[i],
            marker: {enabled: true},
            point: {
                events: {
                    click: function (e) {
                        location.href = e.point.url;
                        e.preventDefault();
                    }
                }
            },
            data: temp
        });
    }

    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();
    chart.redraw({duration: 1000});
}


function updateFrequencyChart(name_list, system_list, summary_data, url_start, chart_div, colour_scale) {
    var piechart_data = new Array(name_list.length);
    var data_counts = 0;
    var i, j;

    var index = name_list.indexOf(null);
    if (index !== -1) name_list[index] = "Blank";

    for (i = 0; i < name_list.length; i++) {
        data_counts = 0;
        for (j = 0; j < system_list.length; j++) {
            data_counts += parseInt(summary_data[j][i].num)
        }
        piechart_data[i] = {
            name: name_list[i],
            y: data_counts,
            url: url_start + name_list[i]
        };
    }

    piechart_data.sort(sort_by_name);
    piechart_data.sort(sort_by_y);

    var colour_max = name_list.length == 1 ? name_list.length : name_list.length - 1;

    for (i = 0; i < name_list.length; i++) {
        piechart_data[i].color = colour_scale(i / colour_max).hex();
    }

    var chart = $('#'+chart_div).highcharts();
    chart.series[0].setData(piechart_data);
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();

    chart.redraw({duration: 1000});
}


function updateAverageChart(name_list, system_list, summary_data, histogram_data, average_choice, chart_div, colour_scale) {
    var data_counts = []; while(data_counts.push([]) < system_list.length);
    var data_bins = []; while(data_bins.push([]) < system_list.length);
    var total_counts_per_name = [];
    var current_counts;
    var average_value_per_name = [];
    var current_value;
    var calc_histograms = typeof histogram_data !== 'undefined';
    var i, j, k;

    var index = name_list.indexOf(null);
    if (index !== -1) name_list[index] = "Blank";

    // Calculate counts per name and average value per name. These are used to sort the chart series by.
    if(calc_histograms) {
        for (j = 0; j < name_list.length; j++) {
            current_counts = 0;
            current_value = 0;
            for (i = 0; i < system_list.length; i++) {
                (data_counts[i]).push(histogram_data[i][j][0]);
                (data_bins[i]).push(histogram_data[i][j][1]);
                current_counts += parseFloat(summary_data[i][j].num);
                if (average_choice == "mean" || average_choice == "both") {
                    current_value += parseFloat(summary_data[i][j].num) * parseFloat(summary_data[i][j].mean);
                }
                else {
                    current_value += parseFloat(summary_data[i][j].num) * parseFloat(summary_data[i][j].median);
                }
            }
            total_counts_per_name.push(current_counts);
            average_value_per_name.push(current_value / current_counts);
        }
    }
    else {
        for (j = 0; j < name_list.length; j++) {
            current_counts = 0;
            current_value = 0;
            for (i = 0; i < system_list.length; i++) {
                current_counts += parseFloat(summary_data[i][j].num);
                if (average_choice == "mean" || average_choice == "both") {
                    current_value += parseFloat(summary_data[i][j].num) * parseFloat(summary_data[i][j].mean);
                }
                else {
                    current_value += parseFloat(summary_data[i][j].num) * parseFloat(summary_data[i][j].median);
                }
            }
            total_counts_per_name.push(current_counts);
            average_value_per_name.push(current_value / current_counts);
        }
    }

    if (average_choice == "mean" || average_choice == "both") {
        var mean_data = []; while(mean_data.push([]) < system_list.length);
        for (i = 0; i < system_list.length; i++) {
            for (j = 0; j < name_list.length; j++) {
                var current_mean = summary_data[i][j].mean != null ? summary_data[i][j].mean : 0;
                var current_num = summary_data[i][j].num != null ? summary_data[i][j].num : 0;
                (mean_data[i]).push({
                    name: name_list[j],
                    y: summary_data[i][j].mean,
                    freq: summary_data[i][j].num,
                    bins: data_bins[i][j],
                    tooltip: system_list[i] + '<br>' + name_list[j] + '<br>' + current_mean.toFixed(1) + ' mean<br>(n=' + current_num + ')',
                    drilldown: calc_histograms ? system_list[i]+name_list[j] : null,
                    total_counts: total_counts_per_name[j],
                    avg_value: average_value_per_name[j]
                });
            }
        }
    }

    if (average_choice == "median" || average_choice == "both") {
        var median_data = []; while(median_data.push([]) < system_list.length);
        for (i = 0; i < system_list.length; i++) {
            for (j = 0; j < name_list.length; j++) {
                (median_data[i]).push({
                    name: name_list[j],
                    y: parseFloat(summary_data[i][j].median),
                    freq: summary_data[i][j].num,
                    bins: data_bins[i][j],
                    tooltip: system_list[i] + '<br>' + name_list[j] + '<br>' + parseFloat(summary_data[i][j].median).toFixed(1) + ' median<br>(n=' + summary_data[i][j].num + ')',
                    drilldown: calc_histograms ? system_list[i]+name_list[j] : null,
                    total_counts: total_counts_per_name[j],
                    avg_value: average_value_per_name[j]
                });
            }
        }
    }

    if (calc_histograms) {
        var temp;
        var drilldown_series = [];
        for (i = 0; i < system_list.length; i++) {
            for (j = 0; j < name_list.length; j++) {
                temp = [];
                for (k = 0; k < data_counts[i][0].length; k++) {
                    temp.push([data_bins[i][j][k].toFixed(1).toString() + ' \u2264 x < ' + data_bins[i][j][k + 1].toFixed(1).toString(), data_counts[i][j][k]]);
                }
                drilldown_series.push({
                    id: system_list[i] + name_list[j],
                    name: system_list[i],
                    useHTML: true,
                    data: temp
                });
            }
        }
    }

    var chart = $('#'+chart_div).highcharts();
    chart.xAxis[0].update({
        categories: name_list,
        min: 0,
        max: name_list.length - 1
    }, false);
    if (calc_histograms) chart.options.drilldown.series = drilldown_series;
    chart.options.exporting.sourceWidth = $(window).width();
    chart.options.exporting.sourceHeight = $(window).height();

    var colour_max;
    if (average_choice == "mean") {
        colour_max = system_list.length == 1 ? system_list.length : system_list.length - 1;
        for (i = 0; i < system_list.length; i++) {
            if (chart.series.length > i) {
                chart.series[i].update({
                    name: system_list[i],
                    data: mean_data[i],
                    color: colour_scale(i/colour_max).hex()
                });
            }
            else {
                chart.addSeries({
                    name: system_list[i],
                    data: mean_data[i],
                    color: colour_scale(i/colour_max).hex()
                });
            }
        }
    }
    else if (average_choice == "median") {
        colour_max = system_list.length == 1 ? system_list.length : system_list.length - 1;
        for (i = 0; i < system_list.length; i++) {
            if (chart.series.length > i) {
                chart.series[i].update({
                    name: system_list[i],
                    data: median_data[i],
                    color: colour_scale(i/colour_max).hex()
                });
            }
            else {
                chart.addSeries({
                    name: system_list[i],
                    data: median_data[i],
                    color: colour_scale(i/colour_max).hex()
                });
            }
        }
    }
    else {
        colour_max = system_list.length;
        var current_series = 0;
        for (i = 0; i < (system_list.length)*2; i+=2) {
            if (chart.series.length > i+1) {
                chart.series[i].update({
                    name: system_list[current_series] + ' (mean)',
                    data: mean_data[current_series],
                    color: colour_scale(i/(colour_max*2-1)).hex()
                });
                chart.series[i+1].update({
                    name: system_list[current_series] + ' (median)',
                    data: median_data[current_series],
                    color: colour_scale((i+1)/(colour_max*2-1)).hex()
                });
            }
            else {
                chart.addSeries({
                    name: system_list[current_series] + ' (mean)',
                    data: mean_data[current_series],
                    color: colour_scale(i/(colour_max*2-1)).hex()
                });
                chart.addSeries({
                    name: system_list[current_series] + ' (median)',
                    data: median_data[current_series],
                    color: colour_scale((i+1)/(colour_max*2-1)).hex()
                });
            }
            current_series++;
        }
    }
    chart.redraw({duration: 1000});
}


function updateScatterChart(scatter_data, max_values, chart_div, system_list, colour_scale) {
    var chart = $('#'+chart_div).highcharts();
    var colour_max = system_list.length;
    var i;

    for (i = 0; i < system_list.length; i++) {
        if (chart.series.length > i) {
            chart.series[i].update({
                type: 'scatter',
                name: system_list[i],
                data: scatter_data[i],
                color: colour_scale(i/colour_max).alpha(0.5).css(),
                marker: {
                    radius: 2
                },
                tooltip: {
                    followPointer: false,
                    pointFormat: '{point.x:.0f} mm<br>{point.y:.2f} mGy'
                }
            });
        }
        else {
            chart.addSeries({
                type: 'scatter',
                name: system_list[i],
                data: scatter_data[i],
                color: colour_scale(i/colour_max).alpha(0.5).css(),
                marker: {
                    radius: 2
                },
                tooltip: {
                    followPointer: false,
                    pointFormat: '{point.x:.0f} mm<br>{point.y:.2f} mGy'
                }
            });
        }

    }

    chart.xAxis[0].update({
        max: max_values[0]
    });
    chart.yAxis[0].update({
        max: max_values[1]
    });
    chart.redraw({duration: 1000});
}
