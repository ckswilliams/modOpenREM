var isDragging3d = false;
var previousMousePosition3d = {
    x: 0,
    y: 0
};


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

            skinDoseMap3dObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dObj.mesh.quaternion);
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
    skinDoseMap3dObj.renderer.render(skinDoseMap3dObj.scene, skinDoseMap3dObj.camera);
    requestAnimFrame(render);
}