function sort_by_y(a,b) {
    return ((a.y < b.y) ? -1 : ((a.y > b.y) ? 1 : 0));
}
function sort_by_name(a,b) {
    // http://stackoverflow.com/questions/35289232/alphabetical-array-sort-lowercase-first
    if (a.name[0] === a.name[0].toLocaleLowerCase() && b.name[0] === b.name[0].toLocaleLowerCase() ||
        a.name[0] === a.name[0].toLocaleUpperCase() && b.name[0] === b.name[0].toLocaleUpperCase()) {
        return a.name.localeCompare(b.name);
    }
    if (a.name[0] === a.name[0].toLocaleLowerCase()) {
        return -1;
    }
    return 1;
}