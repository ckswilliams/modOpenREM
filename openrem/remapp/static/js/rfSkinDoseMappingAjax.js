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
            skinDoseMapObj.draw();

            skinDoseMapColourScaleObj.initialise(skinDoseMapObj.minDose, skinDoseMapObj.maxDose, 70, skinDoseMapObj.skinDoseMapCanvas.height);
            skinDoseMapColourScaleObj.draw();

            $('#maxDose').html(skinDoseMapObj.maxDose.toFixed(3) + " Gy");

            document.getElementById("currentWindowWidth").value = skinDoseMapObj.windowWidth.toFixed(3);
            document.getElementById("currentWindowLevel").value = skinDoseMapObj.windowLevel.toFixed(3);

            document.getElementById("windowWidthSlider").max = skinDoseMapObj.windowWidth;
            document.getElementById("windowLevelSlider").max = skinDoseMapObj.windowWidth;

            document.getElementById("windowWidthSlider").value = skinDoseMapObj.windowWidth;
            document.getElementById("windowLevelSlider").value = skinDoseMapObj.windowLevel;

            document.getElementById("minDoseSlider").min = skinDoseMapObj.minDose;
            document.getElementById("minDoseSlider").max = skinDoseMapObj.maxDose;
            document.getElementById("minDoseSlider").value = skinDoseMapObj.minDose;
            document.getElementById("currentMinDisplayedDose").value = skinDoseMapObj.minDose.toFixed(3);

            document.getElementById("maxDoseSlider").min = skinDoseMapObj.minDose;
            document.getElementById("maxDoseSlider").max = skinDoseMapObj.maxDose;
            document.getElementById("maxDoseSlider").value = skinDoseMapObj.maxDose;
            document.getElementById("currentMaxDisplayedDose").value = skinDoseMapObj.maxDose.toFixed(3);

            // 3D skin map stuff
            var currentDose, scaledDose, newColour, i, j, k;
            k = 0;
            for (i = 69; i >= 0; i--) {
                for (j = 0; j < 14; j++) {
                    currentDose = json.skin_map_not_rotated[j * 70 + i];
                    scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
                    if (scaledDose < 0) scaledDose = 0;
                    if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
                    newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

                    dataTextureFront.image.data[k] = newColour[0];
                    dataTextureFront.image.data[k+1] = newColour[1];
                    dataTextureFront.image.data[k+2] = newColour[2];
                    dataTextureFront.image.data[k+3] = 0;
                    k += 4;
                }
            }
            k = 0;
            for (i = 69; i >= 0; i--) {
                for (j = 14; j < 45; j++) {
                    currentDose = json.skin_map_not_rotated[j * 70 + i];
                    scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
                    if (scaledDose < 0) scaledDose = 0;
                    //if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
                    newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

                    dataTextureLeft.image.data[k] = newColour[0];
                    dataTextureLeft.image.data[k+1] = newColour[1];
                    dataTextureLeft.image.data[k+2] = newColour[2];
                    dataTextureLeft.image.data[k+3] = 0;
                    k += 4;
                }
            }
            k = 0;
            for (i = 69; i >= 0; i--) {
                for (j = 45; j < 59; j++) {
                    currentDose = json.skin_map_not_rotated[j * 70 + i];
                    scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
                    if (scaledDose < 0) scaledDose = 0;
                    //if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
                    newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

                    dataTextureBack.image.data[k] = newColour[0];
                    dataTextureBack.image.data[k+1] = newColour[1];
                    dataTextureBack.image.data[k+2] = newColour[2];
                    dataTextureBack.image.data[k+3] = 0;
                    k += 4;
                }
            }
            k = 0;
            for (i = 69; i >= 0; i--) {
                for (j = 59; j < 90; j++) {
                    currentDose = json.skin_map_not_rotated[j * 70 + i];
                    scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
                    if (scaledDose < 0) scaledDose = 0;
                    if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
                    newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

                    dataTextureRight.image.data[k] = newColour[0];
                    dataTextureRight.image.data[k+1] = newColour[1];
                    dataTextureRight.image.data[k+2] = newColour[2];
                    dataTextureRight.image.data[k+3] = 0;
                    k += 4;
                }
            }

            dataTextureFront.needsUpdate = true;
            dataTextureBack.needsUpdate  = true;
            dataTextureLeft.needsUpdate  = true;
            dataTextureRight.needsUpdate = true;
            // End of 3D skin map stuff

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
