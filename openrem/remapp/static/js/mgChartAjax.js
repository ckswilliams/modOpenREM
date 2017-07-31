function URLToArray(url) {
    var request = {};
    var pairs = url.substring(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < pairs.length; i++) {
        if (!pairs[i] || pairs[i].indexOf("=") === -1)
            continue;
        var pair = pairs[i].split('=');
        pair[1] = pair[1].replace(/\+/g, ' ');
        request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
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
        url: "/openrem/mg/chart/",
        data: request_data,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            //var colour_scale = chroma.scale('RdYlBu');
            var colour_scale = chroma.scale('Dark2');

            // Study workload chart data
            if(typeof plotMGStudyPerDayAndHour !== 'undefined') {
                updateWorkloadChart(json.studiesPerHourInWeekdays, 'piechartStudyWorkloadDIV', colour_scale);
            }

            // AGD vs compressed thickness scatter plot
            if(typeof plotMGAGDvsThickness !== 'undefined') {
                updateScatterChart(json.AGDvsThickness, json.maxThicknessAndAGD, 'scatterDIV1', json.AGDvsThicknessSystems, 'mm', 'mGy', [0,2], colour_scale);
            }

            // kVp vs compressed thickness scatter plot
            if(typeof plotMGkVpvsThickness !== 'undefined') {
                updateScatterChart(json.kVpvsThickness, json.maxThicknessAndkVp, 'scatterDIV2', json.kVpvsThicknessSystems, 'mm', 'kV', [0,0], colour_scale);
            }

            // mAs vs compressed thickness scatter plot
            if(typeof plotMGmAsvsThickness !== 'undefined') {
                updateScatterChart(json.mAsvsThickness, json.maxThicknessAndmAs, 'scatterDIV3', json.mAsvsThicknessSystems, 'mm', 'mAs', [0,1], colour_scale);
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