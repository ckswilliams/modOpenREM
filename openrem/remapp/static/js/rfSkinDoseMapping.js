/**
 * Function to draw the available colour scales
 */
function colourScaleSelection() {
    var colour_scales = ['OrRd','PuBu','BuPu','Oranges','BuGn','YlOrBr',
        'YlGn','Reds','RdPu','Greens','YlGnBu','Purples','GnBu','Greys',
        'YlOrRd','PuRd','Blues','PuBuGn'];
    var i, j;
    var colour_scale;
    var canvas, context;
    var side_length = 15;
    var num_shades = 11;

    for (i=0; i<colour_scales.length; i++) {
        canvas = $('#' + colour_scales[i])[0];
        context = canvas.getContext('2d');
        canvas.height = side_length;
        canvas.width = side_length * num_shades;
        colour_scale = chroma.scale(colour_scales[i]);
        for (j=0; j<num_shades; j++) {
            context.fillStyle = colour_scale(j/(num_shades-1));
            context.fillRect(j*side_length, 0, side_length, side_length);
        }
    }
}


/**
 * Function to set a new colour scale
 * @param new_scale
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function useNewColourScale(new_scale, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    skin_dose_map_obj.useNewColourScale(new_scale);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.useNewColourScale(new_scale);
    skin_dose_map_colour_scale_obj.draw();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.useNewColourScale(new_scale);
        skin_dose_map_3d_obj.draw();
    }
}


/**
 * Function to return the position of the cursor
 * @param obj
 * @returns {*}
 */
function findPos(obj) {
    var curleft = 0, curtop = 0;
    if (obj.offsetParent) {
        do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
        return {x: curleft, y: curtop};
    }
    return undefined;
}


/**
 * Function to decode an rgb value to a dose in Gy
 * @param r
 * @param g
 * @param b
 * @param doseUpperLimit
 * @returns {number}
 */
function rgbToDoseInGy(r, g, b, doseUpperLimit) {
    return doseUpperLimit * ((r * b) + g) / 65535.0;
}


/**
 * Function to convert a dose in Gy to an rgb value
 * @param dose
 * @returns {string}
 */
function doseInGyToRGB(dose) {
    var r, g, b;
    dose = dose / 10. * 65535;
    r = Math.floor(dose / 255);
    g = Math.round(dose % 255);
    b = 255;
    return 'rgb(' + r.toString() + ',' + g.toString() + ',' + b.toString() + ')';
}


/**
 * Function to reset the skin dose maps to their default settings
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 * @param skin_dose_map_3d_person_obj
 */
