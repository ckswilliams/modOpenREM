var camera, scene, renderer, mesh;

var frontData = new Uint8Array(14*70*4);
var backData  = new Uint8Array(14*70*4);
var leftData  = new Uint8Array(31*70*4);
var rightData = new Uint8Array(31*70*4);

var dataTextureFront = new THREE.DataTexture( frontData, 14, 70,  THREE.RGBAFormat );
var dataTextureBack  = new THREE.DataTexture( backData,  14, 70,  THREE.RGBAFormat );
var dataTextureLeft  = new THREE.DataTexture( leftData,  31, 70, THREE.RGBAFormat );
var dataTextureRight = new THREE.DataTexture( rightData, 31, 70, THREE.RGBAFormat );

dataTextureFront.needsUpdate = true;
dataTextureBack.needsUpdate = true;
dataTextureLeft.needsUpdate = true;
dataTextureRight.needsUpdate = true;

var materialFront = new THREE.MeshBasicMaterial( { map: dataTextureFront } );
var materialBack  = new THREE.MeshBasicMaterial( { map: dataTextureBack  } );
var materialLeft  = new THREE.MeshBasicMaterial( { map: dataTextureLeft  } );
var materialRight = new THREE.MeshBasicMaterial( { map: dataTextureRight } );

init(73.2, 178.6, 90*6, 70*6);


