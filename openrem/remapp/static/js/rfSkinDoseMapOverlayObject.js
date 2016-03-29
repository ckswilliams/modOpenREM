function skinDoseMapOverlayObject(canvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.draw = draw;
    function draw() {
        this.overlayContext.textAlign = 'center';
        this.overlayContext.font = '12pt arial';

        this.overlayContext.fillStyle = 'rgba(0, 80, 0, 0.85)';
        this.overlayContext.fillText('Superior', this.canvas.width/2, 15);
        this.overlayContext.fillText('Inferior', this.canvas.width/2, this.canvas.height-10);

        this.overlayContext.save();

        this.overlayContext.rotate(0.5*Math.PI);
        this.overlayContext.fillStyle = 'rgba(255, 0, 0, 0.85)';
        this.overlayContext.fillText('Anterior', this.canvas.height/2, -this.frontLeftBoundary/2);
        this.overlayContext.fillText('Posterior', this.canvas.height/2, -this.leftBackBoundary - (this.backRightBoundary-this.leftBackBoundary)/2);
        this.overlayContext.fillText('Left', this.canvas.height/2, -this.frontLeftBoundary - (this.leftBackBoundary-this.frontLeftBoundary)/2);
        this.overlayContext.fillText('Right', this.canvas.height/2, -this.rightFrontBoundary + (this.rightFrontBoundary-this.backRightBoundary)/2);

        this.overlayContext.restore();

        this.overlayContext.lineWidth = 1;
        this.overlayContext.setLineDash([5, 15]);
        this.overlayContext.strokeStyle = 'rgba(255, 0, 0, 0.25)';

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
        this.frontLeftBoundary = this.phantomFlatWidth * this.mag;
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

    this.frontLeftBoundary = this.phantomFlatWidth * this.mag;
    this.leftBackBoundary = this.frontLeftBoundary + (this.phantomCurvedEdgeWidth * this.mag);
    this.backRightBoundary = this.leftBackBoundary + (this.phantomFlatWidth * this.mag);
    this.rightFrontBoundary = this.backRightBoundary + (this.phantomCurvedEdgeWidth * this.mag);
}
