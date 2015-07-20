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
});


function query_progress( json ) {
    $.ajax({
        url: "/openrem/admin/dicomstore/ajax_test3",
        data: {
            query_id: json.query_id
        },
        type: "POST",
        dataType: "json",
        success: function( json ) {
            //alert( "I'm in test3!");
            $( '#qr-status' ).html( json.message);
            if (json.status != "complete") setTimeout(function(){
                var data = {
                    query_id: json.query_id
                }
                query_progress( data );
            }, 1000);
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem getting the status!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        }

    });

}