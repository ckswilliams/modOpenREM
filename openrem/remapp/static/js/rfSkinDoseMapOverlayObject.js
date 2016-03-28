function skinDoseMapOverlayObject(canvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.draw = draw;
    function draw() {
        this.overlayContext.textAlign = 'center';

        this.overlayContext.fillStyle = 'Green';
        this.overlayContext.fillText('Superior', this.canvas.width/2, 15);
        this.overlayContext.fillText('Inferior', this.canvas.width/2, this.canvas.height-10);

        this.overlayContext.fillStyle = 'Red';
        this.overlayContext.fillText('Anterior', this.frontLeftBoundary/2, this.canvas.height/2);
        this.overlayContext.fillText('Anterior', this.canvas.width-this.frontLeftBoundary/2, this.canvas.height/2);
        this.overlayContext.fillText('Posterior', this.canvas.width/2, this.canvas.height/2);
        this.overlayContext.fillText('Left', this.frontLeftBoundary + (this.leftBackBoundary-this.frontLeftBoundary)/2, this.canvas.height/2);
        this.overlayContext.fillText('Right', this.rightFrontBoundary - (this.rightFrontBoundary-this.backRightBoundary)/2, this.canvas.height/2);

        this.overlayContext.lineWidth = 1;
        this.overlayContext.setLineDash([5, 15]);
        this.overlayContext.strokeStyle = 'Red';

        this.overlayContext.beginPath();
        this.overlayContext.moveTo(this.frontLeftBoundary, 0);
        this.overlayContext.lineTo(this.frontLeftBoundary, this.canvas.height-1);
        this.overlayContext.stroke();

        this.overlayContext.beginPath();
        this.overlayContext.moveTo(this.leftBackBoundary, 0);
        this.overlayContext.lineTo(this.leftBackBoundary, this.canvas.height-1);
        this.overlayContext.stroke();

        this.overlayContext.beginPath();
        this.overlayContext.moveTo(this.backRightBoundary, 0);
        this.overlayContext.lineTo(this.backRightBoundary, this.canvas.height-1);
        this.overlayContext.stroke();

        this.overlayContext.beginPath();
        this.overlayContext.moveTo(this.rightFrontBoundary, 0);
        this.overlayContext.lineTo(this.rightFrontBoundary, this.canvas.height-1);
        this.overlayContext.stroke();
    }


    this.initialise = initialise;
    function initialise(skinMapCanvasWidth, skinMapCanvasHeight, phantomFlatWidth, phantomCurvedEdgeWidth, phantomHeight) {
        this.phantomHeight = phantomHeight;
        this.phantomFlatWidth = phantomFlatWidth;
        this.phantomCurvedEdgeWidth = phantomCurvedEdgeWidth;

        this.canvas.width = skinMapCanvasWidth;
        this.canvas.height = skinMapCanvasHeight;
        updateBoundaries();
    }


    function updateBoundaries () {
        this.frontLeftBoundary = this.phantomFlatWidth/2 * this.mag;
        this.leftBackBoundary = this.frontLeftBoundary + (this.phantomCurvedEdgeWidth * this.mag);
        this.backRightBoundary = this.leftBackBoundary + (this.phantomFlatWidth * this.mag);
        this.rightFrontBoundary = this.backRightBoundary + (this.phantomCurvedEdgeWidth * this.mag);
    }


    this.canvasName = canvasName;
    this.canvas = document.getElementById(this.canvasName);
    this.overlayContext = this.canvas.getContext('2d');

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.mag = 6;

    this.phantomHeight = 70;
    this.phantomFlatWidth = 14;
    this.phantomCurvedEdgeWidth = 31;

    this.frontLeftBoundary = this.phantomFlatWidth/2 * this.mag;
    this.leftBackBoundary = this.frontLeftBoundary + (this.phantomCurvedEdgeWidth * this.mag);
    this.backRightBoundary = this.leftBackBoundary + (this.phantomFlatWidth * this.mag);
    this.rightFrontBoundary = this.backRightBoundary + (this.phantomCurvedEdgeWidth * this.mag);
}