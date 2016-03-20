function skinDoseMap3dObject(skinDoseMap3dCanvasName, colourScaleName) {

    this.useNewColourScale = useNewColourScale;
    function useNewColourScale(new_scale) {
        this.colourScale = chroma.scale(new_scale);
    }


    this.draw = draw;
    function draw() {
        var currentDose, scaledDose, newColour, i, j, k;
        k = 0;
        for (i = this.phantomHeight-1; i >= 0; i--) {
            for (j = 0; j < 14; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                this.dataTextureFront.image.data[k] = newColour[0];
                this.dataTextureFront.image.data[k+1] = newColour[1];
                this.dataTextureFront.image.data[k+2] = newColour[2];
                this.dataTextureFront.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = this.phantomHeight-1; i >= 0; i--) {
            for (j = 14; j < 45; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                this.dataTextureLeft.image.data[k] = newColour[0];
                this.dataTextureLeft.image.data[k+1] = newColour[1];
                this.dataTextureLeft.image.data[k+2] = newColour[2];
                this.dataTextureLeft.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = this.phantomHeight-1; i >= 0; i--) {
            for (j = 45; j < 59; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                this.dataTextureBack.image.data[k] = newColour[0];
                this.dataTextureBack.image.data[k+1] = newColour[1];
                this.dataTextureBack.image.data[k+2] = newColour[2];
                this.dataTextureBack.image.data[k+3] = 0;
                k += 4;
            }
        }
        k = 0;
        for (i = this.phantomHeight-1; i >= 0; i--) {
            for (j = 59; j < 90; j++) {
                currentDose = this.skinDoseMap[j * this.phantomHeight + i];
                scaledDose = currentDose - (this.windowLevel - (this.windowWidth / 2.0));
                if (scaledDose < 0) scaledDose = 0;
                if (scaledDose > this.windowWidth) scaledDose = this.windowWidth;
                newColour = this.colourScale(scaledDose / this.windowWidth).rgb();

                this.dataTextureRight.image.data[k] = newColour[0];
                this.dataTextureRight.image.data[k+1] = newColour[1];
                this.dataTextureRight.image.data[k+2] = newColour[2];
                this.dataTextureRight.image.data[k+3] = 0;
                k += 4;
            }
        }

        this.dataTextureFront.needsUpdate = true;
        this.dataTextureBack.needsUpdate  = true;
        this.dataTextureLeft.needsUpdate  = true;
        this.dataTextureRight.needsUpdate = true;
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

        this.skinDoseMap = skinDoseMap;
        this.phantomFlatWidth = phantomFlatWidth;
        this.phantomCurvedEdgeWidth = phantomCurvedEdgeWidth;
        this.phantomHeight = phantomHeight;
        this.phantomCurvedRadius = phantomCurvedRadius;

        this.frontData = new Uint8Array(this.phantomFlatWidth*this.phantomHeight*4);
        this.backData  = new Uint8Array(this.phantomFlatWidth*this.phantomHeight*4);
        this.leftData  = new Uint8Array(this.phantomCurvedEdgeWidth*this.phantomHeight*4);
        this.rightData = new Uint8Array(this.phantomCurvedEdgeWidth*this.phantomHeight*4);

        this.dataTextureFront = new THREE.DataTexture( this.frontData, this.phantomFlatWidth, this.phantomHeight,  THREE.RGBAFormat );
        this.dataTextureBack  = new THREE.DataTexture( this.backData,  this.phantomFlatWidth, this.phantomHeight,  THREE.RGBAFormat );
        this.dataTextureLeft  = new THREE.DataTexture( this.leftData,  this.phantomCurvedEdgeWidth, this.phantomHeight, THREE.RGBAFormat );
        this.dataTextureRight = new THREE.DataTexture( this.rightData, this.phantomCurvedEdgeWidth, this.phantomHeight, THREE.RGBAFormat );

        this.dataTextureFront.needsUpdate = true;
        this.dataTextureBack.needsUpdate = true;
        this.dataTextureLeft.needsUpdate = true;
        this.dataTextureRight.needsUpdate = true;

        this.materialFront = new THREE.MeshBasicMaterial( { map: this.dataTextureFront } );
        this.materialBack  = new THREE.MeshBasicMaterial( { map: this.dataTextureBack  } );
        this.materialLeft  = new THREE.MeshBasicMaterial( { map: this.dataTextureLeft  } );
        this.materialRight = new THREE.MeshBasicMaterial( { map: this.dataTextureRight } );
        this.materialFront.map.minFilter = THREE.LinearFilter;
        this.materialBack.map.minFilter = THREE.LinearFilter;
        this.materialLeft.map.minFilter = THREE.LinearFilter;
        this.materialRight.map.minFilter = THREE.LinearFilter;

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

        var endMaterial = new THREE.MeshNormalMaterial( { color: 0x7777ff } );
        var materials = [this.materialBack, this.materialLeft, this.materialFront, this.materialRight, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial];
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

        // Put the animation into a canvas called skinDoseMap3d
        // and resize the DIV to window.innerWidth/4, window.innerHeight/4
        //var canvas = document.getElementById( 'skinDoseMap3d' );
        //canvas.width = canvasWidth;
        //canvas.height = canvasHeight;
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas });
        this.renderer.setClearColor( 0xeeeeee );
    }


    this.animate = animate;
    function animate() {
        requestAnimationFrame(animate);
        render();
    }


    this.canvasName = skinDoseMap3dCanvasName;
    this.canvas = document.getElementById(this.canvasName);

    this.colourScaleName = colourScaleName;
    this.colourScale = chroma.scale(this.colourScaleName);

    this.mag = 6;

    this.windowWidth = 10.0;
    this.windowLevel = 5.0;

    this.skinDoseMap = [];

    this.phantomHeight = 10;
    this.phantomFlatWidth = 10;
    this.phantomCurvedEdgeWidth = 10;
    this.phantomCurvedRadius = 10;

    this.frontData = [];
    this.backData = [];
    this.leftData = [];
    this.rightData = [];

    this.camera = 0;
    this.scene = 0;
    this.renderer = 0;
    this.mesh = 0;

    this.dataTextureFront = 0;
    this.dataTextureBack = 0;
    this.dataTextureLeft = 0;
    this.dataTextureRight = 0;

    this.materialFront = 0;
    this.materialBack = 0;
    this.materialLeft = 0;
    this.materialRight = 0;
}