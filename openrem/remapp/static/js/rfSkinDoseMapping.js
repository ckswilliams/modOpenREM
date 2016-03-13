function colourScaleSelection(div) {
    var colour_scales = ['OrRd','PuBu','BuPu','Oranges','BuGn','YlOrBr',
        'YlGn','Reds','RdPu','Greens','YlGnBu','Purples','GnBu','Greys',
        'YlOrRd','PuRd','Blues','PuBuGn','Spectral','RdYlGn','RdBu','PiYG',
        'PRGn', 'RdYlBu','BrBG','RdGy','PuOr'];
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
    colourScale = chroma.scale(new_scale);
    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
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
            dose = skin_map[Math.floor(y/mag) * Math.floor(canvas.width/mag) + Math.floor(x/mag)];
            scaledDose = dose - (wl-(ww/2.0));
            if (scaledDose < 0) scaledDose = 0;
            if (scaledDose > ww) scaledDose = ww;
            newColour = colourScale(scaledDose / ww).rgb();
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
    var current_dose = skin_map[Math.floor(y/mag) * Math.floor(this.width/mag) + Math.floor(x/mag)].toFixed(3) + " Gy";
    $('[data-tooltip="skin_dose_map"]').qtip('option', 'content.text', current_dose);
});


function reset() {
    var minDose = parseFloat(document.getElementById("minDoseSlider").min);
    var maxDose = parseFloat(document.getElementById("maxDoseSlider").max);

    windowWidth = maxDose - minDose;
    windowLevel = minDose + (windowWidth/2.0);

    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);

    document.getElementById("minDoseSlider").value = minDose;
    document.getElementById("currentMinDisplayedDose").value = minDose.toFixed(3);
    document.getElementById("maxDoseSlider").value = maxDose;
    document.getElementById("currentMaxDisplayedDose").value = maxDose.toFixed(3);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateWindowLevel(newWindowLevel) {
    if (newWindowLevel < 0) newWindowLevel = 0;
    windowLevel = parseFloat(newWindowLevel);
    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);

    var minDisplayedDose = windowLevel - (windowWidth/2.0);
    var maxDisplayedDose = windowLevel + (windowWidth/2.0);

    document.getElementById("minDoseSlider").value = minDisplayedDose;
    document.getElementById("currentMinDisplayedDose").value = minDisplayedDose.toFixed(3);
    document.getElementById("maxDoseSlider").value = maxDisplayedDose;
    document.getElementById("currentMaxDisplayedDose").value = maxDisplayedDose.toFixed(3);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateWindowWidth(newWindowWidth) {
    windowWidth = newWindowWidth;
    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);

    var minDisplayedDose = windowLevel - (windowWidth/2.0);
    var maxDisplayedDose = windowLevel + (windowWidth/2.0);

    document.getElementById("minDoseSlider").value = minDisplayedDose;
    document.getElementById("currentMinDisplayedDose").value = minDisplayedDose.toFixed(3);
    document.getElementById("maxDoseSlider").value = maxDisplayedDose;
    document.getElementById("currentMaxDisplayedDose").value = maxDisplayedDose.toFixed(3);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateMinDisplayedDose(minDisplayedDose) {
    minDisplayedDose = parseFloat(minDisplayedDose);

    var minDose = parseFloat(document.getElementById("minDoseSlider").min);
    var maxDose = parseFloat(document.getElementById("minDoseSlider").max);

    if (minDisplayedDose <= minDose) {
        minDisplayedDose = minDose;
    }
    else if (minDisplayedDose >= maxDose) {
        minDisplayedDose = maxDose;
    }

    // Prevent the minDisplatedDose exceeding the maxDisplayedDose
    var maxDisplayedDose = parseFloat(document.getElementById("currentMaxDisplayedDose").value);
    if (minDisplayedDose >= maxDisplayedDose) {
        document.getElementById("maxDoseSlider").value = minDisplayedDose;
        document.getElementById("currentMaxDisplayedDose").value = minDisplayedDose.toFixed(3);
        maxDisplayedDose = minDisplayedDose;
    }

    windowWidth = maxDisplayedDose - minDisplayedDose;
    windowLevel = minDisplayedDose +  (windowWidth / 2.0);

    document.getElementById("minDoseSlider").value = minDisplayedDose;
    document.getElementById("currentMinDisplayedDose").value = minDisplayedDose.toFixed(3);

    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);

    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateMaxDisplayedDose(maxDisplayedDose) {
    maxDisplayedDose = parseFloat(maxDisplayedDose);

    var minDose = parseFloat(document.getElementById("minDoseSlider").min);
    var maxDose = parseFloat(document.getElementById("minDoseSlider").max);

    if (maxDisplayedDose <= minDose) {
        maxDisplayedDose = minDose;
    }
    else if (maxDisplayedDose >= maxDose) {
        maxDisplayedDose = maxDose;
    }

    // Prevent the maxDisplatedDose being smaller than the minDisplayedDose
    var minDisplayedDose = parseFloat(document.getElementById("currentMinDisplayedDose").value);
    if (maxDisplayedDose <= minDisplayedDose) {
        document.getElementById("minDoseSlider").value = maxDisplayedDose;
        document.getElementById("currentMinDisplayedDose").value = maxDisplayedDose.toFixed(3);
        minDisplayedDose = maxDisplayedDose;
    }

    windowWidth = maxDisplayedDose - minDisplayedDose;
    windowLevel = minDisplayedDose +  (windowWidth / 2.0);

    document.getElementById("maxDoseSlider").value = maxDisplayedDose;
    document.getElementById("currentMaxDisplayedDose").value = maxDisplayedDose.toFixed(3);

    document.getElementById("currentWindowWidth").value = parseFloat(windowWidth).toFixed(3);
    document.getElementById("windowWidthSlider").value = parseFloat(windowWidth);

    document.getElementById("currentWindowLevel").value = parseFloat(windowLevel).toFixed(3);
    document.getElementById("windowLevelSlider").value = parseFloat(windowLevel);

    applyColourScale(windowLevel, windowWidth);
    updateColourScale();
}


