function colourScaleSelection(div) {
    var colour_scales = ['OrRd','PuBu','BuPu','Oranges','BuGn','YlOrBr',
        'YlGn','Reds','RdPu','Greens','YlGnBu','Purples','GnBu','Greys',
        'YlOrRd','PuRd','Blues','PuBuGn'];
    var i, j;
    var colour_scale;
    var canvas, context;
    var side_length = 15;
    var num_shades = 11;

    for (i=0; i<colour_scales.length; i++) {
        canvas = document.getElementById(colour_scales[i]);
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


function useNewColourScale(new_scale) {
    skinDoseMapObj.useNewColourScale(new_scale);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.useNewColourScale(new_scale);
    skinDoseMapColourScaleObj.draw();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.useNewColourScale(new_scale);
        skinDoseMap3dObj.draw();
    }
}


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


function rgbToDoseInGy(r, g, b, doseUpperLimit) {
    return doseUpperLimit * ((r * b) + g) / 65535.0;
}


function doseInGyToRGB(dose) {
    var r, g, b;
    dose = dose / 10. * 65535;
    r = Math.floor(dose / 255);
    g = Math.round(dose % 255);
    b = 255;
    return 'rgb(' + r.toString() + ',' + g.toString() + ',' + b.toString() + ')';
}


function reset() {
    skinDoseMapObj.updateWindowWidth(skinDoseMapObj.maxDose - skinDoseMapObj.minDose);
    skinDoseMapObj.updateWindowLevel(skinDoseMapObj.minDose + (skinDoseMapObj.windowWidth/2.0));
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();

        skinDoseMap3dObj.reset();
        skinDoseMap3dPersonObj.reset();
    }

    $('input[name=currentWindowLevel]').val(skinDoseMapObj.windowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentWindowWidth]').val(skinDoseMapObj.windowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $('input[name=windowLevelSlider]').prop({'value': skinDoseMapObj.windowLevel});
    $('input[name=windowWidthSlider]').prop({'value': skinDoseMapObj.windowWidth});

    $('input[name=minDoseSlider]').prop({'value': skinDoseMapObj.minDose});
    $('input[name=maxDoseSlider]').prop({'value': skinDoseMapObj.maxDose});

    $('input[name=currentMinDisplayedDose]').val(skinDoseMapObj.minDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skinDoseMapObj.maxDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


function updateWindowLevel(newWindowLevel) {
    newWindowLevel = parseFloat(newWindowLevel);
    if (newWindowLevel < 0) newWindowLevel = 0;

    $('input[name=currentWindowLevel]').val(newWindowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=windowLevelSlider]').prop({'value': newWindowLevel});

    skinDoseMapObj.updateWindowLevel(newWindowLevel);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    $('input[name=minDoseSlider]').prop({'value': skinDoseMapObj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skinDoseMapObj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


function updateWindowWidth(newWindowWidth) {
    newWindowWidth = parseFloat(newWindowWidth);
    $('input[name=currentWindowWidth]').val(newWindowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=windowWidthSlider]').prop({'value': newWindowWidth});

    skinDoseMapObj.updateWindowWidth(newWindowWidth);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    $('input[name=minDoseSlider]').prop({'value': skinDoseMapObj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skinDoseMapObj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


function updateMinDisplayedDose(minDisplayedDose) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skinDoseMapObj.updateMinDisplayedDose(minDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues();
}


function updateMaxDisplayedDose(maxDisplayedDose) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skinDoseMapObj.updateMaxDisplayedDose(maxDisplayedDose)
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues();
}


function updateMinDisplayedDoseManual(minDisplayedDose) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skinDoseMapObj.updateMinDisplayedDoseManual(minDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues();
}


function updateMaxDisplayedDoseManual(maxDisplayedDose) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skinDoseMapObj.updateMaxDisplayedDoseManual(maxDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();

    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues();
}


function updateSlidersAndValues() {
    $('input[name=minDoseSlider]').prop({'value': skinDoseMapObj.minDisplayedDose});
    $('input[name=maxDoseSlider]').prop({'value': skinDoseMapObj.maxDisplayedDose});

    $('input[name=currentMinDisplayedDose]').val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentMaxDisplayedDose]').val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $('input[name=currentWindowLevel]').val(skinDoseMapObj.windowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $('input[name=currentWindowWidth]').val(skinDoseMapObj.windowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $('input[name=windowLevelSlider]').prop({'value': skinDoseMapObj.windowLevel});
    $('input[name=windowWidthSlider]').prop({'value': skinDoseMapObj.windowWidth});
}


var previousMousePosition = {
    x: 0,
    y: 0
};


$("#skinDoseMap")
    .on('mouseup', function (e) {
        isDragging = false;
    })
    .on('mousedown', function (e) {
        isDragging = true;
    })
    .on('mousemove', function (e) {
        var pos = findPos(this);
        var x = e.pageX - pos.x;
        var y = e.pageY - pos.y;
        var p = skinDoseMapObj.skinDoseMapContext.getImageData(x, y, 1, 1).data;
        var mag = skinDoseMapObj.mag;
        var current_dose = skinDoseMapObj.skinDoseMap[(Math.floor(this.height/mag)-1 - Math.floor(y/mag)) * Math.floor(this.width/mag) + Math.floor(x/mag)].toPrecision(2) + " Gy";
        $('[data-tooltip="skin_dose_map"]').qtip('option', 'content.text', current_dose);

        var deltaMove = {
            x: e.offsetX - previousMousePosition.x,
            y: e.offsetY - previousMousePosition.y
        };

        if (isDragging) {
            var maxWL = parseFloat(document.getElementById("windowLevelSlider").max);
            var newWL = skinDoseMapObj.windowLevel * (100-deltaMove.y)/100;
            if (newWL == 0) newWL += 0.01;
            if (newWL < 0) newWL = 0;
            if (newWL > maxWL) newWL = maxWL;
            skinDoseMapObj.updateWindowLevel(newWL);

            var maxWW = parseFloat(document.getElementById("windowWidthSlider").max);
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

            updateSlidersAndValues();
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


function downloadCanvas(link, canvasId, filename) {
    var canvas = document.getElementById(canvasId);

    if (canvas.msToBlob) { //for IE
        var blob = canvas.msToBlob();
        window.navigator.msSaveBlob(blob, filename);
    } else { //other browsers
        link.href = canvas.toDataURL();
        link.download = filename;
    }
}

function download3dCanvas(link, filename) {
    if (renderer.domElement.msToBlob) { //for IE
        var blob = renderer.domElement.msToBlob();
        window.navigator.msSaveBlob(blob, filename);
    } else { //other browsers
        link.href = renderer.domElement.toDataURL('image/png');
        link.download = filename;
    }
}

document.getElementById('save2dSkinMap').addEventListener('click', function() {
    downloadCanvas(this, 'skinDoseMap', '2dSkinMap.png');
}, false);

document.getElementById('save3dSkinMap').addEventListener('click', function() {
    download3dCanvas(this, '3dSkinMap.png');
}, false);

document.getElementById('skinDoseMapOverlayShow').addEventListener('click', function() {
    $('#skinDoseMapOverlayHide').toggle();
    $('#skinDoseMapOverlayShow').toggle();
    skinDoseMapObj.toggleOverlay();
}, false);

document.getElementById('skinDoseMapOverlayHide').addEventListener('click', function() {
    $('#skinDoseMapOverlayHide').toggle();
    $('#skinDoseMapOverlayShow').toggle();
    skinDoseMapObj.toggleOverlay();
}, false);


var skinMapFullScreen = false;
var skinDoseMapGroupOrigWidth, skinDoseMapGroupOrigHeight;
document.getElementById('skinDoseMapFullscreenBtn').addEventListener('click', function() {
    skinMapFullScreen = (skinMapFullScreen == true) ? skinMapFullScreen = false : skinMapFullScreen = true;

    var otherHeight = $('#skinDoseMapContainer').height() - $('#skinDoseMap').height();

    $('#skinDoseMapContainer').toggleClass('fullscreen');

    if (skinMapFullScreen) {
        var skinDoseMapGroupWidth = $(window).width();
        var skinDoseMapGroupHeight = $(window).height() - otherHeight;

        var maxMagWidth = Math.floor((skinDoseMapGroupWidth-80) / skinDoseMapObj.skinDoseMapWidth);
        var maxMagHeight = Math.floor(skinDoseMapGroupHeight / skinDoseMapObj.skinDoseMapHeight);

        skinDoseMapObj.mag = (maxMagHeight <= maxMagWidth) ? maxMagHeight : maxMagWidth;
        skinDoseMapObj.resizeSkinDoseMap();
        $('#skinDoseMapGroup').width(skinDoseMapObj.skinDoseMapCanvas.width + 80 + 'px').height(skinDoseMapObj.skinDoseMapCanvas.height + 'px');
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
        $('#skinDoseMapGroup').width(skinDoseMapGroupOrigWidth).height(skinDoseMapGroupOrigHeight);
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
}, false);


function isCanvasSupported(){
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));
}


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
