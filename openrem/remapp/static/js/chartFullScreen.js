chart_div_height = 0;

$(document).on('webkitfullscreenchange mozfullscreenchange fullscreenchange', function(e)
{
    if (document.webkitIsFullScreen || document.fullscreen || document.mozFullScreen || document.msFullscreenElement) {
        console.log('going to fullscreen');
        if (document.mozFullScreen) {
            chart_div_height = e.target.documentElement.clientHeight;
        }
        else {
            chart_div_height = e.target.clientHeight;
        }
        e.target.style.minHeight = "100%";
        e.target.style.width = "100%";
        setTimeout(function() {$(document).resize();}, 0);
    } else {
        console.log('returning from fullscreen');
        if (navigator.userAgent.indexOf('Mozilla') != -1 && navigator.userAgent.indexOf('Mozilla') != 0) {
            e.target.documentElement.clientHeight = chart_div_height;
        }
        else{
            e.target.clientHeight = chart_div_height;
        }
        e.target.style.minHeight = "";
        e.target.style.height = chart_div_height + 'px';
        e.target.style.width = "";
        setTimeout(function() {$(document).resize();}, 0);
    }
});

function enterFullScreen(div_id) {
    var elem = document.getElementById(div_id);
    if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    } else {
        if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else {
            elem.requestFullscreen();
        }
    }
}