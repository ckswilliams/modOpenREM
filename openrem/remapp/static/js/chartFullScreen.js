function enterFullScreen(div_id) {
    $('#'+div_id).toggleClass('fullscreen');
    setTimeout(function() {$(document).resize();}, 0);
}