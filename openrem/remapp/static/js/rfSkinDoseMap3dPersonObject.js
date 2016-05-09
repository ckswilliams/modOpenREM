function skinDoseMap3dPersonObject() {

    this.mergeMeshes = mergeMeshes;
    function mergeMeshes (meshes) {
        var combined = new THREE.Geometry();

        var last_face = 0, j;

        for (var i = 0; i < meshes.length; i++) {
            meshes[i].updateMatrix();
            combined.merge(meshes[i].geometry, meshes[i].matrix);
            for(j = last_face; j < combined.faces.length; j++) {
                combined.faces[j].materialIndex = i;
            }
            last_face = combined.faces.length;
        }

        return combined;
    }


    this.initialise = initialise;
    function initialise(phantomHeight) {

        this.phantomHeight = phantomHeight;

        this.scene = new THREE.Scene();

        // Set up the camera
        this.camera = new THREE.PerspectiveCamera(50, 1.0, 1, 10000);
        this.camera.position.x = this.phantomHeight;
        this.camera.position.y = 0;
        this.camera.position.z = 100;
        this.camera.lookAt( this.scene.position );
        this.scene.add(this.camera);

        var meshes = [], geometry, material;

        THREE.ImageUtils.crossOrigin = 'anonymous';

        var endMaterial = new THREE.MeshLambertMaterial( { color: 0x7092be } );

        // A light source is needed for the MehLambertMaterial
        var directionalLight = new THREE.DirectionalLight( 0xffffff, 1.75 );
        directionalLight.position.set( 0, 0, 1 );
        this.scene.add( directionalLight );

        var materials = [endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial];
        var meshFaceMaterial = new THREE.MeshFaceMaterial(materials);


        // A body
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var bodyRadius = 20;
        geometry = new THREE.SphereGeometry(bodyRadius, 50, 50);
        this.mesh = new THREE.Mesh(geometry);
        meshes.push(this.mesh);

        // A head
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var headRadius = 10;
        geometry = new THREE.SphereGeometry(headRadius, 50, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.position.y = bodyRadius+headRadius;
        meshes.push(this.mesh);

        // A nose
        // SphereGeometry(radius, widthSegments, heightSegments, phiStart, phiLength, thetaStart, thetaLength)
        var noseRadius = 4;
        geometry = new THREE.SphereGeometry(noseRadius, 50, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.position.y = bodyRadius+headRadius;
        this.mesh.position.z = headRadius;
        meshes.push(this.mesh);

        // A right arm
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        var armRadiusTop = 6;
        var armRadiusBottom = 2;
        var armLength = 30;
        geometry = new THREE.CylinderGeometry(armRadiusTop, armRadiusBottom, armLength, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.rotation.x = -Math.PI / 2;
        this.mesh.rotation.z = -Math.PI / 2;
        this.mesh.rotation.y = Math.PI / 6;
        this.mesh.position.x = -bodyRadius-armLength/4;
        this.mesh.position.y = bodyRadius/1.2;
        meshes.push(this.mesh);

        // A left arm
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        geometry = new THREE.CylinderGeometry(armRadiusTop, armRadiusBottom, armLength, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.rotation.x = -Math.PI / 2;
        this.mesh.rotation.z = -Math.PI / 2;
        this.mesh.rotation.y = -Math.PI - Math.PI/6;
        this.mesh.position.x = bodyRadius+armLength/4;
        this.mesh.position.y = bodyRadius/1.2;
        meshes.push(this.mesh);

        // A left leg
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        var legRadiusTop = 8;
        var legRadiusBottom = 2;
        var legLength = 60;
        geometry = new THREE.CylinderGeometry(legRadiusTop, legRadiusBottom, legLength, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.position.x = bodyRadius/2.5;
        this.mesh.position.y = -legLength/2;
        meshes.push(this.mesh);

        // A right leg
        // CylinderGeometry(radiusTop, radiusBottom, height, radiusSegments, heightSegments, openEnded, thetaStart, thetaLength)
        geometry = new THREE.CylinderGeometry(legRadiusTop, legRadiusBottom, legLength, 50);
        this.mesh = new THREE.Mesh(geometry);
        this.mesh.position.x = -bodyRadius/2.5;
        this.mesh.position.y = -legLength/2;
        meshes.push(this.mesh);

        //merge all the geometries
        geometry = this.mergeMeshes(meshes);
        this.mesh = new THREE.Mesh(geometry, meshFaceMaterial);
        this.scene.add(this.mesh);
    }


    this.reset = reset;
    function reset() {
        this.mesh.position.set( 0, 0, 0 );
        this.mesh.rotation.set( 0, 0, 0 );
        this.mesh.scale.set( 1, 1, 1 );
        this.mesh.updateMatrix();
    }


    this.phantomHeight = 10;

    this.camera = 0;
    this.scene = 0;
    this.mesh = 0;
}