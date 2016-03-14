function skinDoseMapObject(skinDoseArray, skinDoseMapWidth, skinDoseMapHeight, skinDoseMapCanvasName,
                           colourScaleName, colourScaleCanvasName, mag) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
        this.applyColourScale();
        this.updateColourScale();
    }


    this.findPos = findPos;
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


    this.rgbToDoseInGy = rgbToDoseInGy;
    function rgbToDoseInGy(r, g, b) {
        return this.doseUpperLimit * ((r * b) + g) / 65535.0;
    }


    this.doseInGyToRGB = doseInGyToRGB;
    function doseInGyToRGB(dose) {
        var r, g, b;
        dose = dose / 10. * 65535;
        r = Math.floor(dose / 255);
        g = Math.round(dose % 255);
        b = 255;
        return 'rgb(' + r.toString() + ',' + g.toString() + ',' + b.toString() + ')';
    }


    this.setPixel = setPixel;
    function setPixel(imageData, x, y, r, g, b, a) {
        var index = (x + y * imageData.width) * 4;
        imageData.data[index + 0] = r;
        imageData.data[index + 1] = g;
        imageData.data[index + 2] = b;
        imageData.data[index + 3] = a;
    }


    this.applyColourScale = applyColourScale;
    function applyColourScale() {
        var x, y, dose, newColour, scaledDose;
        var imageData = this.skinDoseMapContext.getImageData(0, 0, this.skinDoseMapCanvas.width, this.skinDoseMapCanvas.height);
        for (x = 0; x < this.skinDoseMapCanvas.width; x++) {
            for (y = 0; y < this.skinDoseMapCanvas.height; y++) {
                dose = this.skinDoseMap[Math.floor(y / this.mag) * Math.floor(this.skinDoseMapCanvas.width / this.mag) + Math.floor(x / this.mag)];
                scaledDose = dose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();
                this.setPixel(imageData, x, y, newColour[0], newColour[1], newColour[2], 255);
            }
        }
        this.skinDoseMapContext.putImageData(imageData, 0, 0);
    }


    this.resizeSkinDoseMap = resizeSkinDoseMap;
    function resizeSkinDoseMap() {
        this.skinDoseMapCanvas.width = this.skinDoseMapWidth * this.mag;
        this.skinDoseMapCanvas.height = this.skinDoseMapHeight * this.mag;
        this.applyColourScale();
    }


    this.resizeColourScale = resizeColourScale;
    function resizeColourScale() {
        this.colourScaleCanvas.height = this.skinDoseMapHeight * this.mag;
        this.updateColourScale();
    }


    this.reset = reset;
    function reset() {
        this.updateWindowWidth(this.maxDose - this.minDose);
        this.updateWindowLevel(this.minDose + (this.windowWidth / 2.0));
    }


    this.updateWindowLevel = updateWindowLevel;
    function updateWindowLevel(newWindowLevel) {
        if (newWindowLevel < 0) newWindowLevel = 0;
        this.windowLevel = parseFloat(newWindowLevel);

        this.minDisplayedDose = this.windowLevel - (this.windowWidth / 2.0);
        this.maxDisplayedDose = this.windowLevel + (this.windowWidth / 2.0);

        this.applyColourScale();
        this.updateColourScale();
    }


    this.updateWindowWidth = updateWindowWidth;
    function updateWindowWidth(newWindowWidth) {
        this.windowWidth = newWindowWidth;

        this.minDisplayedDose = this.windowLevel - (this.windowWidth / 2.0);
        this.maxDisplayedDose = this.windowLevel + (this.windowWidth / 2.0);
        
        this.applyColourScale();
        this.updateColourScale();
    }


    this.updateMinDisplayedDose = updateMinDisplayedDose;
    function updateMinDisplayedDose(minDisplayedDose) {
        minDisplayedDose = parseFloat(minDisplayedDose);
        
        if (minDisplayedDose <= this.minDose) {
            minDisplayedDose = this.minDose;
        }
        else if (minDisplayedDose >= this.maxDose) {
            minDisplayedDose = this.maxDose;
        }

        // Prevent the minDisplatedDose exceeding the maxDisplayedDose
        if (minDisplayedDose >= this.maxDisplayedDose) {
            this.maxDisplayedDose = minDisplayedDose;
        }

        this.windowWidth = this.maxDisplayedDose - this.minDisplayedDose;
        this.windowLevel = this.minDisplayedDose + (this.windowWidth / 2.0);

        this.applyColourScale();
        this.updateColourScale();
    }


    this.updateMaxDisplayedDose = updateMaxDisplayedDose;
    function updateMaxDisplayedDose(maxDisplayedDose) {
        maxDisplayedDose = parseFloat(maxDisplayedDose);

        if (maxDisplayedDose <= this.minDose) {
            maxDisplayedDose = this.minDose;
        }
        else if (maxDisplayedDose >= this.maxDose) {
            maxDisplayedDose = this.maxDose;
        }

        // Prevent the maxDisplatedDose being smaller than the minDisplayedDose
        if (maxDisplayedDose <= this.minDisplayedDose) {
            this.minDisplayedDose = maxDisplayedDose;
        }

        this.windowWidth = maxDisplayedDose - minDisplayedDose;
        this.windowLevel = minDisplayedDose + (this.windowWidth / 2.0);
        
        this.applyColourScale();
        this.updateColourScale();
    }


    this.updateColourScale = updateColourScale;
    function updateColourScale() {
        var x, y, i, increment, dose, heightOffset, colour;

        this.colourScaleContext.clearRect(0, 0, this.colourScaleCanvas.width, this.colourScaleCanvas.height);

        heightOffset = 20;
        var imageData = this.colourScaleContext.getImageData(0, heightOffset / 2, this.colourScaleCanvas.width, this.colourScaleCanvas.height - heightOffset);

        for (y = 0; y < this.colourScaleCanvas.height - heightOffset; y++) {
            for (x = 55; x < 70; x++) {
                dose = y / (this.colourScaleCanvas.height - heightOffset) * this.doseUpperLimit;
                colour = this.colourScale(1 - (dose / this.doseUpperLimit)).rgb();
                this.setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
            }
        }

        i = 0;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor((this.colourScaleCanvas.height - heightOffset) / 10)) {
            for (x = 50; x < 55; x++) {
                this.setPixel(imageData, x, y, 0, 0, 0, 255);
            }
        }
        for (x = 50; x < 55; x++) {
            this.setPixel(imageData, x, this.colourScaleCanvas.height - heightOffset - 1, 0, 0, 0, 255);
        }
        this.colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

        i = parseFloat(this.windowLevel - this.windowWidth / 2.0);
        increment = (this.windowWidth) / 10;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor((this.colourScaleCanvas.height - heightOffset) / 10)) {
            this.colourScaleContext.fillText(i.toFixed(3), 15, this.colourScaleCanvas.height - y - 7);
            i += increment;
        }
    }


    this.skinDoseMapCanvasName = skinDoseMapCanvasName;
    this.skinDoseMapCanvas = document.getElementById(this.skinDoseMapCanvasName);
    this.skinDoseMapContext = this.skinDoseMapCanvas.getContext('2d');

    this.colourScaleCanvasName = colourScaleCanvasName;
    this.colourScaleCanvas = document.getElementById(this.colourScaleCanvasName);
    this.colourScaleContext = this.colourScaleCanvas.getContext('2d');

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.mag = mag;

    this.skinDoseMap = skinDoseArray;
    this.skinDoseMapWidth = skinDoseMapWidth;
    this.skinDoseMapHeight = skinDoseMapHeight;

    this.minDose = Math.min.apply(null, this.skinDoseMap);
    this.maxDose = Math.max.apply(null, this.skinDoseMap);

    this.doseUpperLimit = 10.0;
    this.windowWidth = this.maxDose - this.minDose;
    this.windowLevel = this.minDose + (this.windowWidth / 2.0);
    this.minDisplayedDose = this.minDose;
    this.maxDisplayedDose = this.maxDose;

    var isDragging = false;

    this.resizeSkinDoseMap();
    this.resizeColourScale();

    // Add the data-tooltip attribute to the skin dose map canvas so that
    // a tooltip can be attached to it.
    this.skinDoseMapCanvas.setAttribute("data-tooltip", "skin_dose_map");
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
        style: {classes: 'qtip-bootstrap'}
    });


    $('#'+this.skinDoseMapCanvasName).mousemove(function (e) {
        var pos = this.findPos(this);
        var x = e.pageX - pos.x;
        var y = e.pageY - pos.y;
        var coord = "x=" + x + ", y=" + y;
        var current_dose = this.skinDoseMap[Math.floor(y / this.mag) * Math.floor(this.width / this.mag) + Math.floor(x / this.mag)].toFixed(3) + " Gy";
        $('[data-tooltip="skin_dose_map"]').qtip('option', 'content.text', current_dose);
    });


    $('#'+this.skinDoseMapCanvasName).mousedown(function () {
        isDragging = true;
    });


    $('#'+this.skinDoseMapCanvasName).mouseup(function () {
        isDragging = false;
    });


    var previousMousePosition = {
        x: 0,
        y: 0
    };


    $('#'+this.skinDoseMapCanvasName).on('mousedown', function (e) {
        isDragging = true;
    }).on('mousemove', function (e) {
        var deltaMove = {
            x: e.offsetX - previousMousePosition.x,
            y: e.offsetY - previousMousePosition.y
        };

        if (isDragging) {
            var maxWL = this.maxDose - this.minDose;
            var newWL = this.windowLevel * (100 - deltaMove.y) / 100;
            if (newWL == 0) newWL += 0.01;
            if (newWL < 0) newWL = 0;
            if (newWL > maxWL) newWL = maxWL;
            this.updateWindowLevel(newWL);

            var maxWW = this.maxDose - this.minDose;
            var newWW = this.windowWidth + this.windowWidth * deltaMove.x / 100;
            if (newWW == 0) newWW += 0.01;
            if (newWW < 0) newWW = 0;
            if (newWW > maxWW) newWW = maxWW;
            this.updateWindowWidth(newWW);
        }

        previousMousePosition = {
            x: e.offsetX,
            y: e.offsetY
        };
    });
}