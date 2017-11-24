/*global chroma*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */

/**
 * Function to create a skin dose map colour scale object
 * @param colourScaleCanvasName
 * @param colourScaleName
 */
function skinDoseMapColourScaleObject(colourScaleCanvasName, colourScaleName) {

    this.colourScaleCanvasName = colourScaleCanvasName;
    this.colourScaleCanvas = document.getElementById(this.colourScaleCanvasName);
    this.colourScaleContext = this.colourScaleCanvas.getContext("2d");

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.colourScaleCanvas.width = 10;
    this.colourScaleCanvas.height = 10;

    this.minDose = 0.0;
    this.maxDose = 10.0;

    this.decimalPlaces = 3;


    /**
     * Internal function to use a new colour scale
     * @param newScale
     */
    this.useNewColourScale = function (newScale) {
        var _this = this;
        _this.colourScale = chroma.scale(newScale);
    };


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
    this.setPixel = function (imageData, x, y, r, g, b, a) {
        var index = (x + y * imageData.width) * 4;
        imageData.data[index   ] = r;
        imageData.data[index + 1] = g;
        imageData.data[index + 2] = b;
        imageData.data[index + 3] = a;
    };


    /**
     * Internal function to resize the colour scale
     * @param newWidth
     * @param newHeight
     */
    this.resizeColourScale = function (newWidth, newHeight) {
        var _this = this;
        _this.colourScaleCanvas.width = newWidth;
        _this.colourScaleCanvas.height = newHeight;
    };


    /**
     * Internal function to draw the colour scale
     */
    this.draw = function () {
        var _this = this;
        var x, y, i, increment, fraction, heightOffset, scaleHeight, colour;

        _this.colourScaleContext.clearRect(0, 0, _this.colourScaleCanvas.width, _this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = _this.colourScaleCanvas.height - heightOffset;

        var imageData = _this.colourScaleContext.getImageData(0, heightOffset / 2, _this.colourScaleCanvas.width, scaleHeight);

        for (y = 0; y < scaleHeight; y++) {
            for (x = 0; x < 15; x++) {
                fraction = y / scaleHeight;
                colour = _this.colourScale(1.0 - fraction).rgb();
                _this.setPixel(imageData, x, y, colour[0], colour[1], colour[2], 255);
            }
        }

        for (i = 0; i < 11; i++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            for (x = 15; x < 20; x++) {
                _this.setPixel(imageData, x, y, 0, 0, 0, 255);
            }
        }
        y = scaleHeight - 1;
        for (x = 15; x < 20; x++) {
            _this.setPixel(imageData, x, y, 0, 0, 0, 255);
        }
        _this.colourScaleContext.putImageData(imageData, 0, heightOffset / 2);

        _this.colourScaleContext.textBaseline = "middle";
        var dose = _this.minDose;
        increment = (_this.maxDose - _this.minDose) / 10;
        for (i = 0; i < 11; i ++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            _this.colourScaleContext.fillText(dose.toFixed(_this.decimalPlaces), 23, y+(heightOffset / 2));
            dose += increment;
        }
    };


    /**
     * Internal function to redraw the values on the colour scale
     */
    this.redrawValues = function () {
        var _this = this;
        var y, i, increment, heightOffset, scaleHeight;

        _this.colourScaleContext.clearRect(23, 0, 50, _this.colourScaleCanvas.height);

        heightOffset = 20;
        scaleHeight = _this.colourScaleCanvas.height - heightOffset;

        //var imageData = _this.colourScaleContext.getImageData(0, heightOffset / 2, _this.colourScaleCanvas.width, scaleHeight);

        var dose = _this.minDose;
        increment = (_this.maxDose - _this.minDose) / 10;
        for (i = 0; i < 11; i ++) {
            y = scaleHeight - Math.floor(i * scaleHeight / 10);
            _this.colourScaleContext.fillText(dose.toFixed(_this.decimalPlaces), 23, y+(heightOffset / 2));
            dose += increment;
        }
    };


    /**
     * Internal function to initialise the colour scale
     * @param minDose
     * @param maxDose
     * @param width
     * @param height
     * @param decimalPlaces
     */
    this.initialise = function (minDose, maxDose, width, height, decimalPlaces) {
        var _this = this;
        _this.decimalPlaces = decimalPlaces;
        _this.resizeColourScale(width, height);

        _this.minDose = minDose;
        _this.maxDose = maxDose;
    };
}