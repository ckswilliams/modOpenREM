function skinDoseMap3dObject(skinDoseMap3dCanvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.draw = draw;
    function draw() {
        var currentDose, scaledDose, newColour, i, j, k;
        k = 0;
        for (i = 0; i < this.phantomHeight; i++) {
            for (j = 0; j < this.phantomFlatWidth; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                dataTextureFront.image.data[k] = newColour[0];
                dataTextureFront.image.data[k+1] = newColour[1];
                dataTextureFront.image.data[k+2] = newColour[2];
                dataTextureFront.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = 0; i < this.phantomHeight; i++) {
            for (j = this.phantomFlatWidth; j < this.phantomFlatWidth+this.phantomCurvedEdgeWidth; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                dataTextureLeft.image.data[k] = newColour[0];
                dataTextureLeft.image.data[k+1] = newColour[1];
                dataTextureLeft.image.data[k+2] = newColour[2];
                dataTextureLeft.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = 0; i < this.phantomHeight; i++) {
            for (j = this.phantomFlatWidth+this.phantomCurvedEdgeWidth; j < this.phantomFlatWidth*2+this.phantomCurvedEdgeWidth; j++) {
                currentDose = this.skinDoseMap[(j * this.phantomHeight) + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                dataTextureBack.image.data[k] = newColour[0];
                dataTextureBack.image.data[k+1] = newColour[1];
                dataTextureBack.image.data[k+2] = newColour[2];
                dataTextureBack.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = 0; i < this.phantomHeight; i++) {
            for (j = this.phantomFlatWidth*2+this.phantomCurvedEdgeWidth; j < this.phantomFlatWidth*2+this.phantomCurvedEdgeWidth*2; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                dataTextureRight.image.data[k] = newColour[0];
                dataTextureRight.image.data[k+1] = newColour[1];
                dataTextureRight.image.data[k+2] = newColour[2];
                dataTextureRight.image.data[k+3] = 0;
                k += 4;
            }
        }

        dataTextureFront.needsUpdate = true;
        dataTextureBack.needsUpdate  = true;
        dataTextureLeft.needsUpdate  = true;
        dataTextureRight.needsUpdate = true;
    }


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
    function initialise(skinDoseMap, phantomFlatWidth, phantomCurvedEdgeWidth, phantomHeight, phantomCurvedRadius) {

        this.skinDoseMap = new Array(skinDoseMap.length);
        this.skinDoseMapWidth = 2*phantomFlatWidth + 2*phantomCurvedEdgeWidth;
        this.skinDoseMapHeight = phantomHeight;
        this.phantomFlatWidth = phantomFlatWidth;
        this.phantomCurvedEdgeWidth = phantomCurvedEdgeWidth;
        this.phantomHeight = phantomHeight;
        this.phantomCurvedRadius = phantomCurvedRadius;

        var x, y, offset;
        for (x = 0; x < this.skinDoseMapWidth; x++) {
            for (y = 0; y < this.skinDoseMapHeight; y++) {
                offset = this.skinDoseMapHeight * x + y;
                this.skinDoseMap[offset] = skinDoseMap[this.skinDoseMapWidth * (this.skinDoseMapHeight - 1 - y) + x];
            }
        }

        frontData = new Uint8Array(this.phantomFlatWidth*this.phantomHeight*4);
        backData  = new Uint8Array(this.phantomFlatWidth*this.phantomHeight*4);
        leftData  = new Uint8Array(this.phantomCurvedEdgeWidth*this.phantomHeight*4);
        rightData = new Uint8Array(this.phantomCurvedEdgeWidth*this.phantomHeight*4);

        dataTextureFront = new THREE.DataTexture( frontData, this.phantomFlatWidth, this.phantomHeight,  THREE.RGBAFormat );
        dataTextureBack  = new THREE.DataTexture( backData,  this.phantomFlatWidth, this.phantomHeight,  THREE.RGBAFormat );
        dataTextureLeft  = new THREE.DataTexture( leftData,  this.phantomCurvedEdgeWidth, this.phantomHeight, THREE.RGBAFormat );
        dataTextureRight = new THREE.DataTexture( rightData, this.phantomCurvedEdgeWidth, this.phantomHeight, THREE.RGBAFormat );

        dataTextureFront.needsUpdate = true;
        dataTextureBack.needsUpdate = true;
        dataTextureLeft.needsUpdate = true;
        dataTextureRight.needsUpdate = true;

        materialFront = new THREE.MeshLambertMaterial( { map: dataTextureFront } );
        materialBack  = new THREE.MeshLambertMaterial( { map: dataTextureBack  } );
        materialLeft  = new THREE.MeshLambertMaterial( { map: dataTextureLeft  } );
        materialRight = new THREE.MeshLambertMaterial( { map: dataTextureRight } );
        materialFront.map.minFilter = THREE.LinearFilter;
        materialBack.map.minFilter = THREE.LinearFilter;
        materialLeft.map.minFilter = THREE.LinearFilter;
        materialRight.map.minFilter = THREE.LinearFilter;

        var aspectRatio = this.canvas.width / this.canvas.height;

        this.scene = new THREE.Scene();

        // Set up the camera
        this.camera = new THREE.PerspectiveCamera(50, aspectRatio, 1, 10000);
        this.camera.position.x = this.phantomHeight;
        this.camera.position.y = 0;
        this.camera.position.z = 100;
        this.camera.lookAt( this.scene.position );
        this.scene.add(this.camera);

        var geometry, material;
        this.meshes = [], geometry, material;

        THREE.ImageUtils.crossOrigin = 'anonymous';

        var endMaterial = new THREE.MeshLambertMaterial( { color: 0x7092be } );
        var materials = [materialBack, materialLeft, materialFront, materialRight, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial];
        var meshFaceMaterial = new THREE.MeshFaceMaterial(materials);

        geometry = new THREE.PlaneGeometry(this.phantomFlatWidth, this.phantomHeight);
        var mesh = new THREE.Mesh(geometry);
        mesh.rotation.y = Math.PI;
        mesh.position.z = -this.phantomCurvedRadius;
        this.meshes.push(mesh);

        geometry = new THREE.CylinderGeometry(this.phantomCurvedRadius, this.phantomCurvedRadius, this.phantomHeight, 32, 1, true, 0, Math.PI );
        mesh = new THREE.Mesh(geometry);
        mesh.position.x = this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        geometry = new THREE.PlaneGeometry(this.phantomFlatWidth, this.phantomHeight);
        mesh = new THREE.Mesh(geometry);
        mesh.position.z = this.phantomCurvedRadius;
        this.meshes.push(mesh);

        geometry = new THREE.CylinderGeometry  (this.phantomCurvedRadius, this.phantomCurvedRadius, this.phantomHeight, 32, 1, true, Math.PI, Math.PI );
        mesh = new THREE.Mesh(geometry);
        mesh.position.x = -this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        geometry = new THREE.PlaneGeometry(this.phantomFlatWidth, this.phantomCurvedRadius*2);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = Math.PI / 2;
        mesh.position.y = -this.phantomHeight / 2;
        this.meshes.push(mesh);

        geometry = new THREE.PlaneGeometry(this.phantomFlatWidth, this.phantomCurvedRadius*2);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = -Math.PI / 2;
        mesh.position.y = this.phantomHeight/ 2;
        this.meshes.push(mesh);

        geometry = new THREE.CircleGeometry(this.phantomCurvedRadius, 32, Math.PI/2, Math.PI);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = -Math.PI / 2;
        mesh.position.y = this.phantomHeight / 2;
        mesh.position.x = -this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        geometry = new THREE.CircleGeometry(this.phantomCurvedRadius, 32, -Math.PI/2, Math.PI);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = -Math.PI / 2;
        mesh.position.y = this.phantomHeight / 2;
        mesh.position.x = this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        geometry = new THREE.CircleGeometry(this.phantomCurvedRadius, 32, Math.PI/2, Math.PI);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = -Math.PI / 2;
        mesh.rotation.y = Math.PI;
        mesh.position.y = -this.phantomHeight / 2;
        mesh.position.x = this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        geometry = new THREE.CircleGeometry(this.phantomCurvedRadius, 32, -Math.PI/2, Math.PI);
        mesh = new THREE.Mesh(geometry);
        mesh.rotation.x = -Math.PI / 2;
        mesh.rotation.y = Math.PI;
        mesh.position.y = -this.phantomHeight / 2;
        mesh.position.x = -this.phantomFlatWidth / 2;
        this.meshes.push(mesh);

        //merge all the geometries
        geometry = mergeMeshes(this.meshes);
        this.mesh = new THREE.Mesh(geometry, meshFaceMaterial);
        this.scene.add(this.mesh);

        // A light source is needed for the MehLambertMaterial
        var directionalLight = new THREE.DirectionalLight( 0xffffff, 1.0 );
        directionalLight.position.set( 0, 0, 1 );
        this.scene.add( directionalLight );
    }


    this.reset = reset;
    function reset() {
        this.mesh.position.set( 0, 0, 0 );
        this.mesh.rotation.set( 0, 0, 0 );
        this.mesh.scale.set( 1, 1, 1 );
        this.mesh.updateMatrix();

        this.camera.position.x = this.phantomHeight;
        this.camera.position.y = 0;
        this.camera.position.z = 100;
        this.camera.lookAt( this.scene.position );
    }


    this.animate = animate;
    function animate() {
        requestAnimationFrame(animate);
        render();
    }


    this.canvasName = skinDoseMap3dCanvasName;
    this.canvas = document.getElementById(this.canvasName);

    var colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(colourScaleName);

    this.windowWidth = 10.0;
    this.windowLevel = 5.0;

    var skinDoseMap = [];

    this.phantomHeight = 10;
    this.phantomFlatWidth = 10;
    this.phantomCurvedEdgeWidth = 10;
    this.phantomCurvedRadius = 10;

    this.skinDoseMapWidth = 10;
    this.skinDoseMapHeight = 10;

    var frontData = [];
    var backData = [];
    var leftData = [];
    var rightData = [];

    this.camera = 0;
    this.scene = 0;
    this.mesh = 0;

    var dataTextureFront = 0;
    var dataTextureBack = 0;
    var dataTextureLeft = 0;
    var dataTextureRight = 0;

    var materialFront = 0;
    var materialBack = 0;
    var materialLeft = 0;
    var materialRight = 0;
}