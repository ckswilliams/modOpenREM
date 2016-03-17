var camera, scene, renderer, mesh;
var dosesFront, dosesBack, dosesLeft, dosesRight; // Need to initialise these
// at the same time as first drawing the dataTextures on the phantom.

//------------------------------------------------------------------------------
// Display the image of each phantom side on a canvas so that the pixel values
// can be obtained for use in DataTextures later on.
var imageFront = new Image();
var imageBack  = new Image();
var imageLeft  = new Image();
var imageRight = new Image();

imageFront.src = '/static/img/3-1.png';
imageBack.src  = '/static/img/1-1.png';
imageLeft.src  = '/static/img/2-1.png';
imageRight.src = '/static/img/4-1.png';

var frontData = new Uint8Array( 70*350*4);
var backData  = new Uint8Array( 70*350*4);
var leftData  = new Uint8Array(155*350*4);
var rightData = new Uint8Array(155*350*4);

var dataTextureFront = new THREE.DataTexture( frontData, 70, 350,  THREE.RGBAFormat );
var dataTextureBack  = new THREE.DataTexture( backData,  70, 350,  THREE.RGBAFormat );
var dataTextureLeft  = new THREE.DataTexture( leftData,  155, 350, THREE.RGBAFormat );
var dataTextureRight = new THREE.DataTexture( rightData, 155, 350, THREE.RGBAFormat );

dataTextureFront.needsUpdate = true;
dataTextureBack.needsUpdate = true;
dataTextureLeft.needsUpdate = true;
dataTextureRight.needsUpdate = true;

var materialFront = new THREE.MeshBasicMaterial( { map: dataTextureFront } );
var materialBack  = new THREE.MeshBasicMaterial( { map: dataTextureBack  } );
var materialLeft  = new THREE.MeshBasicMaterial( { map: dataTextureLeft  } );
var materialRight = new THREE.MeshBasicMaterial( { map: dataTextureRight } );

init(73.2, 178.6, 90*6, 70*6);

window.onload = function() {
    // Display each image in the corresponding canvas
    var example = document.getElementById('phantomFront');
    var context = example.getContext('2d');
    context.drawImage(imageFront, 0, 0);

    example = document.getElementById('phantomBack');
    context = example.getContext('2d');
    context.drawImage(imageBack, 0, 0);

    example = document.getElementById('phantomLeft');
    context = example.getContext('2d');
    context.drawImage(imageLeft, 0, 0);

    example = document.getElementById('phantomRight');
    context = example.getContext('2d');
    context.drawImage(imageRight, 0, 0);

    initialiseDataTextures();
}
// End of getting the pixel data of the four phantom images
//------------------------------------------------------------------------------


function initialiseDataTextures() {
    var example = document.getElementById('phantomFront');
    var context = example.getContext('2d');
    var tempFrontData = context.getImageData(0, 0, 70, 350).data;

    example = document.getElementById('phantomBack');
    context = example.getContext('2d');
    var tempBackData = context.getImageData(0, 0, 70, 350).data;

    example = document.getElementById('phantomLeft');
    context = example.getContext('2d');
    var tempLeftData = context.getImageData(0, 0, 155, 350).data;

    example = document.getElementById('phantomRight');
    context = example.getContext('2d');
    var tempRightData = context.getImageData(0, 0, 155, 350).data;

    for (var i = 0; i < frontData.length; i++) {
        dataTextureFront.image.data[i] = tempFrontData[i];
        dataTextureBack.image.data[i]  = tempBackData[i];
    }
    for (i = 0; i < leftData.length; i++) {
        dataTextureLeft.image.data[i]  = tempLeftData[i];
        dataTextureRight.image.data[i] = tempRightData[i];
    }
    dataTextureFront.needsUpdate = true;
    dataTextureBack.needsUpdate  = true;
    dataTextureLeft.needsUpdate  = true;
    dataTextureRight.needsUpdate = true;

    // Code here to initilise the dose value arrays - need to calculate
    // the doses from the initial pixel values. These will then be used
    // to recalculate the texture colours when using the window / level
    // controls and also for the mouse-over display of dose.
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

    var torso = refTorso * height / refHeight;
    var radius = refRadius / Math.sqrt(height / refHeight) * Math.sqrt(mass / refMass);
    var flatWidth = refWidth / refRadius * radius;

    scene = new THREE.Scene();

    // Set up the camera
    camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 10000);
    camera.position.x = torso;
    camera.position.y = 0;
    camera.position.z = 100;
    camera.lookAt( scene.position );
    scene.add(camera);

    var meshes = [], geometry, material;

    THREE.ImageUtils.crossOrigin = 'anonymous';


    /*
     var texture1 = THREE.ImageUtils.loadTexture( './images/1-1.png' );
     var material1 = new THREE.MeshBasicMaterial( { map: texture1 } );
     var texture2 = THREE.ImageUtils.loadTexture( './images/2-1.png' );
     var material2 = new THREE.MeshBasicMaterial( { map: texture2 } );
     var texture3 = THREE.ImageUtils.loadTexture( './images/3-1.png' );
     var material3 = new THREE.MeshBasicMaterial( { map: texture3 } );
     var texture4 = THREE.ImageUtils.loadTexture( './images/4-1.png' );
     var material4 = new THREE.MeshBasicMaterial( { map: texture4 } );
     */
    var endMaterial = new THREE.MeshNormalMaterial( { color: 0x7777ff } );

    /*
     // Generate random noise texture using a DataTexture
     // See http://threejs.org/docs/#Reference/Textures/DataTexture
     // This may be useful when it comes to updating the DataTexture
     // when I implement the window / levelling and different colour
     // mapping:
     // http://stackoverflow.com/questions/25108574/update-texture-map-in-threejs
     var noiseSize = 256;
     var size = noiseSize * noiseSize;
     var data = new Uint8Array( 4 * size );
     for ( var i = 0; i < size * 4; i ++ ) {
     data[ i ] = 128; //Math.random() * 255 | 0;
     }
     var dt = new THREE.DataTexture( data, noiseSize, noiseSize, THREE.RGBAFormat );
     dt.wrapS = THREE.RepeatWrapping;
     dt.wrapT = THREE.RepeatWrapping;
     dt.needsUpdate = true;
     var dataMaterial = new THREE.MeshBasicMaterial( { map: dt } );
     */
    //var materials = [materialBack, materialLeft, materialFront, materialRight, dataMaterial, dataMaterial, dataMaterial, dataMaterial, dataMaterial, dataMaterial];
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
    renderer = new THREE.WebGLRenderer({ canvas: canvas });
    renderer.setSize(90*6, 70*6);
    renderer.setClearColor( 0xffffff );

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