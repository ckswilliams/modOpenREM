function sortByY(a, b) {
    return ((a.y < b.y) ? -1 : ((a.y > b.y) ? 1 : 0));
}
function sortByName(a, b) {
    // http://stackoverflow.com/questions/35289232/alphabetical-array-sort-lowercase-first
    if (!("name" in a)) {return 1;}
    if (a.name === null) {return 1;}
    if (typeof a.name[0] === "undefined") {return 1;}

    if (!("name" in b)) {return -1;}
    if (b.name === null) {return -1;}
    if (typeof b.name[0] === "undefined") {return -1;}

    if (a.name[0] === a.name[0].toLocaleLowerCase() && b.name[0] === b.name[0].toLocaleLowerCase() ||
        a.name[0] === a.name[0].toLocaleUpperCase() && b.name[0] === b.name[0].toLocaleUpperCase()) {
        return a.name.localeCompare(b.name);
    }
    if (a.name[0] === a.name[0].toLocaleLowerCase()) {
        return -1;
    }
    return 1;
}
