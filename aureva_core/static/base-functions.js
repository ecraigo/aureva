// Basic functions to improve functionality of Aureva.


function returnRest( element, check ) {
    // Fetches the rest of the name of a class that begins with the string specified by "check".
    var cls = element.attr('class').split(' ');
    var rest = '';
    for (i=0; i < cls.length; i++) {
        if (cls[i].indexOf(check) !== -1) {
            /* Get rest of class name */
            rest = cls[i].slice(check.length, cls[i].length);
        }
    }
    return rest;
}