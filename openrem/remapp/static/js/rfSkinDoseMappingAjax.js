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
    var i, j, temp;

    $(".ajax-progress").show();

    $.ajax({
        type: "GET",
        url: this.URL + 'skin_map/',
        data: request_data,
        dataType: "json",
        success: function( json ) {

            skin_map = json.skin_map;

            canvas.width = json.width*mag;
            canvas.height = json.height*mag;
            colourScaleCanvas.height = json.height*mag;

            var i, j;

            // Draw the skin dose map onto the canvas
            for (i=0; i<json.width; i++) {
                for (j=0; j<json.height; j++) {
                    context.fillStyle = doseInGyToRGB(skin_map[j*json.width+i]);
                    context.fillRect(i*mag, j*mag, mag, mag);
                }
            }

            // Apply a colour scale to the image
            var minDose, maxDose;
            minDose = Math.min.apply(null, skin_map);
            maxDose = Math.max.apply(null, skin_map);
            windowWidth = maxDose - minDose;
            windowLevel = minDose + (windowWidth/2.0);
            applyColourScale(windowLevel, windowWidth);

            $('#maxDose').html(maxDose.toFixed(3) + " Gy");

            document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
            document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);

            document.getElementById("windowWidthSlider").max = parseFloat(windowWidth);
            document.getElementById("windowLevelSlider").max = parseFloat(windowWidth);

            document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);
            document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);

            document.getElementById("minDoseSlider").min = minDose;
            document.getElementById("minDoseSlider").max = maxDose;
            document.getElementById("minDoseSlider").value = minDose;
            document.getElementById("currentMinDisplayedDose").value = minDose.toFixed(3);

            document.getElementById("maxDoseSlider").min = minDose;
            document.getElementById("maxDoseSlider").max = maxDose;
            document.getElementById("maxDoseSlider").value = maxDose;
            document.getElementById("currentMaxDisplayedDose").value = maxDose.toFixed(3);

            updateColourScale();

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
