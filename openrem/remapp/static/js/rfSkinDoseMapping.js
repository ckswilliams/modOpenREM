/**
 * Function to draw the available colour scales
 */
function colourScaleSelection() {
    var colourScales = ["OrRd","PuBu","BuPu","Oranges","BuGn","YlOrBr",
        "YlGn","Reds","RdPu","Greens","YlGnBu","Purples","GnBu","Greys",
        "YlOrRd","PuRd","Blues","PuBuGn"];
    var i, j;
    var colourScale;
    var canvas, context;
    var sideLength = 15;
    var numShades = 11;

    for (i=0; i<colourScales.length; i++) {
        canvas = $("#" + colourScales[i])[0];
        context = canvas.getContext("2d");
        canvas.height = sideLength;
        canvas.width = sideLength * numShades;
        colourScale = chroma.scale(colourScales[i]);
        for (j=0; j<numShades; j++) {
            context.fillStyle = colourScale(j/(numShades-1));
            context.fillRect(j*sideLength, 0, sideLength, sideLength);
        }
    }
}


/**
 * Function to set a new colour scale
 * @param newScale
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function useNewColourScale(newScale, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    skinDoseMapObj.useNewColourScale(newScale);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.useNewColourScale(newScale);
    skinDoseMapColourScaleObj.draw();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.useNewColourScale(newScale);
        skinDoseMap3dObj.draw();
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
    return "rgb(" + r.toString() + "," + g.toString() + "," + b.toString() + ")";
}


/**
 * Function to reset the skin dose maps to their default settings
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 * @param skinDoseMap3dPersonObj
 */
function reset(skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap, skinDoseMap3dPersonObj) {
    skinDoseMapObj.updateWindowWidth(skinDoseMapObj.maxDose - skinDoseMapObj.minDose);
    skinDoseMapObj.updateWindowLevel(skinDoseMapObj.minDose + (skinDoseMapObj.windowWidth/2.0));
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

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

    $("input[name=currentWindowLevel]").val(skinDoseMapObj.windowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentWindowWidth]").val(skinDoseMapObj.windowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $("input[name=windowLevelSlider]").prop({"value": skinDoseMapObj.windowLevel});
    $("input[name=windowWidthSlider]").prop({"value": skinDoseMapObj.windowWidth});

    $("input[name=minDoseSlider]").prop({"value": skinDoseMapObj.minDose});
    $("input[name=maxDoseSlider]").prop({"value": skinDoseMapObj.maxDose});

    $("input[name=currentMinDisplayedDose]").val(skinDoseMapObj.minDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentMaxDisplayedDose]").val(skinDoseMapObj.maxDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the window level has been changed with a slider or the mouse
 * @param newWindowLevel
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateWindowLevel(newWindowLevel, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    newWindowLevel = parseFloat(newWindowLevel);
    if (newWindowLevel < 0) newWindowLevel = 0;

    $("input[name=currentWindowLevel]").val(newWindowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=windowLevelSlider]").prop({"value": newWindowLevel});

    skinDoseMapObj.updateWindowLevel(newWindowLevel);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    $("input[name=minDoseSlider]").prop({"value": skinDoseMapObj.minDisplayedDose});
    $("input[name=maxDoseSlider]").prop({"value": skinDoseMapObj.maxDisplayedDose});

    $("input[name=currentMinDisplayedDose]").val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentMaxDisplayedDose]").val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the window width has been changed with a slider or the mouse
 * @param newWindowWidth
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateWindowWidth(newWindowWidth, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    newWindowWidth = parseFloat(newWindowWidth);
    $("input[name=currentWindowWidth]").val(newWindowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=windowWidthSlider]").prop({"value": newWindowWidth});

    skinDoseMapObj.updateWindowWidth(newWindowWidth);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    $("input[name=minDoseSlider]").prop({"value": skinDoseMapObj.minDisplayedDose});
    $("input[name=maxDoseSlider]").prop({"value": skinDoseMapObj.maxDisplayedDose});

    $("input[name=currentMinDisplayedDose]").val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentMaxDisplayedDose]").val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
}


/**
 * Function to update the skin dose map when the minimum displayed dose has been changed using a slider or the mouse
 * @param minDisplayedDose
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateMinDisplayedDose(minDisplayedDose, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skinDoseMapObj.updateMinDisplayedDose(minDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj);
}


/**
 * Function to update the skin dose map when the maximum displayed dose has been changed using a slider or the mouse
 * @param maxDisplayedDose
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateMaxDisplayedDose(maxDisplayedDose, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skinDoseMapObj.updateMaxDisplayedDose(maxDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj);
}


/**
 * Function to change the skin dose map when the minimum displayed dose has been changed manually
 * @param minDisplayedDose
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateMinDisplayedDoseManual(minDisplayedDose, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    skinDoseMapObj.updateMinDisplayedDoseManual(minDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.minDose = skinDoseMapObj.minDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj);
}


/**
 * Function to update the skin dose map when the maximum displayed dose has been changed
 * @param maxDisplayedDose
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 * @param skinDoseMap3dObj
 * @param show3dSkinDoseMap
 */