function update3dSkinMap() {
    var currentDose, scaledDose, newColour, i, j, k;
    k = 0;
    for (i = 69; i >= 0; i--) {
        for (j = 0; j < 14; j++) {
            currentDose = skinDoseMap3dData[j * 70 + i];
            scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
            if (scaledDose < 0) scaledDose = 0;
            if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
            newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

            dataTextureFront.image.data[k] = newColour[0];
            dataTextureFront.image.data[k+1] = newColour[1];
            dataTextureFront.image.data[k+2] = newColour[2];
            dataTextureFront.image.data[k+3] = 0;
            k += 4;
        }
    }
    k = 0;
    for (i = 69; i >= 0; i--) {
        for (j = 14; j < 45; j++) {
            currentDose = skinDoseMap3dData[j * 70 + i];
            scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
            if (scaledDose < 0) scaledDose = 0;
            //if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
            newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

            dataTextureLeft.image.data[k] = newColour[0];
            dataTextureLeft.image.data[k+1] = newColour[1];
            dataTextureLeft.image.data[k+2] = newColour[2];
            dataTextureLeft.image.data[k+3] = 0;
            k += 4;
        }
    }
    k = 0;
    for (i = 69; i >= 0; i--) {
        for (j = 45; j < 59; j++) {
            currentDose = skinDoseMap3dData[j * 70 + i];
            scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
            if (scaledDose < 0) scaledDose = 0;
            //if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
            newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

            dataTextureBack.image.data[k] = newColour[0];
            dataTextureBack.image.data[k+1] = newColour[1];
            dataTextureBack.image.data[k+2] = newColour[2];
            dataTextureBack.image.data[k+3] = 0;
            k += 4;
        }
    }
    k = 0;
    for (i = 69; i >= 0; i--) {
        for (j = 59; j < 90; j++) {
            currentDose = skinDoseMap3dData[j * 70 + i];
            scaledDose = currentDose - (skinDoseMapObj.windowLevel - (skinDoseMapObj.windowWidth / 2.0));
            if (scaledDose < 0) scaledDose = 0;
            if (scaledDose > skinDoseMapObj.windowWidth) scaledDose = skinDoseMapObj.windowWidth;
            newColour = skinDoseMapObj.colourScale(scaledDose / skinDoseMapObj.windowWidth).rgb();

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


function increaseAll() {
    var endpoint = dataTextureFront.image.data.length;
    for (var i = 0; i < endpoint; i+=4) {
        dataTextureFront.image.data[i] += 10;
        dataTextureBack.image.data[i]  += 10;
        dataTextureFront.image.data[i+1] += 10;
        dataTextureBack.image.data[i+1]  += 10;
        dataTextureFront.image.data[i+2] += 10;
        dataTextureBack.image.data[i+2]  += 10;
    }

    endpoint = dataTextureLeft.image.data.length;
    for (i = 0; i < endpoint; i+=4) {
        dataTextureLeft.image.data[i]  += 10;
        dataTextureRight.image.data[i] += 10;
        dataTextureLeft.image.data[i+1]  += 10;
        dataTextureRight.image.data[i+1] += 10;
        dataTextureLeft.image.data[i+2]  += 10;
        dataTextureRight.image.data[i+2] += 10;
    }

    dataTextureFront.needsUpdate = true;
    dataTextureBack.needsUpdate  = true;
    dataTextureLeft.needsUpdate  = true;
    dataTextureRight.needsUpdate = true;
}


function decreaseAll() {
    var endpoint = dataTextureFront.image.data.length;
    for (var i = 0; i < endpoint; i+=4) {
        dataTextureFront.image.data[i] -= 10;
        dataTextureBack.image.data[i]  -= 10;
        dataTextureFront.image.data[i+1] -= 10;
        dataTextureBack.image.data[i+1]  -= 10;
        dataTextureFront.image.data[i+2] -= 10;
        dataTextureBack.image.data[i+2]  -= 10;
    }

    endpoint = dataTextureLeft.image.data.length;
    for (i = 0; i < endpoint; i+=4) {
        dataTextureLeft.image.data[i]  -= 10;
        dataTextureRight.image.data[i] -= 10;
        dataTextureLeft.image.data[i+1]  -= 10;
        dataTextureRight.image.data[i+1] -= 10;
        dataTextureLeft.image.data[i+2]  -= 10;
        dataTextureRight.image.data[i+2] -= 10;
    }

    dataTextureFront.needsUpdate = true;
    dataTextureBack.needsUpdate  = true;
    dataTextureLeft.needsUpdate  = true;
    dataTextureRight.needsUpdate = true;
}


function increaseRed() {
    var endpoint = dataTextureFront.image.data.length;
    for (var i = 0; i < endpoint; i+=4) {
        dataTextureFront.image.data[i] += 10;
        dataTextureBack.image.data[i]  += 10;
    }

    endpoint = dataTextureLeft.image.data.length;
    for (i = 0; i < endpoint; i+=4) {
        dataTextureLeft.image.data[i]  += 10;
        dataTextureRight.image.data[i] += 10;
    }

    dataTextureFront.needsUpdate = true;
    dataTextureBack.needsUpdate  = true;
    dataTextureLeft.needsUpdate  = true;
    dataTextureRight.needsUpdate = true;
}

function decreaseRed() {
    var endpoint = dataTextureFront.image.data.length
    for (var i = 0; i < endpoint; i+=4) {
        dataTextureFront.image.data[i] -= 10;
        dataTextureBack.image.data[i]  -= 10;
    }

    endpoint = dataTextureLeft.image.data.length
    for (var i = 0; i < endpoint; i+=4) {
        dataTextureLeft.image.data[i]  -= 10;
        dataTextureRight.image.data[i] -= 10;
    }

    dataTextureFront.needsUpdate = true;
    dataTextureBack.needsUpdate  = true;
    dataTextureLeft.needsUpdate  = true;
    dataTextureRight.needsUpdate = true;
}


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


function init(mass, height, canvasWidth, canvasHeight) {

    var refHeight = 178.6;
    var refMass = 73.2;
    var refTorso = 70.0;
    var refRadius = 10.0;
    var refWidth = 14.4;

    var aspectRatio = canvasWidth / canvasHeight;

    var torso = refTorso * height / refHeight;
    var radius = refRadius / Math.sqrt(height / refHeight) * Math.sqrt(mass / refMass);
    var flatWidth = refWidth / refRadius * radius;

    scene = new THREE.Scene();

    // Set up the camera
    camera = new THREE.PerspectiveCamera(50, aspectRatio, 1, 10000);
    camera.position.x = torso;
    camera.position.y = 0;
    camera.position.z = 100;
    camera.lookAt( scene.position );
    scene.add(camera);

    var meshes = [], geometry, material;

    THREE.ImageUtils.crossOrigin = 'anonymous';

    var endMaterial = new THREE.MeshNormalMaterial( { color: 0x7777ff } );
    var materials = [materialBack, materialLeft, materialFront, materialRight, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial, endMaterial];
    var meshFaceMaterial = new THREE.MeshFaceMaterial(materials);

    geometry = new THREE.PlaneGeometry(flatWidth, torso);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.y = Math.PI;
    mesh.position.z = -radius;
    meshes.push(mesh);

    geometry = new THREE.CylinderGeometry(radius, radius, torso, 32, 1, true, 0, Math.PI );
    mesh = new THREE.Mesh(geometry);
    mesh.position.x = flatWidth / 2;
    meshes.push(mesh);

    geometry = new THREE.PlaneGeometry(flatWidth, torso);
    mesh = new THREE.Mesh(geometry);
    mesh.position.z = radius;
    meshes.push(mesh);

    geometry = new THREE.CylinderGeometry  (radius, radius, torso, 32, 1, true, Math.PI, Math.PI );
    mesh = new THREE.Mesh(geometry);
    mesh.position.x = -flatWidth / 2;
    meshes.push(mesh);

    geometry = new THREE.PlaneGeometry(flatWidth, radius*2);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = Math.PI / 2;
    mesh.position.y = -torso / 2;
    meshes.push(mesh);

    geometry = new THREE.PlaneGeometry(flatWidth, radius*2);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.y = torso / 2;
    meshes.push(mesh);

    geometry = new THREE.CircleGeometry(radius, 32, Math.PI/2, Math.PI);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.y = torso / 2;
    mesh.position.x = -flatWidth / 2;
    meshes.push(mesh);

    geometry = new THREE.CircleGeometry(radius, 32, -Math.PI/2, Math.PI);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.y = torso / 2;
    mesh.position.x = flatWidth / 2;
    meshes.push(mesh);

    geometry = new THREE.CircleGeometry(radius, 32, Math.PI/2, Math.PI);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = -Math.PI / 2;
    mesh.rotation.y = Math.PI;
    mesh.position.y = -torso / 2;
    mesh.position.x = flatWidth / 2;
    meshes.push(mesh);

    geometry = new THREE.CircleGeometry(radius, 32, -Math.PI/2, Math.PI);
    mesh = new THREE.Mesh(geometry);
    mesh.rotation.x = -Math.PI / 2;
    mesh.rotation.y = Math.PI;
    mesh.position.y = -torso / 2;
    mesh.position.x = -flatWidth / 2;
    meshes.push(mesh);

    //merge all the geometries
    geometry = mergeMeshes(meshes);
    mesh = new THREE.Mesh(geometry, meshFaceMaterial);
    scene.add(mesh);

    // Put the animation into a canvas called skinDoseMap3d
    // and resize the DIV to window.innerWidth/4, window.innerHeight/4
    var canvas = document.getElementById( 'skinDoseMap3d' );
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    renderer = new THREE.WebGLRenderer({ canvas: canvas });
    renderer.setClearColor( 0xeeeeee );

    $('#skinDoseMap3d').hide();
}

function animate() {
    requestAnimationFrame(animate);
    render();
}

var isDragging3d = false;
var previousMousePosition3d = {
    x: 0,
    y: 0
};

//$(renderer.domElement).on('mousedown', function(e) {
$("#skinDoseMap3d").on('mousedown', function(e) {
    isDragging3d = true;
    })
    .on('mousemove', function(e) {
        var deltaMove = {
            x: e.offsetX-previousMousePosition3d.x,
            y: e.offsetY-previousMousePosition3d.y
        };

        if(isDragging3d) {

            var deltaRotationQuaternion = new THREE.Quaternion()
                .setFromEuler(new THREE.Euler(
                    toRadians(deltaMove.y * 1),
                    toRadians(deltaMove.x * 1),
                    0,
                    'XYZ'
                ));

            mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, mesh.quaternion);
        }

        previousMousePosition3d = {
            x: e.offsetX,
            y: e.offsetY
        };
    });

$(document).on('mouseup', function(e) {
    isDragging3d = false;
});

$("#skinDoseMap3d").on('mousewheel', function(e) {
    var d = ((typeof e.originalEvent.wheelDelta != "undefined")?(-e.originalEvent.wheelDelta):e.originalEvent.detail);
    d = 10 * ((d>0)?1:-1);

    var cPos = camera.position;
    if (isNaN(cPos.x) || isNaN(cPos.y) || isNaN(cPos.y))
        return;

    var r = cPos.x*cPos.x + cPos.y*cPos.y;
    var sqr = Math.sqrt(r);
    var sqrZ = Math.sqrt(cPos.z*cPos.z + r);

    var nx = cPos.x + ((r==0)?0   :(d * cPos.x/sqr));
    var ny = cPos.y + ((r==0)?0   :(d * cPos.y/sqr));
    var nz = cPos.z + ((sqrZ==0)?0:(d * cPos.z/sqrZ));

    if (isNaN(nx) || isNaN(ny) || isNaN(nz))
        return;

    var r_new = nx*nx + ny*ny;
    if (r_new > 100) {
        cPos.x = nx;
        cPos.y = ny;
        cPos.z = nz;
    }

    camera.lookAt( scene.position );
});

// shim layer with setTimeout fallback
window.requestAnimFrame = (function(){
    return  window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };
})();

function toRadians(angle) {
    return angle * (Math.PI / 180);
}

function toDegrees(angle) {
    return angle * (180 / Math.PI);
}

function render() {
    renderer.render(scene, camera);
    requestAnimFrame(render);
}


render();