/*global skinDoseMap3dPersonObj, skinDoseMap3dObj, skinDoseMap3dHUDObj, THREE, requestAnimFrame*/
/*eslint no-undef: "error"*/
/*eslint security/detect-object-injection: "off" */

/**
 * Function to convert an angle in degrees into radians
 * @param angle
 * @returns {number}
 */
function toRadians(angle) {
    return angle * (Math.PI / 180);
}


/**
 * Function to convert an angle in radians to degrees
 * @param angle
 * @returns {number}
 */
function toDegrees(angle) {
    return angle * (180 / Math.PI);
}


var isDragging3d = false;
var firstMouseMove = true;
var previousMousePosition3d = {
    x: 0,
    y: 0
};


var ongoingTouches = [];

function copyTouch(touch) {
  return { identifier: touch.identifier, pageX: touch.pageX, pageY: touch.pageY, clientX: touch.clientX, clientY: touch.clientY };
}

function ongoingTouchIndexById(idToFind) {
  for (var i = 0; i < ongoingTouches.length; i++) {
    var id = ongoingTouches[i].identifier;

    if (id === idToFind) {
      return i;
    }
  }
  return -1;    // not found
}

function zoom3dMap(d) {
    var cPos = skinDoseMap3dObj.camera.position;
    if (isNaN(cPos.x) || isNaN(cPos.y) || isNaN(cPos.y)) {return;}

    var r = cPos.x * cPos.x + cPos.y * cPos.y;
    var sqr = Math.sqrt(r);
    var sqrZ = Math.sqrt(cPos.z * cPos.z + r);

    var nx = cPos.x + ((r === 0) ? 0 : (d * cPos.x / sqr));
    var ny = cPos.y + ((r === 0) ? 0 : (d * cPos.y / sqr));
    var nz = cPos.z + ((sqrZ === 0) ? 0 : (d * cPos.z / sqrZ));

    if (isNaN(nx) || isNaN(ny) || isNaN(nz)) {return;}

    var rNew = nx * nx + ny * ny;
    if (rNew > 100) {
        cPos.x = nx;
        cPos.y = ny;
        cPos.z = nz;
    }

    skinDoseMap3dObj.camera.lookAt(skinDoseMap3dObj.scene.position);
}

var skinDoseMap3dElement = $("#skinDoseMap3d");

// jQuery mouse event handlers for the DIV that contains the 3D skin dose map
skinDoseMap3dElement
    .on("mousedown", function() {
        isDragging3d = true;
    })
    .on("mousemove", function(e) {
        var deltaMove;
        if (firstMouseMove === true) {
            deltaMove = {
                x: 0,
                y: 0
            };
            firstMouseMove = false;
        }
        else {
            deltaMove = {
                x: e.offsetX - previousMousePosition3d.x,
                y: e.offsetY - previousMousePosition3d.y
            };
        }

        if(isDragging3d) {

            var deltaRotationQuaternion = new THREE.Quaternion()
                .setFromEuler(new THREE.Euler(
                    toRadians(deltaMove.y * 1),
                    toRadians(deltaMove.x * 1),
                    0,
                    "XYZ"
                ));

            skinDoseMap3dObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dObj.mesh.quaternion);
            skinDoseMap3dPersonObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dPersonObj.mesh.quaternion);
        }

        previousMousePosition3d = {
            x: e.offsetX,
            y: e.offsetY
        };
    })
    .on("touchstart", function(e) {
        isDragging3d = true;

        var changedTouches = e.originalEvent.changedTouches;
        for (var i = 0; i < changedTouches.length; i++) {
            ongoingTouches.push(copyTouch(changedTouches[i]));
        }
    })
    .on("touchmove", function(e) {
        e.preventDefault();

        // If one pointer is down rotate the object based on the movement
        if (ongoingTouches.length === 1) {

            var touches = e.originalEvent.changedTouches;
            var deltaMove;

            if (firstMouseMove === true) {
                deltaMove = {
                    x: 0,
                    y: 0
                };
                firstMouseMove = false;
            }
            else {
                deltaMove = {
                    x: touches[0].pageX - previousMousePosition3d.x,
                    y: touches[0].pageY - previousMousePosition3d.y
                };
            }

            for (var i = 0; i < touches.length; i++) {
                var idx = ongoingTouchIndexById(touches[i].identifier);

                if (idx >= 0) {
                    ongoingTouches.splice(idx, 1, copyTouch(touches[i]));  // swap in the new touch record

                    if (isDragging3d) {
                        var deltaRotationQuaternion = new THREE.Quaternion()
                            .setFromEuler(new THREE.Euler(
                                toRadians(deltaMove.y * 1),
                                toRadians(deltaMove.x * 1),
                                0,
                                "XYZ"
                            ));
                        skinDoseMap3dObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dObj.mesh.quaternion);
                        skinDoseMap3dPersonObj.mesh.quaternion.multiplyQuaternions(deltaRotationQuaternion, skinDoseMap3dPersonObj.mesh.quaternion);
                    }

                    previousMousePosition3d = {
                        x: touches[i].pageX,
                        y: touches[i].pageY
                    };
                }
            }
        }
    })
    .on("touchend", function(e) {
        isDragging3d = false;

        var touches = e.originalEvent.changedTouches;
        for (var i = 0; i < touches.length; i++) {
            var idx = ongoingTouchIndexById(touches[i].identifier);
            if (idx >= 0) {
                ongoingTouches.splice(idx, 1);  // remove it; we're done
            }
        }
    })
    .on("mousewheel", function(e) {
        e.preventDefault();
        e.stopPropagation();

        var d = ((typeof e.originalEvent.wheelDelta !== "undefined")?(-e.originalEvent.wheelDelta):e.originalEvent.detail);
        d = 10 * ((d>0)?1:-1);

        zoom3dMap(d);
    });


$(document)
    .on("mouseup touchend", function () {
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


var skinDoseMap3dCanvas = skinDoseMap3dElement[0]; // The first element is the HTML DOM Object
var renderer = new THREE.WebGLRenderer({ canvas: skinDoseMap3dCanvas, preserveDrawingBuffer: true, antialias: true });
renderer.autoClear = false;
renderer.setClearColor( 0x000000, 0 );


/**
 * Function to render the 3D scene
 */
function render() {
    renderer.clear();
    renderer.setViewport(0, 0, skinDoseMap3dObj.canvas.width, skinDoseMap3dObj.canvas.height);
    renderer.render(skinDoseMap3dObj.scene, skinDoseMap3dObj.camera);

    renderer.clearDepth();
    renderer.setViewport(0, 0, skinDoseMap3dObj.canvas.width, skinDoseMap3dObj.canvas.height);
    renderer.render(skinDoseMap3dHUDObj.scene, skinDoseMap3dHUDObj.camera);

    renderer.clearDepth();
    renderer.setViewport(10, 10, 75, 75);
    renderer.render(skinDoseMap3dPersonObj.scene, skinDoseMap3dPersonObj.camera);

    requestAnimFrame(render);
}


/**
 * Function to check whether the browser can support WebGL
 * @returns {boolean}
 */
function webglAvailable() {
    try {
        var canvas = document.createElement("canvas");
        return !!( window.WebGLRenderingContext && (
            canvas.getContext("webgl") ||
            canvas.getContext("experimental-webgl") )
        );
    } catch (e) {
        return false;
    }
}


// http://stackoverflow.com/questions/29312123/how-does-the-double-exclamation-work-in-javascript
var show3dSkinDoseMap = !!webglAvailable();