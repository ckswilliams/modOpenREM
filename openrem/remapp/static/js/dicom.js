$(document).ready(function(){
    // Submit post on submit
    var form = $('form#post-form');
    form.submit(function(event) {
        event.preventDefault();
        console.log('ajax form submission function called successfully.');
        $( '#move-status' ).html( '' );
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
    });
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
                };
                query_progress( data );
            }, 500);
            if (json.status == "complete"){
                var data = {
                    query_id: json.query_id
                };
                var move_html = '<div><button type="button" class="btn btn-default" id="move" data-id="'
                    + json.query_id
                    + '">Move</button></div>';
                $( '#move-button').html( move_html );
                $('#move').click(function(){
                    console.log("In the move function");
                    var query_id = $(this).data("id");
                    console.log(query_id);
                    $( '#move-button').html( '' );
                    $.ajax({
                        url: "/openrem/admin/queryretrieve",
                        data: {
                            query_id: query_id
                        },
                        type: "POST",
                        dataType: "json",
                        success: function( json ) {
                            console.log("In the qr success function.")
                            retrieve_progress( json );
                        }
                    });
                });
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


function retrieve_progress( json ) {
    $.ajax({
        url: "/openrem/admin/moveupdate",
        data: {
            query_id: json.query_id
        },
        type: "POST",
        dataType: "json",
        success: function( json ) {
            $( '#move-status' ).html( json.message );
            if (json.status != "move complete") setTimeout(function(){
                var data = {
                    query_id: json.query_id
                };
                retrieve_progress( data );
            }, 500);
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem getting the status!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }

    });

}
