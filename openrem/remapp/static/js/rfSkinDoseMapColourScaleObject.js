function skinDoseMapColourScaleObject(colourScaleCanvasName, colourScaleName) {

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


    this.resizeColourScale = resizeColourScale;
    function resizeColourScale(newWidth, newHeight) {
        this.colourScaleCanvas.width = newWidth;
        this.colourScaleCanvas.height = newHeight;
    }


    this.draw = draw;
    function draw() {
        var x, y, i, increment, fraction, heightOffset, scaleHeight, colour;

        this.colourScaleContext.clearRect(0, 0, this.colourScaleCanvas.width, this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = this.colourScaleCanvas.height - heightOffset;

        var imageData = this.colourScaleContext.getImageData(0, heightOffset / 2, this.colourScaleCanvas.width, scaleHeight);

        for (y = 0; y < scaleHeight; y++) {
            for (x = 55; x < 70; x++) {
                fraction = y / scaleHeight;
                colour = this.colourScale(1.0 - fraction).rgb();
                this.setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
            }
        }

        i = 0;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor(scaleHeight / 10)) {
            for (x = 50; x < 55; x++) {
                this.setPixel(imageData, x, y, 0, 0, 0, 255);
            }
        }
        for (x = 50; x < 55; x++) {
            this.setPixel(imageData, x, scaleHeight - 1, 0, 0, 0, 255);
        }
        this.colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

        i = this.minDose;
        increment = (this.maxDose - this.minDose) / 10;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor(scaleHeight / 10)) {
            this.colourScaleContext.fillText(i.toFixed(3), 15, this.colourScaleCanvas.height - y - 7);
            i += increment;
        }
    }


    this.redrawValues = redrawValues;
    function redrawValues() {
        var y, i, increment, heightOffset, scaleHeight;

        this.colourScaleContext.clearRect(0, 0, 50, this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = this.colourScaleCanvas.height - heightOffset;

        var imageData = this.colourScaleContext.getImageData(0, heightOffset / 2, this.colourScaleCanvas.width, scaleHeight);

        i = this.minDose;
        increment = (this.maxDose - this.minDose) / 10;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor(scaleHeight / 10)) {
            this.colourScaleContext.fillText(i.toFixed(3), 15, this.colourScaleCanvas.height - y - 7);
            i += increment;
        }
    }


    this.initialise = initialise;
    function initialise(minDose, maxDose, width, height) {
        this.resizeColourScale(width, height);

        this.minDose = minDose;
        this.maxDose = maxDose;
    }

    this.colourScaleCanvasName = colourScaleCanvasName;
    this.colourScaleCanvas = document.getElementById(this.colourScaleCanvasName);
    this.colourScaleContext = this.colourScaleCanvas.getContext('2d');

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.colourScaleCanvas.width = 10;
    this.colourScaleCanvas.height = 10;

    this.minDose = 0.0;
    this.maxDose = 10.0;
}