function updateMaxDisplayedDoseManual(maxDisplayedDose, skinDoseMapObj, skinDoseMapColourScaleObj, skinDoseMap3dObj, show3dSkinDoseMap) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    skinDoseMapObj.updateMaxDisplayedDoseManual(maxDisplayedDose);
    skinDoseMapObj.draw();
    if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
    skinDoseMapObj.writeInformation();

    skinDoseMapColourScaleObj.maxDose = skinDoseMapObj.maxDisplayedDose;
    skinDoseMapColourScaleObj.redrawValues();

    if (show3dSkinDoseMap) {
        skinDoseMap3dObj.windowWidth = skinDoseMapObj.windowWidth;
        skinDoseMap3dObj.windowLevel = skinDoseMapObj.windowLevel;
        skinDoseMap3dObj.draw();
    }

    updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj);
}


/**
 * Function to update the HTML sliders and their displayed values
 * @param skinDoseMapObj
 * @param skinDoseMapColourScaleObj
 */
function updateSlidersAndValues(skinDoseMapObj, skinDoseMapColourScaleObj) {
    $("input[name=minDoseSlider]").prop({"value": skinDoseMapObj.minDisplayedDose});
    $("input[name=maxDoseSlider]").prop({"value": skinDoseMapObj.maxDisplayedDose});

    $("input[name=currentMinDisplayedDose]").val(skinDoseMapObj.minDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentMaxDisplayedDose]").val(skinDoseMapObj.maxDisplayedDose.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $("input[name=currentWindowLevel]").val(skinDoseMapObj.windowLevel.toFixed(skinDoseMapColourScaleObj.decimalPlaces));
    $("input[name=currentWindowWidth]").val(skinDoseMapObj.windowWidth.toFixed(skinDoseMapColourScaleObj.decimalPlaces));

    $("input[name=windowLevelSlider]").prop({"value": skinDoseMapObj.windowLevel});
    $("input[name=windowWidthSlider]").prop({"value": skinDoseMapObj.windowWidth});
}


var previousMousePosition = {
    x: 0,
    y: 0
};


