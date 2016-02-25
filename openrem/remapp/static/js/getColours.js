function getColours(noOfColours, numerator) {
    var colours = [];
    var r, g, b, colour;
    var frequency = numerator / noOfColours;
    for (var i = 0; i < noOfColours;++i) {
        if (noOfColours > 24) {
            r = Math.sin(frequency * i * 2 + 0) * (127) + 127;
            g = Math.sin(frequency * i * 2 + 1) * (127) + 127;
            b = Math.sin(frequency * i * 2 + 3) * (127) + 127;
        } else {
            r = Math.sin(frequency * i  + 0) * (127) + 127;
            g = Math.sin(frequency * i  + 1) * (127) + 127;
            b = Math.sin(frequency * i  + 3) * (127) + 127;
        }
        colour = 'rgb({r},{g},{b})';
        colour = colour.replace("{r}", Math.floor(r));
        colour = colour.replace("{g}", Math.floor(g));
        colour = colour.replace("{b}", Math.floor(b));
        colours.push(colour);
    }
    return colours;
}

function getColoursOld(noOfColours) {
    var colours = [];
    frequency = 5 / noOfColours;
    for (var i = 0; i < noOfColours;++i) {
        if (noOfColours > 24) {
            r = Math.sin(frequency * i * 2 + 0) * (127) + 128;
            g = Math.sin(frequency * i * 2 + 1) * (127) + 128;
            b = Math.sin(frequency * i * 2 + 3) * (127) + 128;
        } else {
            r = Math.sin(frequency * i  + 0) * (127) + 128;
            g = Math.sin(frequency * i  + 1) * (127) + 128;
            b = Math.sin(frequency * i  + 3) * (127) + 128;
        }
        colour = 'rgb({r},{g},{b})';
        colour = colour.replace("{r}", Math.floor(r));
        colour = colour.replace("{g}", Math.floor(g));
        colour = colour.replace("{b}", Math.floor(b));
        colours.push(colour);
    }
    return colours;
}