function updateColourScale() {
    var x, y, i, increment, dose, heightOffset;

    colourScaleContext.clearRect(0, 0, colourScaleCanvas.width, colourScaleCanvas.height);

    heightOffset = 20;
    var imageData = colourScaleContext.getImageData(0, heightOffset / 2, colourScaleCanvas.width, colourScaleCanvas.height - heightOffset);

    for (y = 0; y < colourScaleCanvas.height - heightOffset; y++) {
        for (x = 55; x < 70; x++) {
            dose = y / (colourScaleCanvas.height - heightOffset) * doseUpperLimit;
            colour = colourScale(1-(dose / doseUpperLimit)).rgb();
            setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
        }
    }

    i = 0;
    for (y = 0; y < colourScaleCanvas.height; y += Math.floor((colourScaleCanvas.height - heightOffset) / 10)) {
        for (x = 50; x < 55; x++) {
            setPixel(imageData, x, y, 0, 0, 0, 255);
        }
    }
    for (x = 50; x < 55; x++) {
        setPixel(imageData, x, colourScaleCanvas.height - heightOffset - 1, 0, 0, 0, 255);
    }
    colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

    i = parseFloat(windowLevel - windowWidth/2.0);
    increment = (windowWidth) / 10;
    for (y = 0; y < colourScaleCanvas.height; y += Math.floor((colourScaleCanvas.height - heightOffset) / 10)) {
        colourScaleContext.fillText(i.toFixed(3), 15, colourScaleCanvas.height - y - 7);
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
        var maxWL = parseFloat(document.getElementById("windowLevelSlider").max);
        var newWL = windowLevel * (100-deltaMove.y)/100;
        if (newWL == 0) newWL += 0.01;
        if (newWL < 0) newWL = 0;
        if (newWL > maxWL) newWL = maxWL;
        updateWindowLevel(newWL);

        var maxWW = parseFloat(document.getElementById("windowWidthSlider").max);
        var newWW = windowWidth + windowWidth * deltaMove.x/100;
        if (newWW == 0) newWW += 0.01;
        if (newWW < 0) newWW = 0;
        if (newWW > maxWW) newWW = maxWW;
        updateWindowWidth(newWW);
    }

    previousMousePosition = {
        x: e.offsetX,
        y: e.offsetY
    };
});



var canvas = document.getElementById('skinDoseMap');
var context = canvas.getContext('2d');
var mag = 6;
var skin_map;
var doseUpperLimit = 10.0;
var windowWidth, windowLevel;

var colourScaleCanvas = document.getElementById('colourScale');
var colourScaleContext = colourScaleCanvas.getContext('2d');

var isDragging = false;

var colourScale = chroma.scale('Greys');

$('.colour_scale_selection').hide();
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