// jQuery mouse event handlers for the DIV that contains the 2D skin dose map
$("#skinDoseMap")
    .on("mouseup", function () {
        isDragging = false;
    })
    .on("mousedown", function () {
        isDragging = true;
    })
    .on("mousemove", function (e) {
        var pos = findPos(this);
        var x = e.pageX - pos.x;
        var y = e.pageY - pos.y;
        //var p = skinDoseMapObj.skinDoseMapContext.getImageData(x, y, 1, 1).data;
        var mag = skinDoseMapObj.mag;
        if (x <= this.width-1 && y <= this.height-1) {
            var current_dose = parseFloat(skinDoseMapObj.skinDoseMap[(Math.floor(y/mag)) * Math.floor(this.width/mag) + Math.floor(x/mag)]).toPrecision(2) + " Gy";
            $("[data-tooltip='skin_dose_map']").qtip("option", "content.text", current_dose);
        }

        var deltaMove = {
            x: e.offsetX - previousMousePosition.x,
            y: e.offsetY - previousMousePosition.y
        };

        if (isDragging) {
            var maxWL = parseFloat($("#windowLevelSlider")[0].max);
            var newWL = skinDoseMapObj.windowLevel * (100-deltaMove.y)/100;
            if (newWL === 0) newWL += 0.01;
            if (newWL < 0) newWL = 0;
            if (newWL > maxWL) newWL = maxWL;
            skinDoseMapObj.updateWindowLevel(newWL);

            var maxWW = parseFloat($("#windowWidthSlider")[0].max);
            var newWW = skinDoseMapObj.windowWidth + skinDoseMapObj.windowWidth * deltaMove.x/100;
            if (newWW === 0) newWW += 0.01;
            if (newWW < 0) newWW = 0;
            if (newWW > maxWW) newWW = maxWW;
            skinDoseMapObj.updateWindowWidth(newWW);

            skinDoseMapObj.draw();
            if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
            skinDoseMapObj.writeInformation();

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

colourScaleSelection("colour_scale_selection");

$("[data-tooltip='skin_dose_map']").qtip({
    content: {
        text: ""
    },
    position: {
        target: "mouse",
        adjust: {
            mouse: true,
            x: 15,
            y: 15
        }
    },
    style: { classes: "qtip-bootstrap" }
});


/**
 * Function to enable the user to save the contents of the HTML canvas as a png file
 * @param link
 * @param canvasId
 * @param filename
 */
function downloadCanvas(link, canvasId, filename) {
    var canvas = $("#"+canvasId)[0];

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
        link.href = renderer.domElement.toDataURL("image/png");
        link.download = filename;
    }
}

$("#save2dSkinMap").click(function() {
    downloadCanvas(this, "skinDoseMap", "2dSkinMap.png");
});

$("#save3dSkinMap").click(function() {
    download3dCanvas(this, "3dSkinMap.png");
});

$("#skinDoseMapOverlayShow").click(function() {
    $("#skinDoseMapOverlayHide").toggle();
    $("#skinDoseMapOverlayShow").toggle();
    skinDoseMapObj.toggleOverlay();
});

$("#skinDoseMapOverlayHide").click(function() {
    $("#skinDoseMapOverlayHide").toggle();
    $("#skinDoseMapOverlayShow").toggle();
    skinDoseMapObj.toggleOverlay();
});


var skinMapFullScreen = false;
var skinDoseMapGroupOrigWidth, skinDoseMapGroupOrigHeight;
$("#skinDoseMapFullscreenBtn").click(function() {
    skinMapFullScreen = !skinMapFullScreen;

    var skinDoseMapContainer = $("#skinDoseMapContainer");

    var otherHeight = skinDoseMapContainer.height() - $("#skinDoseMap").height();

    skinDoseMapContainer.toggleClass("fullscreen");

    var skinDoseMapGroup = $("#skinDoseMapGroup");

    if (skinMapFullScreen) {
        var skinDoseMapGroupWidth = $(window).width();
        var skinDoseMapGroupHeight = $(window).height() - otherHeight;

        var maxMagWidth = Math.floor((skinDoseMapGroupWidth-80) / skinDoseMapObj.skinDoseMapWidth);
        var maxMagHeight = Math.floor(skinDoseMapGroupHeight / skinDoseMapObj.skinDoseMapHeight);

        skinDoseMapObj.mag = (maxMagHeight <= maxMagWidth) ? maxMagHeight : maxMagWidth;
        skinDoseMapObj.resizeSkinDoseMap();
        skinDoseMapGroup.width(skinDoseMapObj.skinDoseMapCanvas.width + 80 + "px").height(skinDoseMapObj.skinDoseMapCanvas.height + "px");
        skinDoseMapObj.draw();
        skinDoseMapObj.updateBoundaries();
        if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
        skinDoseMapObj.writeInformation();

        skinDoseMapColourScaleObj.resizeColourScale(70, skinDoseMapObj.skinDoseMapCanvas.height);
        skinDoseMapColourScaleObj.draw();

        if (show3dSkinDoseMap) {
            skinDoseMap3dObj.canvas.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dObj.canvas.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dObj.draw();
            skinDoseMap3dHUDObj.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dHUDObj.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dHUDObj.redraw();
        }
    } else {
        skinDoseMapGroup.width(skinDoseMapGroupOrigWidth).height(skinDoseMapGroupOrigHeight);
        skinDoseMapObj.mag = 6;
        skinDoseMapObj.resizeSkinDoseMap();
        skinDoseMapObj.draw();
        skinDoseMapObj.updateBoundaries();
        if (skinDoseMapObj.showOverlay) skinDoseMapObj.drawOverlay();
        skinDoseMapObj.writeInformation();

        skinDoseMapColourScaleObj.resizeColourScale(70, skinDoseMapObj.skinDoseMapCanvas.height);
        skinDoseMapColourScaleObj.draw();

        if (show3dSkinDoseMap) {
            skinDoseMap3dObj.canvas.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dObj.canvas.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dObj.draw();
            skinDoseMap3dHUDObj.width = skinDoseMapObj.skinDoseMapCanvas.width;
            skinDoseMap3dHUDObj.height = skinDoseMapObj.skinDoseMapCanvas.height;
            skinDoseMap3dHUDObj.redraw();
        }
    }
});


/**
 * Function to check that the HTML5 canvas is supported by the user's browser
 * @returns {boolean}
 */
function isCanvasSupported(){
    var elem = document.createElement("canvas");
    return !!(elem.getContext && elem.getContext("2d"));
}


/**
 * Function to toggle between 2D and 3D skin dose map display
 */
function switch2d3dSkinDoseMap() {
    $("#save2dSkinMap").toggle();
    $("#save3dSkinMap").toggle();
    $("#skinDoseMap3d").toggle();
    $("#skinDoseMap").toggle();

    $("#maxDose").toggleClass("whiteText");
    $("#phantomDimensions").toggleClass("whiteText");
    $("#patientHeight").toggleClass("whiteText");
    $("#patientMass").toggleClass("whiteText");
    $("#patientOrientation").toggleClass("whiteText");
}
