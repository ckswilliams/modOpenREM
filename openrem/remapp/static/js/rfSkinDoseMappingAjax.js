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
        url: this.URL + 'skin_map/',
        data: request_data,
        dataType: "json",
        success: function( json ) {

            skinDoseMapObj.initialise(json.skin_map, 90, 70);

            skinDoseMapColourScaleObj.initialise(skinDoseMapObj.minDose, skinDoseMapObj.maxDose, 70, skinDoseMapObj.skinDoseMapCanvas.height);
            //skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDose;
            //skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDose;
            //skinDoseMapColourScaleObj.height = skinDoseMapObj.skinDoseMapCanvas.height;
            //skinDoseMapColourScaleObj.resizeColourScale();

            $('#maxDose').html(skinDoseMapObj.maxDose.toFixed(3) + " Gy");

            document.getElementById("currentWindowWidth").value = parseFloat(skinDoseMapObj.windowWidth).toFixed(3);
            document.getElementById("currentWindowLevel").value = parseFloat(skinDoseMapObj.windowLevel).toFixed(3);

            document.getElementById("windowWidthSlider").max = parseFloat(skinDoseMapObj.windowWidth);
            document.getElementById("windowLevelSlider").max = parseFloat(skinDoseMapObj.windowWidth);

            document.getElementById("windowWidthSlider").value = parseFloat(skinDoseMapObj.windowWidth);
            document.getElementById("windowLevelSlider").value = parseFloat(skinDoseMapObj.windowLevel);

            document.getElementById("minDoseSlider").min = skinDoseMapObj.minDose;
            document.getElementById("minDoseSlider").max = skinDoseMapObj.maxDose;
            document.getElementById("minDoseSlider").value = skinDoseMapObj.minDose;
            document.getElementById("currentMinDisplayedDose").value = skinDoseMapObj.minDose.toFixed(3);

            document.getElementById("maxDoseSlider").min = skinDoseMapObj.minDose;
            document.getElementById("maxDoseSlider").max = skinDoseMapObj.maxDose;
            document.getElementById("maxDoseSlider").value = skinDoseMapObj.maxDose;
            document.getElementById("currentMaxDisplayedDose").value = skinDoseMapObj.maxDose.toFixed(3);

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
