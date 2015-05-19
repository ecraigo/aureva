/**
 * Made for the track draggable tag editor forms on the site.
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

function toDisplay(array) {
    /* Convert nicely to element tags for unique display */
    var string = "";

    for ( i=0; i<array.length; i++ ) {

        string += '<div class="btn-group" ' +
            'id="tag' + String(i) + '">' +
            '<button type="button" class="btn btn-default btn-sm">' +
            array[i].label +
            '</button>' +
            '<button type="button" class="btn btn-default btn-sm btn-delete">' +
            '<span class="glyphicon glyphicon-remove"></span></button></div>';
    }
    return string;
}

var tagList = [];

$(document).ready( function ( e ) {
    /* For adding a new tag */
    $( '#add-tag' ).click(function( event ) {

        var label = $( '#add-tag-label' ).val();

        /* Check to see if there is text in both boxes; otherwise do nothing */
        if( label ) {

            if ( $( 'button.btn-delete' ).length < 7 ) {
                /* Update tags and then push JSON to hidden field */
                tagList.push( {label: escapeHtml( label )} );
                $( '#hidden-tags-field' ).val( JSON.stringify( tagList ) );


                /* Refresh p-list below */
                $( '#tag-list' ).html( toDisplay(tagList) );
                /* Clear the input boxes */
                $( '#add-tag-label' ).val(null);

                /* All the code and events for making these tags draggable */
                $( '#tag-list' ).sortable({
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
                        var oldIndex = parseInt( $(ui.item).attr('id').slice(3) );
                        var newIndex = $(ui.item).index();

                        /* Refresh everything again */
                        tagList.splice( newIndex, 0, tagList.splice(oldIndex, 1 )[0]);
                        $( '#tag-list' ).html( toDisplay(tagList) );
                        $( '#hidden-tags-field' ).val( JSON.stringify( tagList ) );
                    }
                });

            } else {
                alert( 'No more than 7 tags allowed at once.' );
            }

        }
    });

    /* For deleting a tag */
    $( '.container' ).on( 'click', 'button.btn-delete', function ( event ) {
        /* Get clicked ID, slice off the "tag" part in the beginning, and delete the corresponding element. */
        var arrayIndex = parseInt( $(this).parent().attr('id').slice(3) );
        tagList.splice(arrayIndex, 1);

        /* Refresh HTML display again */
        $( '#tag-list' ).html( toDisplay( tagList ) );
        $( '#hidden-tags-field' ).val( JSON.stringify( tagList ) );
    });
});