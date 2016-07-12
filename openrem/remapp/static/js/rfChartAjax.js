function URLToArray(url) {
    var request = {};
    var pairs = url.substring(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < pairs.length; i++) {
        if(!pairs[i])
            continue;
        var pair = pairs[i].split('=');
        request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]).replace(/\+/g, ' ');
    }
    return request;
}


function ArrayToURL(array) {
    var pairs = [];
    for (var key in array)
        if (array.hasOwnProperty(key))
            pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(array[key]));
    return pairs.join('&');
}


// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var request_data = ArrayToURL(URLToArray(this.URL));

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: "/openrem/rf/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            var colour_scale = chroma.scale('RdYlBu');

            // Study workload chart data
            if(typeof plotRFStudyPerDayAndHour !== 'undefined') {
                updateWorkloadChart(json.studiesPerHourInWeekdays, 'piechartStudyWorkloadDIV', colour_scale);
            }

            // Study description frequency chart data start
            if(typeof plotRFStudyFreq !== 'undefined') {
                updateFrequencyChart(json.studyNameList, json.studySystemList, json.studySummary, urlStartStudy, 'piechartStudyDIV', colour_scale);
            }

            // DAP per study description data
            if( typeof plotRFStudyDAP !== 'undefined') {
                updateAverageChart(json.studyNameList, json.studySystemList, json.studySummary, json.studyHistogramData, plotAverageChoice, 'plotRFStudyDAPContainer', colour_scale);
                sortChartDataToDefault(chartSorting, chartSortingDirection, 'plotRFStudyDAPContainer');
            }

            $(".ajax-progress").hide();
        },
        error: function( xhr, status, errorThrown ) {
            $(".ajax-progress").hide();
            $(".ajax-error").show();
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }
    });
    return false;
});