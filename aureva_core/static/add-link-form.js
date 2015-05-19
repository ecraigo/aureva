/**
 * Made for the user-profile draggable link editor forms on the site.
 */

/* Some moustache.js code, preventing malicious code injection in the input boxes */
var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
};

function escapeHtml(string) {
  return String(string).replace(/[&<>"']/g, function (s) {
    return entityMap[s];
  });
}
/* End moustache.js code */

function forceAbsolute(URL) {
    /* Force URLs absolute to avoid undesirable relative URL functionality */
    /* substr() returns '' if out of range, so we are still valid in those cases */

    newURL = URL.toLowerCase();

    if ( newURL.substr(0, 7) !== 'http://' && newURL.substr(0, 8) !== 'https://' ) {
        newURL = 'http://' + newURL;
    }
    return newURL;
}

function toDisplay(array) {
    /* Convert nicely to element tags for unique display */
    var string = "";

    for ( i=0; i<array.length; i++ ) {

        string += '<div class="btn-group" ' +
            'id="link' + String(i) + '">' +
            '<button type="button" class="btn btn-default btn-sm">' +
            '<a href="' + array[i].URL + '" target="_blank">' + array[i].label + '</a>' +
            '</button>' +
            '<button type="button" class="btn btn-default btn-sm btn-delete">' +
            '<span class="glyphicon glyphicon-remove"></span></button></div>';
    }
    return string;
}

var linkList = [];

$(document).ready( function ( e ) {
    /* For adding a new link */
    $( '#add-link' ).click(function( event ) {

        var label = $( '#add-link-label' ).val();
        var URL = $( '#add-link-URL' ).val();

        /* Check to see if there is text in both boxes; otherwise do nothing */
        if( label && URL ) {

            if ( $( 'button.btn-delete' ).length < 7 ) {
                /* Update links and then push JSON to hidden field */
                linkList.push( {label: escapeHtml( label ),
                              URL: escapeHtml( forceAbsolute( URL ) )} );
                $( '#hidden-links-field' ).val( JSON.stringify( linkList ) );


                /* Refresh p-list below */
                $( '#link-list' ).html( toDisplay(linkList) );
                /* Clear the input boxes */
                $( '#add-link-label' ).val(null);
                $( '#add-link-URL' ).val(null);

                /* All the code and events for making these links draggable */
                $( '#link-list' ).sortable({
                    handle: 'button',
                    containment: 'document',
                    cancel: '',
                    opacity: 0.5,
                    tolerance: 'pointer',

                    /* Custom object under cursor when dragged; temporarily remove delete tab */
                    helper: function( event, ui ) {
                        return '<div class="btn-group"><button type="button" class="btn btn-default btn-sm">' +
                            ui.text() + '</button></div>';
                    },

                    /* Re-sort list after drop. */
                    stop: function( event, ui ) {
                        var oldIndex = parseInt( $(ui.item).attr('id').slice(4) );
                        var newIndex = $(ui.item).index();

                        /* Refresh everything again */
                        linkList.splice( newIndex, 0, linkList.splice(oldIndex, 1 )[0]);
                        $( '#link-list' ).html( toDisplay(linkList) );
                        $( '#hidden-links-field' ).val( JSON.stringify( linkList ) );
                    }
                });

            } else {
                alert( 'No more than 7 links allowed at once.' );
            }

        }
    });

    /* For deleting a link */
    $( '.container' ).on( 'click', 'button.btn-delete', function ( event ) {
        /* Get clicked ID, slice off the "link" part in the beginning, and delete the corresponding element. */
        var arrayIndex = parseInt( $(this).parent().attr('id').slice(4) );
        linkList.splice(arrayIndex, 1);

        /* Refresh HTML display again */
        $( '#link-list' ).html( toDisplay(linkList) );
        $( '#hidden-links-field' ).val( JSON.stringify( linkList ) );
    });
});