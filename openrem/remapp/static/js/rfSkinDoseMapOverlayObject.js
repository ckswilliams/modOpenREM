function skinDoseMapOverlayObject(canvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.draw = draw;
    function draw() {
        this.overlayContext.fillStyle = this.colourScale(0.5).hex();
        this.overlayContext.fillText('Superior', this.canvas.width/2, 15);
        this.overlayContext.fillText('Inferior', this.canvas.width/2, this.canvas.height-10);
        this.overlayContext.fillText('Anterior', 15, this.canvas.height/2);
        this.overlayContext.fillText('Anterior', this.canvas.width-45, this.canvas.height/2);
        this.overlayContext.fillText('Posterior', this.canvas.width/2, this.canvas.height/2);
    }


    this.initialise = initialise;
    function initialise(skinMapCanvasWidth, skinMapCanvasHeight) {
        this.canvas.width = skinMapCanvasWidth;
        this.canvas.height = skinMapCanvasHeight;
    }


    this.canvasName = canvasName;
    this.canvas = document.getElementById(this.canvasName);
    this.overlayContext = this.canvas.getContext('2d');

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);
}