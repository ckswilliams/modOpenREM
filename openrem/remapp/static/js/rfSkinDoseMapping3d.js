var isDragging3d = false;
var previousMousePosition3d = {
    x: 0,
    y: 0
};


$("#skinDoseMap3d")
    .on('mousedown', function(e) {
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

            skinDoseMap3dObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dObj.mesh.quaternion);
            skinDoseMap3dPersonObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dPersonObj.mesh.quaternion);
        }

        previousMousePosition3d = {
            x: e.offsetX,
            y: e.offsetY
        };
    })
    .on('mousewheel', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var d = ((typeof e.originalEvent.wheelDelta != "undefined")?(-e.originalEvent.wheelDelta):e.originalEvent.detail);
        d = 10 * ((d>0)?1:-1);

        var cPos = skinDoseMap3dObj.camera.position;
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

        skinDoseMap3dObj.camera.lookAt( skinDoseMap3dObj.scene.position );
    });


$(document).on('mouseup', function(e) {
    isDragging3d = false;
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
    renderer.clear();
    renderer.setViewport(0, 0, skinDoseMap3dObj.canvas.width, skinDoseMap3dObj.canvas.height);
    renderer.render(skinDoseMap3dObj.scene, skinDoseMap3dObj.camera);

    renderer.clearDepth();
    renderer.setViewport(10, 10, 75, 75);
    renderer.render(skinDoseMap3dPersonObj.scene, skinDoseMap3dPersonObj.camera);
    requestAnimFrame(render);
}


function webglAvailable() {
    try {
        var canvas = document.createElement('canvas');
        return !!( window.WebGLRenderingContext && (
            canvas.getContext('webgl') ||
            canvas.getContext('experimental-webgl') )
        );
    } catch (e) {
        return false;
    }
}


skinDoseMap3dCanvas = document.getElementById('skinDoseMap3d');
renderer = new THREE.WebGLRenderer({ canvas: skinDoseMap3dCanvas, preserveDrawingBuffer: true, antialias: true });
renderer.autoClear = false;
renderer.setClearColor( 0x000000, 0 );

var show3dSkinDoseMap = webglAvailable() ? true : false;