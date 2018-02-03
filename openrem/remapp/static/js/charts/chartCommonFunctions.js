/*eslint security/detect-object-injection: "off" */

function hideOrShowAllSeries(nameOfDIV, hideOrShow, buttonIDStub) {
    if (hideOrShow === "hide") {
        $($("#" + nameOfDIV).highcharts().series).each(function () {
            this.hide();
        });
    }
    else {
        $($("#" + nameOfDIV).highcharts().series).each(function () {
            this.show();
        });
    }
    $("#" + buttonIDStub + "hide").toggle();
    $("#" + buttonIDStub + "show").toggle();
}


function toggleAllSeries(nameOfDIV) {
    $($("#" + nameOfDIV).highcharts().series).each(function () {
        if (this.visible) {
            this.hide();
        } else {
            this.show();
        }
    });
}


function hideButtonsIfOneSeries(nameOfDIV, buttonIDStub) {
    if ($("#" + nameOfDIV).highcharts().series.length === 1) {
        $("#" + buttonIDStub + "hide").hide();
        $("#" + buttonIDStub + "show").hide();
        $("#" + buttonIDStub + "toggle").hide();
    }
}


function hideSeriesButtons(buttonIDStub) {
    $("#" + buttonIDStub + "hide").hide();
    $("#" + buttonIDStub + "show").hide();
    $("#" + buttonIDStub + "toggle").hide();
}


function resetSeriesButtons(buttonIDStub) {
    $("#" + buttonIDStub + "hide").show();
    $("#" + buttonIDStub + "show").hide();
    $("#" + buttonIDStub + "toggle").show();
}


function urlToArray(url) {
    var request = {};
    var pairs = url.substring(url.indexOf("?") + 1).split("&");
    for (var i = 0; i < pairs.length; i++) {
        if (!pairs[i] || pairs[i].indexOf("=") === -1) {
            continue;
        }
        var pair = pairs[i].split("=");
        pair[1] = pair[1].replace(/\+/g, " ");
        request[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
    }
    return request;
}


function arrayToURL(array) {
    var pairs = [];
    for (var key in array) {
        if (array.hasOwnProperty(key)) {
            pairs.push(encodeURIComponent(key) + "=" + encodeURIComponent(array[key]));
        }
    }
    return pairs.join("&");
}