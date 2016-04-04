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

                var decimalPlaces = Math.abs(Math.ceil(Math.log10(skinDoseMapObj.maxDose))) + 3;

                $('#skinDoseMapGroup').width(skinDoseMapObj.skinDoseMapCanvas.width + 80).height(skinDoseMapObj.skinDoseMapCanvas.height);

                skinDoseMapObj.draw();

                skinDoseMapColourScaleObj.initialise(skinDoseMapObj.minDose, skinDoseMapObj.maxDose, 70, skinDoseMapObj.skinDoseMapCanvas.height, decimalPlaces);
                skinDoseMapColourScaleObj.draw();

                skinDoseMapGroupOrigWidth = $('#skinDoseMapGroup').width();
                skinDoseMapGroupOrigHeight = $('#skinDoseMapGroup').height();

                $('#maxDose').html(skinDoseMapObj.maxDose.toFixed(decimalPlaces));
                $('#phantomDimensions').html(json.phantom_height + 'x' + json.phantom_width + 'x' + json.phantom_depth);
                $('#patientHeight').html((json.patient_height/100).toFixed(2));
                $('#patientMass').html(json.patient_mass.toFixed(1));

                $('input[name=windowWidthSlider]').prop({
                    'max': skinDoseMapObj.windowWidth,
                    'step': Math.pow(10, -decimalPlaces),
                    'value': skinDoseMapObj.windowWidth
                });
                $('input[name=currentWindowWidth]').val(skinDoseMapObj.windowWidth.toFixed(decimalPlaces));

                $('input[name=windowLevelSlider]').prop({
                    'max': skinDoseMapObj.windowWidth,
                    'step': Math.pow(10, -decimalPlaces),
                    'value': skinDoseMapObj.windowLevel
                });
                $('input[name=currentWindowLevel]').val(skinDoseMapObj.windowLevel.toFixed(decimalPlaces));

                $('input[name=minDoseSlider]').prop({
                    'min': skinDoseMapObj.minDose,
                    'max': skinDoseMapObj.maxDose,
                    'step': Math.pow(10, -decimalPlaces),
                    'value': skinDoseMapObj.minDose
                });
                $('input[name=currentMinDisplayedDose]').val(skinDoseMapObj.minDose.toFixed(decimalPlaces));

                $('input[name=maxDoseSlider]').prop({
                    'min': skinDoseMapObj.minDose,
                    'max': skinDoseMapObj.maxDose,
                    'step': Math.pow(10, -decimalPlaces),
                    'value': skinDoseMapObj.maxDose
                });
                $('input[name=currentMaxDisplayedDose]').val(skinDoseMapObj.maxDose.toFixed(decimalPlaces));

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
