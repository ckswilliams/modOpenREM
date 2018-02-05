/*global THREE*/
/*eslint no-undef: "error"*/

/**
 * Function to create a 2d text overlay on top of the 3d skin dose map
 */
function skinDoseMap3dHUDObject() {

    this.camera = 0;
    this.scene = 0;
    this.mesh = 0;
    this.width = 0;
    this.height = 0;
    this.maxDoseLabel = "";
    this.phantomDimensionsLabel = "70x34x20";
    this.patientHeight = "1.79";
    this.patientMass = "73.2";
    this.patientOrientation = "HFS";
    this.patientHeightSource = "Assumed";
    this.patientMassSource = "Assumed";
    this.patientOrientationSource = "Assumed";

    this.hudCanvas = document.createElement("canvas");
    this.hudContext = this.hudCanvas.getContext("2d");
    this.hudTexture = new THREE.Texture(this.hudCanvas);
    this.hudTexture.minFilter = THREE.LinearFilter;

    /**
     * Internal function to initialise the information display
     * @param width
     * @param height
     */
    this.initialise = function (width, height) {
        var _this = this;

        _this.width = width;
        _this.height = height;

        _this.hudCanvas.width = _this.width;
        _this.hudCanvas.height = _this.height;

        _this.hudContext.font = "8pt arial";
        _this.hudContext.textAlign = "left";
        _this.hudContext.fillStyle = "rgba(255,255,255,1.0)";
        _this.hudContext.fillText("Calculated peak skin dose:", 5, 15);
        _this.hudContext.fillText("Phantom dimensions:", 5, 30);
        _this.hudContext.fillText(_this.patientHeightSource + " patient height:", 5, 45);
        _this.hudContext.fillText(_this.patientMassSource + " patient mass:", 5, 60);
        _this.hudContext.fillText(_this.patientOrientationSource + " patient orientation:", 5, 75);

        _this.hudContext.fillText(_this.phantomDimensionsLabel + " (HxWxD)", 150, 30);
        _this.hudContext.fillText(_this.patientHeight + " m", 150, 45);
        _this.hudContext.fillText(_this.patientMass + " kg", 150, 60);
        _this.hudContext.fillText(_this.patientOrientation, 150, 75);

        _this.hudContext.font = "bold 8pt arial";
        _this.hudContext.fillText(_this.maxDoseLabel + " Gy", 150, 15);

        _this.camera = new THREE.OrthographicCamera(
            -_this.width/2, _this.width/2,
            _this.height/2, -_this.height/2,
            0, 30
        );

        _this.hudTexture.needsUpdate = true;
        var material = new THREE.MeshBasicMaterial({map:_this.hudTexture});
        material.transparent = true;

        var planeGeometry = new THREE.PlaneGeometry(_this.width, _this.height);
        var plane = new THREE.Mesh(planeGeometry, material);

        _this.scene = new THREE.Scene();
        _this.scene.add(plane);
    };


    /**
     * Internal function to redraw the information - needed if user toggles full-screen viewing
     */
    this.redraw = function () {
        var _this = this;

        _this.hudCanvas.width = _this.width;
        _this.hudCanvas.height = _this.height;

        _this.hudContext.clearRect(0, 0, _this.width, _this.height);

        _this.hudContext.font = "8pt arial";
        _this.hudContext.textAlign = "left";
        _this.hudContext.fillStyle = "rgba(255,255,255,1.0)";
        _this.hudContext.fillText("Calculated peak skin dose:", 5, 15);
        _this.hudContext.fillText("Phantom dimensions:", 5, 30);
        _this.hudContext.fillText(_this.patientHeightSource + " patient height:", 5, 45);
        _this.hudContext.fillText(_this.patientMassSource + " patient mass:", 5, 60);
        _this.hudContext.fillText(_this.patientOrientationSource + " patient orientation:", 5, 75);

        _this.hudContext.fillText(_this.phantomDimensionsLabel + " (HxWxD)", 150, 30);
        _this.hudContext.fillText(_this.patientHeight + " m", 150, 45);
        _this.hudContext.fillText(_this.patientMass + " kg", 150, 60);
        _this.hudContext.fillText(_this.patientOrientation, 150, 75);

        _this.hudContext.font = "bold 8pt arial";
        _this.hudContext.fillText(_this.maxDoseLabel + " Gy", 150, 15);

        _this.hudTexture.needsUpdate = true;
    };
}