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


function rgbToDoseInGy(r, g, b) {
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

function setPixel(imageData, x, y, r, g, b, a) {
    var index = (x + y * imageData.width) * 4;
    imageData.data[index + 0] = r;
    imageData.data[index + 1] = g;
    imageData.data[index + 2] = b;
    imageData.data[index + 3] = a;
}


function applyColourScale(wl, ww) {
    var x, y, dose, newColour, scaledDose;
    var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    for (x = 0; x < canvas.width; x++) {
        for (y = 0; y < canvas.height; y++) {
            dose = skinDoses[y * canvas.width + x];
            scaledDose = dose - (wl-(ww/2.0));
            if (scaledDose < 0) scaledDose = 0;
            if (scaledDose > ww) scaledDose = ww;
            newColour = colourScale(1 - (scaledDose / ww)).rgb();
            setPixel(imageData, x, y, newColour[0], newColour[1], newColour[2], 255);
        }
    }
    context.putImageData(imageData, 0, 0);
}


$('#skinDoseMap').mousemove(function (e) {
    var pos = findPos(this);
    var x = e.pageX - pos.x;
    var y = e.pageY - pos.y;
    var coord = "x=" + x + ", y=" + y;
    $('#hoverDose').html(skinDoses[y * this.width + x] + " Gy");
});


function reset() {
    var minDose, maxDose;
    minDose = Math.min.apply(null, skinDoses);
    maxDose = Math.max.apply(null, skinDoses);
    windowWidth = maxDose - minDose;
    windowLevel = minDose + (windowWidth/2.0);

    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateWindowLevel(newWindowLevel) {
    if (newWindowLevel < 0) newWindowLevel = 0;
    windowLevel = parseFloat(newWindowLevel);
    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);
    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateWindowWidth(newWindowWidth) {
    windowWidth = newWindowWidth;
    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);
    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateColourScale() {
    var x, y, i, increment, dose, heightOffset;

    colourScaleContext.clearRect(0, 0, colourScaleCanvas.width, colourScaleCanvas.height);

    heightOffset = 20;
    var imageData = colourScaleContext.getImageData(0, heightOffset / 2, colourScaleCanvas.width, colourScaleCanvas.height - heightOffset);

    for (y = 0; y < colourScaleCanvas.height - heightOffset; y++) {
        for (x = 35; x < 50; x++) {
            dose = y / (colourScaleCanvas.height - heightOffset) * doseUpperLimit;
            colour = colourScale(dose / doseUpperLimit).rgb();
            setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
        }
    }

    i = 0;
    for (y = 0; y < colourScaleCanvas.height; y += Math.floor((colourScaleCanvas.height - heightOffset) / 10)) {
        for (x = 30; x < 35; x++) {
            setPixel(imageData, x, y, 0, 0, 0, 255);
        }
    }
    for (x = 30; x < 35; x++) {
        setPixel(imageData, x, colourScaleCanvas.height - heightOffset - 1, 0, 0, 0, 255);
    }
    colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

    i = parseFloat(windowLevel - windowWidth/2.0);
    increment = (windowWidth) / 10;
    for (y = 0; y < colourScaleCanvas.height; y += Math.floor((colourScaleCanvas.height - heightOffset) / 10)) {
        colourScaleContext.fillText(i.toFixed(3), 0, colourScaleCanvas.height - y - 7);
        i += increment;
    }
}


$("#skinDoseMap").mousedown(function () {
    isDragging = true;
});


$("#skinDoseMap").mouseup(function () {
    isDragging = false;
});


var previousMousePosition = {
    x: 0,
    y: 0
};


$("#skinDoseMap").on('mousedown', function (e) {
    isDragging = true;
}).on('mousemove', function (e) {
    var deltaMove = {
        x: e.offsetX - previousMousePosition.x,
        y: e.offsetY - previousMousePosition.y
    };

    if (isDragging) {
        var newWL = windowLevel * (100-deltaMove.y)/100;
        if (newWL == 0) newWL += 0.01;
        if (newWL < 0) newWL = 0;
        updateWindowLevel(newWL);

        var newWW = windowWidth + windowWidth * deltaMove.x/100;
        if (newWW == 0) newWW += 0.01;
        if (newWW < 0) newWW = 0;
        updateWindowWidth(newWW);
    }

    previousMousePosition = {
        x: e.offsetX,
        y: e.offsetY
    };
});



var canvas = document.getElementById('skinDoseMap');
var context = canvas.getContext('2d');
var skinDoses = new Array(100800);
var mag = 4;
var doseUpperLimit = 10.0;
var windowWidth, windowLevel;

var colourScaleCanvas = document.getElementById('colourScale');
var colourScaleContext = colourScaleCanvas.getContext('2d');

var isDragging = false;

var colourScale = chroma.scale('RdYlBu');

$(document).ready(function () {
    var i, j;

    // Draw the skin dose map onto the canvas
    for (i=0; i<70; i++) {
        for (j=0; j<90; j++) {
            context.fillStyle = doseInGyToRGB(skin_map[j*context.canvas.width+i]);
            context.fillRect(i*4, j*4, 4, 4);
        }
    }

    // Initialise the skin doses from skin_map
    var current_dose, k, l;
    for (i=0; i<70; i++) {
        for (j=0; j<90; j++) {
            current_dose = skin_map[j*70+i];
            for (k=i*4; k<(i+1)*4; k++) {
                for (l=j*4; l<(j+1)*4; l++) {
                    skinDoses[l*280+k] = current_dose;
                }
            }
        }
    }

    // Apply a colour scale to the image
    var minDose, maxDose;
    minDose = Math.min.apply(null, skinDoses);
    maxDose = Math.max.apply(null, skinDoses);
    windowWidth = maxDose - minDose;
    windowLevel = minDose + (windowWidth/2.0);
    applyColourScale(windowLevel, windowWidth);

    $('#minDose').html(minDose.toFixed(3) + " Gy");
    $('#maxDose').html(maxDose.toFixed(3) + " Gy");

    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);

    document.getElementById("windowWidthSlider").max = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowLevelSlider").max = parseFloat(windowWidth).toFixed(3);

    updateColourScale();
});