function skinDoseMapObject(skinDoseMapCanvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.setPixel = setPixel;
    function setPixel(imageData, x, y, r, g, b, a) {
        var index = (x + y * imageData.width) * 4;
        imageData.data[index + 0] = r;
        imageData.data[index + 1] = g;
        imageData.data[index + 2] = b;
        imageData.data[index + 3] = a;
    }


    this.draw = draw;
    function draw() {
        var x, y, dose, scaledDose;
        for (x = 0; x < this.skinDoseMapWidth; x++) {
            for (y = 0; y < this.skinDoseMapHeight; y++) {
                dose = this.skinDoseMap[(this.skinDoseMapHeight-1 - y) * this.skinDoseMapWidth + x];
                scaledDose = dose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                this.skinDoseMapContext.fillStyle = this.colourScale(scaledDose / this.windowWidth).hex();
                this.skinDoseMapContext.fillRect(x*this.mag, y*this.mag, this.mag, this.mag);
            }
        }
    }


    this.drawOverlay = drawOverlay;
    function drawOverlay() {
        this.skinDoseMapContext.textAlign = 'center';
        this.skinDoseMapContext.font = '12pt arial';

        this.skinDoseMapContext.fillStyle = 'rgba(0, 80, 0, 0.85)';
        this.skinDoseMapContext.fillText('Superior', this.skinDoseMapCanvas.width/2, 15);
        this.skinDoseMapContext.fillText('Inferior', this.skinDoseMapCanvas.width/2, this.skinDoseMapCanvas.height-10);

        this.skinDoseMapContext.save();

        this.skinDoseMapContext.rotate(0.5*Math.PI);
        this.skinDoseMapContext.fillStyle = 'rgba(255, 0, 0, 0.85)';
        this.skinDoseMapContext.fillText('Anterior', this.skinDoseMapCanvas.height/2, -this.frontLeftBoundary/2);
        this.skinDoseMapContext.fillText('Posterior', this.skinDoseMapCanvas.height/2, -this.leftBackBoundary - (this.backRightBoundary-this.leftBackBoundary)/2);
        this.skinDoseMapContext.fillText('Left', this.skinDoseMapCanvas.height/2, -this.frontLeftBoundary - (this.leftBackBoundary-this.frontLeftBoundary)/2);
        this.skinDoseMapContext.fillText('Right', this.skinDoseMapCanvas.height/2, -this.rightFrontBoundary + (this.rightFrontBoundary-this.backRightBoundary)/2);

        this.skinDoseMapContext.restore();

        this.skinDoseMapContext.lineWidth = 1;
        this.skinDoseMapContext.setLineDash([5, 15]);
        this.skinDoseMapContext.strokeStyle = 'rgba(255, 0, 0, 0.25)';

        this.skinDoseMapContext.beginPath();
        this.skinDoseMapContext.moveTo(this.frontLeftBoundary, 0);
        this.skinDoseMapContext.lineTo(this.frontLeftBoundary, this.skinDoseMapCanvas.height-1);
        this.skinDoseMapContext.stroke();

        this.skinDoseMapContext.beginPath();
        this.skinDoseMapContext.moveTo(this.leftBackBoundary, 0);
        this.skinDoseMapContext.lineTo(this.leftBackBoundary, this.skinDoseMapCanvas.height-1);
        this.skinDoseMapContext.stroke();

        this.skinDoseMapContext.beginPath();
        this.skinDoseMapContext.moveTo(this.backRightBoundary, 0);
        this.skinDoseMapContext.lineTo(this.backRightBoundary, this.skinDoseMapCanvas.height-1);
        this.skinDoseMapContext.stroke();
    }


    this.resizeSkinDoseMap = resizeSkinDoseMap;
    function resizeSkinDoseMap() {
        this.skinDoseMapCanvas.width = this.skinDoseMapWidth * this.mag;
        this.skinDoseMapCanvas.height = this.skinDoseMapHeight * this.mag;
    }


    this.reset = reset;
    function reset() {
        this.updateWindowWidth(this.maxDose - this.minDose);
        this.updateWindowLevel(this.minDose + (this.windowWidth / 2.0));
    }


    this.toggleOverlay = toggleOverlay;
    function toggleOverlay() {
        this.showOverlay = this.showOverlay ? this.showOverlay = false : this.showOverlay = true;

        if (this.showOverlay) {
            this.drawOverlay();
        } else {
            this.draw();
        }
    }


    this.updateWindowLevel = updateWindowLevel;
    function updateWindowLevel(newWindowLevel) {
        if (newWindowLevel < 0) newWindowLevel = 0;
        this.windowLevel = parseFloat(newWindowLevel);

        this.minDisplayedDose = this.windowLevel - (this.windowWidth / 2.0);
        this.maxDisplayedDose = this.windowLevel + (this.windowWidth / 2.0);
    }


    this.updateWindowWidth = updateWindowWidth;
    function updateWindowWidth(newWindowWidth) {
        this.windowWidth = newWindowWidth;

        this.minDisplayedDose = this.windowLevel - (this.windowWidth / 2.0);
        this.maxDisplayedDose = this.windowLevel + (this.windowWidth / 2.0);
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

        this.minDisplayedDose = minDisplayedDose;

        // Prevent the minDisplatedDose exceeding the maxDisplayedDose
        if (minDisplayedDose >= this.maxDisplayedDose) {
            this.maxDisplayedDose = minDisplayedDose;
        }

        this.windowWidth = this.maxDisplayedDose - this.minDisplayedDose;
        this.windowLevel = this.minDisplayedDose + (this.windowWidth / 2.0);
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

        this.maxDisplayedDose = maxDisplayedDose;

        // Prevent the maxDisplatedDose being smaller than the minDisplayedDose
        if (maxDisplayedDose <= this.minDisplayedDose) {
            this.minDisplayedDose = maxDisplayedDose;
        }

        this.windowWidth = this.maxDisplayedDose - this.minDisplayedDose;
        this.windowLevel = this.minDisplayedDose + (this.windowWidth / 2.0);
    }


    this.updateMinDisplayedDoseManual = updateMinDisplayedDose;
    function updateMinDisplayedDose(minDisplayedDose) {
        minDisplayedDose = parseFloat(minDisplayedDose);

        this.minDisplayedDose = minDisplayedDose;

        // Prevent the minDisplatedDose exceeding the maxDisplayedDose
        if (minDisplayedDose >= this.maxDisplayedDose) {
            this.maxDisplayedDose = minDisplayedDose;
        }

        this.windowWidth = this.maxDisplayedDose - this.minDisplayedDose;
        this.windowLevel = this.minDisplayedDose + (this.windowWidth / 2.0);
    }


    this.updateMaxDisplayedDoseManual = updateMaxDisplayedDose;
    function updateMaxDisplayedDose(maxDisplayedDose) {
        maxDisplayedDose = parseFloat(maxDisplayedDose);

        this.maxDisplayedDose = maxDisplayedDose;

        // Prevent the maxDisplatedDose being smaller than the minDisplayedDose
        if (maxDisplayedDose <= this.minDisplayedDose) {
            this.minDisplayedDose = maxDisplayedDose;
        }

        this.windowWidth = this.maxDisplayedDose - this.minDisplayedDose;
        this.windowLevel = this.minDisplayedDose + (this.windowWidth / 2.0);
    }


    this.initialise = initialise;
    function initialise(skinMapData, skinMapWidth, skinMapHeight, phantomFlatWidth, phantomCurvedEdgeWidth) {
        this.skinDoseMap = skinMapData;
        this.skinDoseMapWidth = skinMapWidth;
        this.skinDoseMapHeight = skinMapHeight;
        this.minDose = Math.min.apply(null, this.skinDoseMap);
        this.maxDose = Math.max.apply(null, this.skinDoseMap);
        this.windowWidth = this.maxDose - this.minDose;
        this.windowLevel = this.minDose + (this.windowWidth / 2.0);
        this.minDisplayedDose = this.minDose;
        this.maxDisplayedDose = this.maxDose;

        this.phantomFlatWidth = phantomFlatWidth;
        this.phantomCurvedEdgeWidth = phantomCurvedEdgeWidth;

        this.resizeSkinDoseMap();
        this.updateBoundaries();
    }


    this.updateBoundaries = updateBoundaries;
    function updateBoundaries () {
        this.frontLeftBoundary = this.phantomFlatWidth * this.mag;
        this.leftBackBoundary = this.frontLeftBoundary + (this.phantomCurvedEdgeWidth * this.mag);
        this.backRightBoundary = this.leftBackBoundary + (this.phantomFlatWidth * this.mag);
        this.rightFrontBoundary = this.backRightBoundary + (this.phantomCurvedEdgeWidth * this.mag);
    }


    this.skinDoseMapCanvasName = skinDoseMapCanvasName;
    this.skinDoseMapCanvas = document.getElementById(this.skinDoseMapCanvasName);
    this.skinDoseMapContext = this.skinDoseMapCanvas.getContext('2d');

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.mag = 6;

    this.skinDoseMap = [];
    this.skinDoseMapWidth = 10;
    this.skinDoseMapHeight = 10;

    this.phantomFlatWidth = 14;
    this.phantomCurvedEdgeWidth = 31;

    this.showOverlay = false;

    this.frontLeftBoundary = this.phantomFlatWidth * this.mag;
    this.leftBackBoundary = this.frontLeftBoundary + (this.phantomCurvedEdgeWidth * this.mag);
    this.backRightBoundary = this.leftBackBoundary + (this.phantomFlatWidth * this.mag);
    this.rightFrontBoundary = this.backRightBoundary + (this.phantomCurvedEdgeWidth * this.mag);

    this.minDose = 0.0;
    this.maxDose = 10.0;

    this.windowWidth = this.maxDose - this.minDose;
    this.windowLevel = this.minDose + (this.windowWidth / 2.0);
    this.minDisplayedDose = this.minDose;
    this.maxDisplayedDose = this.maxDose;
}