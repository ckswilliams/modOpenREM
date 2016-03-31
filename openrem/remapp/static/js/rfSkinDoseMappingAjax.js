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
            if (isCanvasSupported()) {
                skinDoseMapObj.initialise(json.skin_map, json.width, json.height, json.phantom_flat_dist, json.phantom_curved_dist);
                $('#skinDoseMapGroup').width(skinDoseMapObj.skinDoseMapCanvas.width + 80 + 'px');
                $('#skinDoseMapGroup').height(skinDoseMapObj.skinDoseMapCanvas.height + 'px');
                skinDoseMapObj.draw();

                skinDoseMapColourScaleObj.initialise(skinDoseMapObj.minDose, skinDoseMapObj.maxDose, 70, skinDoseMapObj.skinDoseMapCanvas.height);
                skinDoseMapColourScaleObj.draw();

                skinDoseMapGroupOrigWidth = $('#skinDoseMapGroup').width();
                skinDoseMapGroupOrigHeight = $('#skinDoseMapGroup').height();

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

                if (show3dSkinDoseMap) {
                    skinDoseMap3dObj.canvas.width = skinDoseMapObj.skinDoseMapCanvas.width;
                    skinDoseMap3dObj.canvas.height = skinDoseMapObj.skinDoseMapCanvas.height;
                    skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
                    skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
                    skinDoseMap3dObj.initialise(json.skin_map, json.phantom_flat_dist, json.phantom_curved_dist, json.phantom_height, json.phantom_depth / 2);
                    skinDoseMap3dObj.draw();
                    skinDoseMap3dPersonObj.initialise(json.phantom_height);
                    render();
                }
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
