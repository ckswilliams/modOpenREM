$(document).ready(function(){

    $('#qr-go').click(function ( event ){
        event.preventDefault();

        $.ajax({
            url: "/openrem/admin/dicomstore/ajax_test2",
            data: {
                qr_id: 1
            },
            type: "POST",
            dataType: "json",
            success: function( json ) {
                query_progress( json );
            },
            error: function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem starting the job!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
            },
            //complete: function( xhr, status ) {
            //    alert( "The request is complete!" );
            //}
        });
    });
    // Submit post on submit
    var form = $('form#post-form');
    form.submit(function(event) {
        event.preventDefault();
        console.log('ajax form submission function called successfully.');
        form = $(this);
        console.log(form)
        var serialized_form = form.serialize();
        $.ajax({ type: "POST",
            url: $(this).attr('action'),
            data: serialized_form,
            dataType: "json",
            success: function( json ) {
                query_progress( json );
            },
            error: function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem starting the job!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
            },
        })
    })
});


function query_progress( json ) {
    $.ajax({
        url: "/openrem/admin/queryupdate",
        data: {
            query_id: json.query_id
        },
        type: "POST",
        dataType: "json",
        success: function( json ) {
            $( '#qr-status' ).html( json.message );
            if (json.status == "not complete") setTimeout(function(){
                var data = {
                    query_id: json.query_id
                }
                query_progress( data );
            }, 500);
            if (json.status == "complete"){
                var data = {
                    query_id: json.query_id
                }
                move_button( data );
            }
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem getting the status!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }

    });

}

function move_button( json ) {

}
