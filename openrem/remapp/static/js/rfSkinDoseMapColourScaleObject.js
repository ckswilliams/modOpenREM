function skinDoseMapColourScaleObject(colourScaleCanvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
        this.updateColourScale();
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

        i = this.minDose;
        increment = (this.maxDose - this.minDose) / 10;
        for (y = 0; y < this.colourScaleCanvas.height; y += Math.floor((this.colourScaleCanvas.height - heightOffset) / 10)) {
            this.colourScaleContext.fillText(i.toFixed(3), 15, this.colourScaleCanvas.height - y - 7);
            i += increment;
        }
    }


    this.initialise = initialise;
    function initialise(minDose, maxDose, width, height) {
        this.colourScaleCanvas.width = width;
        this.colourScaleCanvas.height = height;

        this.minDose = minDose;
        this.maxDose = maxDose;

        this.updateColourScale();
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

    this.doseUpperLimit = 10.0;
}