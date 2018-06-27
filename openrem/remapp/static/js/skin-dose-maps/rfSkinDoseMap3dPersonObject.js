/*global THREE*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */

/**
 * Function to create a 3d person object to orientate the 3d skin dose map
 */
function skinDoseMap3dPersonObject() {

    this.phantomHeight = 10;

    this.camera = 0;
    this.scene = 0;
    this.mesh = 0;


    /**
     * Internal function to merge three.js meshes together
     * @param meshes
     * @returns {THREE.Geometry}
     */
    this.mergeMeshes = function (meshes) {
        var combined = new THREE.Geometry();

        var lastFace = 0, j;

        for (var i = 0; i < meshes.length; i++) {
            meshes[i].updateMatrix();
            combined.merge(meshes[i].geometry, meshes[i].matrix);
            for(j = lastFace; j < combined.faces.length; j++) {
                combined.faces[j].materialIndex = i;
            }
            lastFace = combined.faces.length;
        }

        return combined;
    };


    /**
     * Internal function to initialise the 3d person
     * @param phantomHeight
     */
    this.initialise = function (phantomHeight) {
        var _this = this;

        _this.phantomHeight = phantomHeight;

        _this.scene = new THREE.Scene();

        // Set up the camera
        _this.camera = new THREE.PerspectiveCamera(50, 1.0, 1, 10000);
        _this.camera.position.x = phantomHeight + 0;
        _this.camera.position.y = 0;
        _this.camera.position.z = 100;
        _this.camera.lookAt( _this.scene.position );
        _this.scene.add(_this.camera);

        var meshes = [], geometry; //, material;

        THREE.ImageUtils.crossOrigin = "anonymous";

        var endMaterial = new THREE.MeshLambertMaterial( { color: 0x7092be } );

        // A light source is needed for the MeshLambertMaterial
        var directionalLight = new THREE.DirectionalLight( 0xffffff, 1.75 );
        directionalLight.position.set( 0, 0, 1 );
        _this.scene.add( directionalLight );

        var materials = [endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial];
        var meshFaceMaterial = new THREE.MeshFaceMaterial(materials);


        // A body
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var bodyRadius = 20;
        geometry = new THREE.SphereGeometry(bodyRadius, 50, 50);
        _this.mesh = new THREE.Mesh(geometry);
        meshes.push(_this.mesh);

        // A head
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var headRadius = 10;
        geometry = new THREE.SphereGeometry(headRadius, 50, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.position.y = bodyRadius+headRadius;
        meshes.push(_this.mesh);

        // A nose
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var noseRadius = 4;
        geometry = new THREE.SphereGeometry(noseRadius, 50, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.position.y = bodyRadius+headRadius;
        _this.mesh.position.z = headRadius;
        meshes.push(_this.mesh);

        // A right arm
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        var armRadiusTop = 6;
        var armRadiusBottom = 2;
        var armLength = 30;
        geometry = new THREE.CylinderGeometry(armRadiusTop, armRadiusBottom, armLength, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.rotation.x = -Math.PI / 2;
        _this.mesh.rotation.z = -Math.PI / 2;
        _this.mesh.rotation.y = Math.PI / 6;
        _this.mesh.position.x = -bodyRadius-armLength/4;
        _this.mesh.position.y = bodyRadius/1.2;
        meshes.push(_this.mesh);

        // A left arm
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        geometry = new THREE.CylinderGeometry(armRadiusTop, armRadiusBottom, armLength, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.rotation.x = -Math.PI / 2;
        _this.mesh.rotation.z = -Math.PI / 2;
        _this.mesh.rotation.y = -Math.PI - Math.PI/6;
        _this.mesh.position.x = bodyRadius+armLength/4;
        _this.mesh.position.y = bodyRadius/1.2;
        meshes.push(_this.mesh);

        // A left leg
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        var legRadiusTop = 8;
        var legRadiusBottom = 2;
        var legLength = 60;
        geometry = new THREE.CylinderGeometry(legRadiusTop, legRadiusBottom, legLength, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.position.x = bodyRadius/2.5;
        _this.mesh.position.y = -legLength/2;
        meshes.push(_this.mesh);

        // A right leg
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        geometry = new THREE.CylinderGeometry(legRadiusTop, legRadiusBottom, legLength, 50);
        _this.mesh = new THREE.Mesh(geometry);
        _this.mesh.position.x = -bodyRadius/2.5;
        _this.mesh.position.y = -legLength/2;
        meshes.push(_this.mesh);

        //merge all the geometries
        geometry = _this.mergeMeshes(meshes);
        _this.mesh = new THREE.Mesh(geometry, meshFaceMaterial);
        _this.scene.add(_this.mesh);
    };


    /**
     * Internal function to reset the 3d person
     */
    this.reset = function () {
        var _this = this;
        _this.mesh.position.set( 0, 0, 0 );
        _this.mesh.rotation.set( 0, 0, 0 );
        _this.mesh.scale.set( 1, 1, 1 );
        _this.mesh.updateMatrix();
    };
}