/**
 * Function to create a skin dose map colour scale object
 * @param colourScaleCanvasName
 * @param colourScaleName
 */
function skinDoseMapColourScaleObject(colourScaleCanvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    /**
     * Internal function to use a new colour scale
     * @param new_scale
     */
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.setPixel = setPixel;
    /**
     * Internal function to update an rgba pixel value
     * @param imageData
     * @param x
     * @param y
     * @param r
     * @param g
     * @param b
     * @param a
     */
    function setPixel(imageData, x, y, r, g, b, a) {
        var index = (x + y * imageData.width) * 4;
        imageData.data[index + 0] = r;
        imageData.data[index + 1] = g;
        imageData.data[index + 2] = b;
        imageData.data[index + 3] = a;
    }


    this.resizeColourScale = resizeColourScale;
    /**
     * Internal function to resize the colour scale
     * @param newWidth
     * @param newHeight
     */
    function resizeColourScale(newWidth, newHeight) {
        this.colourScaleCanvas.width = newWidth;
        this.colourScaleCanvas.height = newHeight;
    }


    this.draw = draw;
    /**
     * Internal function to draw the colour scale
     */
    function draw() {
        var x, y, i, increment, fraction, heightOffset, scaleHeight, colour;

        this.colourScaleContext.clearRect(0, 0, this.colourScaleCanvas.width, this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = this.colourScaleCanvas.height - heightOffset;

        var imageData = this.colourScaleContext.getImageData(0, heightOffset / 2, this.colourScaleCanvas.width, scaleHeight);

        for (y = 0; y < scaleHeight; y++) {
            for (x = 0; x < 15; x++) {
                fraction = y / scaleHeight;
                colour = this.colourScale(1.0 - fraction).rgb();
                this.setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
            }
        }

        for (i = 0; i < 11; i++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            for (x = 15; x < 20; x++) {
                this.setPixel(imageData, x, y, 0, 0, 0, 255);
            }
        }
        y = scaleHeight - 1;
        for (x = 15; x < 20; x++) {
            this.setPixel(imageData, x, y, 0, 0, 0, 255);
        }
        this.colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

        this.colourScaleContext.textBaseline = 'middle';
        var dose = this.minDose;
        increment = (this.maxDose - this.minDose) / 10;
        for (i = 0; i < 11; i ++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            this.colourScaleContext.fillText(dose.toFixed(this.decimalPlaces), 23, y+(heightOffset / 2));
            dose += increment;
        }
    }


    this.redrawValues = redrawValues;
    /**
     * Internal function to redraw the values on the colour scale
     */
    function redrawValues() {
        var y, i, increment, heightOffset, scaleHeight;

        this.colourScaleContext.clearRect(23, 0, 50, this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = this.colourScaleCanvas.height - heightOffset;

        var imageData = this.colourScaleContext.getImageData(0, heightOffset / 2, this.colourScaleCanvas.width, scaleHeight);

        var dose = this.minDose;
        increment = (this.maxDose - this.minDose) / 10;
        for (i = 0; i < 11; i ++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            this.colourScaleContext.fillText(dose.toFixed(this.decimalPlaces), 23, y+(heightOffset / 2));
            dose += increment;
        }
    }


    this.initialise = initialise;
    /**
     * Internal function to initialise the colour scale
     * @param minDose
     * @param maxDose
     * @param width
     * @param height
     * @param decimalPlaces
     */
    function initialise(minDose, maxDose, width, height, decimalPlaces) {
        this.decimalPlaces = decimalPlaces;
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
    
    this.decimalPlaces = 3;
}