function reset(skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map, skin_dose_map_3d_person_obj) {
    skin_dose_map_obj.updateWindowWidth(skin_dose_map_obj.maxDose - skin_dose_map_obj.minDose);
    skin_dose_map_obj.updateWindowLevel(skin_dose_map_obj.minDose + (skin_dose_map_obj.windowWidth/2.0));
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.minDose = skin_dose_map_obj.minDisplayedDose;
    skin_dose_map_colour_scale_obj.maxDose = skin_dose_map_obj.maxDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();

        skin_dose_map_3d_obj.reset();
        skin_dose_map_3d_person_obj.reset();
    }

    $('input[name=currentWindowLevel]').val(skin_dose_map_obj.windowLevel.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentWindowWidth]').val(skin_dose_map_obj.windowWidth.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));

    $('input[name=windowLevelSlider]').prop({'value': skin_dose_map_obj.windowLevel});
    $('input[name=windowWidthSlider]').prop({'value': skin_dose_map_obj.windowWidth});

    $('input[name=minDoseSlider]').prop({'value': skin_dose_map_obj.minDose});
    $('input[name=maxDoseSlider]').prop({'value': skin_dose_map_obj.maxDose});

    $('input[name=currentMinDisplayedDose]').val(skin_dose_map_obj.minDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skin_dose_map_obj.maxDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the window level has been changed with a slider or the mouse
 * @param newWindowLevel
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateWindowLevel(newWindowLevel, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    newWindowLevel = parseFloat(newWindowLevel);
    if (newWindowLevel < 0) newWindowLevel = 0;

    $('input[name=currentWindowLevel]').val(newWindowLevel.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=windowLevelSlider]').prop({'value': newWindowLevel});

    skin_dose_map_obj.updateWindowLevel(newWindowLevel);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.minDose = skin_dose_map_obj.minDisplayedDose;
    skin_dose_map_colour_scale_obj.maxDose = skin_dose_map_obj.maxDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    $('input[name=minDoseSlider]').prop({'value': skin_dose_map_obj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skin_dose_map_obj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skin_dose_map_obj.minDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skin_dose_map_obj.maxDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the window width has been changed with a slider or the mouse
 * @param newWindowWidth
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateWindowWidth(newWindowWidth, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    newWindowWidth = parseFloat(newWindowWidth);
    $('input[name=currentWindowWidth]').val(newWindowWidth.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=windowWidthSlider]').prop({'value': newWindowWidth});

    skin_dose_map_obj.updateWindowWidth(newWindowWidth);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.minDose = skin_dose_map_obj.minDisplayedDose;
    skin_dose_map_colour_scale_obj.maxDose = skin_dose_map_obj.maxDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    $('input[name=minDoseSlider]').prop({'value': skin_dose_map_obj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skin_dose_map_obj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skin_dose_map_obj.minDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skin_dose_map_obj.maxDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the minimum displayed dose has been changed using a slider or the mouse
 * @param minDisplayedDose
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateMinDisplayedDose(minDisplayedDose, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skin_dose_map_obj.updateMinDisplayedDose(minDisplayedDose);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.minDose = skin_dose_map_obj.minDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    updateSlidersAndValues(skin_dose_map_obj, skin_dose_map_colour_scale_obj);
}


/**
 * Function to update the skin dose map when the maximum displayed dose has been changed using a slider or the mouse
 * @param maxDisplayedDose
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateMaxDisplayedDose(maxDisplayedDose, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skin_dose_map_obj.updateMaxDisplayedDose(maxDisplayedDose);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.maxDose = skin_dose_map_obj.maxDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    updateSlidersAndValues(skin_dose_map_obj, skin_dose_map_colour_scale_obj);
}


/**
 * Function to change the skin dose map when the minimum displayed dose has been changed manually
 * @param minDisplayedDose
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateMinDisplayedDoseManual(minDisplayedDose, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skin_dose_map_obj.updateMinDisplayedDoseManual(minDisplayedDose);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.minDose = skin_dose_map_obj.minDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    updateSlidersAndValues(skin_dose_map_obj, skin_dose_map_colour_scale_obj);
}


/**
 * Function to update the skin dose map when the maximum displayed dose has been changed
 * @param maxDisplayedDose
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 * @param skin_dose_map_3d_obj
 * @param show_3d_skin_dose_map
 */
function updateMaxDisplayedDoseManual(maxDisplayedDose, skin_dose_map_obj, skin_dose_map_colour_scale_obj, skin_dose_map_3d_obj, show_3d_skin_dose_map) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skin_dose_map_obj.updateMaxDisplayedDoseManual(maxDisplayedDose);
    skin_dose_map_obj.draw();
    if (skin_dose_map_obj.showOverlay) skin_dose_map_obj.drawOverlay();

    skin_dose_map_colour_scale_obj.maxDose = skin_dose_map_obj.maxDisplayedDose;
    skin_dose_map_colour_scale_obj.redrawValues();

    if (show_3d_skin_dose_map) {
        skin_dose_map_3d_obj.windowWidth = skin_dose_map_obj.windowWidth;
        skin_dose_map_3d_obj.windowLevel = skin_dose_map_obj.windowLevel;
        skin_dose_map_3d_obj.draw();
    }

    updateSlidersAndValues(skin_dose_map_obj, skin_dose_map_colour_scale_obj);
}


/**
 * Function to update the HTML sliders and their displayed values
 * @param skin_dose_map_obj
 * @param skin_dose_map_colour_scale_obj
 */
function updateSlidersAndValues(skin_dose_map_obj, skin_dose_map_colour_scale_obj) {
    $('input[name=minDoseSlider]').prop({'value': skin_dose_map_obj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skin_dose_map_obj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skin_dose_map_obj.minDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skin_dose_map_obj.maxDisplayedDose.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));

    $('input[name=currentWindowLevel]').val(skin_dose_map_obj.windowLevel.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));
    $('input[name=currentWindowWidth]').val(skin_dose_map_obj.windowWidth.toFixed(skin_dose_map_colour_scale_obj.decimalPlaces));

    $('input[name=windowLevelSlider]').prop({'value': skin_dose_map_obj.windowLevel});
    $('input[name=windowWidthSlider]').prop({'value': skin_dose_map_obj.windowWidth});
}


var previousMousePosition = {
    x: 0,
    y: 0
};


// jQuery mouse event handlers for the DIV that contains the 2D skin dose map
$("#skinDoseMap")
    .on('mouseup', function () {
        isDragging = false;
    })
    .on('mousedown', function () {
        isDragging = true;
    })
    .on('mousemove', function (e) {
        var pos = findPos(this);
        var x = e.pageX - pos.x;
        var y = e.pageY - pos.y;
        //var p = skinDoseMapObj.skinDoseMapContext.getImageData(x, y, 1, 1).data;
        var mag = skinDoseMapObj.mag;
        if (x <= this.width-1 && y <= this.height-1) {
            var current_dose = parseFloat(skinDoseMapObj.skinDoseMap[(Math.floor(y/mag)) * Math.floor(this.width/mag) + Math.floor(x/mag)]).toPrecision(2) + " Gy";
            $('[data-tooltip="skin_dose_map"]').qtip('option', 'content.text', current_dose);
        }

        var deltaMove = {
            x: e.offsetX - previousMousePosition.x,
            y: e.offsetY - previousMousePosition.y
        };

        if (isDragging) {
            var maxWL = parseFloat($('#windowLevelSlider')[0].max);
            var newWL = skinDoseMapObj.windowLevel * (100-deltaMove.y)/100;
            if (newWL == 0) newWL += 0.01;
            if (newWL < 0) newWL = 0;
            if (newWL > maxWL) newWL = maxWL;
            skinDoseMapObj.updateWindowLevel(newWL);

            var maxWW = parseFloat($('#windowWidthSlider')[0].max);
            var newWW = skinDoseMapObj.windowWidth + skinDoseMapObj.windowWidth * deltaMove.x/100;
            if (newWW == 0) newWW += 0.01;
            if (newWW < 0) newWW = 0;
            if (newWW > maxWW) newWW = maxWW;
            skinDoseMapObj.updateWindowWidth(newWW);

            skinDoseMapObj.draw();
            if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

            skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
            skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
            skinDoseMapColourScaleObj.redrawValues();

            if (show3dSkinDoseMap) {
                skinDoseMap3dObj.windowLevel = newWL;
                skinDoseMap3dObj.windowWidth = newWW;
                skinDoseMap3dObj.draw();
            }

            updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj);
        }

        previousMousePosition = {
            x: e.offsetX,
            y: e.offsetY
        };
    });


var isDragging = false;

colourScaleSelection('colour_scale_selection');

$('[data-tooltip="skin_dose_map"]').qtip({
    content: {
        text: ''
    },
    position: {
        target: 'mouse',
        adjust: {
            mouse: true,
            x: 15,
            y: 15
        }
    },
    style: { classes: 'qtip-bootstrap' }
});


/**
 * Function to enable the user to save the contents of the HTML canvas as a png file
 * @param link
 * @param canvasId
 * @param filename
 */
function downloadCanvas(link, canvasId, filename) {
    var canvas = $('#'+canvasId)[0];

    if (canvas.msToBlob) { //for IE
        var blob = canvas.msToBlob();
        window.navigator.msSaveBlob(blob, filename);
    } else { //other browsers
        link.href = canvas.toDataURL();
        link.download = filename;
    }
}


/**
 * Function to enable the user to save the contents of the three.js display as a png file
 * @param link
 * @param filename
 */
function download3dCanvas(link, filename) {
    if (renderer.domElement.msToBlob) { //for IE
        var blob = renderer.domElement.msToBlob();
        window.navigator.msSaveBlob(blob, filename);
    } else { //other browsers
        link.href = renderer.domElement.toDataURL('image/png');
        link.download = filename;
    }
}

$('#save2dSkinMap').click(function() {
    downloadCanvas(this, 'skinDoseMap', '2dSkinMap.png');
});

$('#save3dSkinMap').click(function() {
    download3dCanvas(this, '3dSkinMap.png');
});

$('#skinDoseMapOverlayShow').click(function() {
    $('#skinDoseMapOverlayHide').toggle();
    $('#skinDoseMapOverlayShow').toggle();
    skinDoseMapObj.toggleOverlay();
});

$('#skinDoseMapOverlayHide').click(function() {
    $('#skinDoseMapOverlayHide').toggle();
    $('#skinDoseMapOverlayShow').toggle();
    skinDoseMapObj.toggleOverlay();
});


var skinMapFullScreen = false;
var skinDoseMapGroupOrigWidth, skinDoseMapGroupOrigHeight;
$('#skinDoseMapFullscreenBtn').click(function() {
    skinMapFullScreen = !skinMapFullScreen;

    var skin_dose_map_container = $('#skinDoseMapContainer');

    var otherHeight = skin_dose_map_container.height() - $('#skinDoseMap').height();

    skin_dose_map_container.toggleClass('fullscreen');

    skin_dose_map_group = $('#skinDoseMapGroup');

    if (skinMapFullScreen) {
        var skinDoseMapGroupWidth = $(window).width();
        var skinDoseMapGroupHeight = $(window).height() - otherHeight;

        var maxMagWidth = Math.floor((skinDoseMapGroupWidth-80) / skinDoseMapObj.skinDoseMapWidth);
        var maxMagHeight = Math.floor(skinDoseMapGroupHeight / skinDoseMapObj.skinDoseMapHeight);

        skinDoseMapObj.mag = (maxMagHeight <= maxMagWidth) ? maxMagHeight : maxMagWidth;
        skinDoseMapObj.resizeSkinDoseMap();
        skin_dose_map_group.width(skinDoseMapObj.skinDoseMapCanvas.width + 80 + 'px').height(skinDoseMapObj.skinDoseMapCanvas.height + 'px');
        skinDoseMapObj.draw();
        skinDoseMapObj.updateBoundaries();
        if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

        skinDoseMapColourScaleObj.resizeColourScale(70, skinDoseMapObj.skinDoseMapCanvas.height);
        skinDoseMapColourScaleObj.draw();

        if (show3dSkinDoseMap) {
            skinDoseMap3dObj.canvas.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dObj.canvas.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dObj.draw();
        }
    } else {
        skin_dose_map_group.width(skinDoseMapGroupOrigWidth).height(skinDoseMapGroupOrigHeight);
        skinDoseMapObj.mag = 6;
        skinDoseMapObj.resizeSkinDoseMap();
        skinDoseMapObj.draw();
        skinDoseMapObj.updateBoundaries();
        if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

        skinDoseMapColourScaleObj.resizeColourScale(70, skinDoseMapObj.skinDoseMapCanvas.height);
        skinDoseMapColourScaleObj.draw();

        if (show3dSkinDoseMap) {
            skinDoseMap3dObj.canvas.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dObj.canvas.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dObj.draw();
        }
    }
});


/**
 * Function to check that the HTML5 canvas is supported by the user's browser
 * @returns {boolean}
 */
function isCanvasSupported(){
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));
}


/**
 * Function to toggle between 2D and 3D skin dose map display
 */
function switch2d3dSkinDoseMap() {
    $('#save2dSkinMap').toggle();
    $('#save3dSkinMap').toggle();
    $('#skinDoseMap3d').toggle();
    $('#skinDoseMap').toggle();

    $('#skinDoseMapInformation').toggleClass('whiteText');
    $('#maxDose').toggleClass('whiteText');
    $('#phantomDimensions').toggleClass('whiteText');
    $('#patientHeight').toggleClass('whiteText');
    $('#patientMass').toggleClass('whiteText');
}
