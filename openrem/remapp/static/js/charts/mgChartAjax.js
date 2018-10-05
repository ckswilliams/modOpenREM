/*global arrayToURL, urlToArray, chroma, hideButtonsIfOneSeries, updateWorkloadChart, updateScatterChart*/
/*eslint no-undef: "error"*/
/*eslint object-shorthand: "off" */

// Code to update the page and chart data on initial page load.
$(document).ready(function() {
    var requestData = arrayToURL(urlToArray(this.URL));

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: Urls.mg_summary_chart_data(),
        data: requestData,
        dataType: "json",
        success: function( json ) {
            // Initialise some colours to use for plotting
            //var colourScale = chroma.scale("RdYlBu");
            var colourScale = chroma.scale("Dark2");

            // Study workload chart data
            if(typeof plotMGStudyPerDayAndHour !== "undefined") {
                updateWorkloadChart(json.studiesPerHourInWeekdays, "piechartStudyWorkloadDIV", colourScale);
            }

            // AGD vs compressed thickness scatter plot
            if(typeof plotMGAGDvsThickness !== "undefined") {
                updateScatterChart(json.AGDvsThickness, json.maxThicknessAndAGD, "scatterDIV1", json.AGDvsThicknessSystems, "mm", "mGy", [0,2], colourScale);
                hideButtonsIfOneSeries("scatterDIV1", "agd_thick_series_");
            }

            // kVp vs compressed thickness scatter plot
            if(typeof plotMGkVpvsThickness !== "undefined") {
                updateScatterChart(json.kVpvsThickness, json.maxThicknessAndkVp, "scatterDIV2", json.kVpvsThicknessSystems, "mm", "kV", [0,0], colourScale);
                hideButtonsIfOneSeries("scatterDIV2", "kvp_thick_series_");
            }

            // mAs vs compressed thickness scatter plot
            if(typeof plotMGmAsvsThickness !== "undefined") {
                updateScatterChart(json.mAsvsThickness, json.maxThicknessAndmAs, "scatterDIV3", json.mAsvsThicknessSystems, "mm", "mAs", [0,1], colourScale);
                hideButtonsIfOneSeries("scatterDIV3", "mas_thick_series_");
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