/*eslint object-shorthand: "off" */

function retrieveProgress(json ) {
    $.ajax({
        url: Urls.move_update(),
        data: {
            queryID: json.queryID
        },
        type: "POST",
        dataType: "json",
        success: function( json ) {
            $( "#move-status" ).html( json.message );
            if (json.status !== "move complete") setTimeout(function(){
                var data = {
                    queryID: json.queryID
                };
                retrieveProgress( data );
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
function queryProgress(json ) {
    $.ajax({
        url: Urls.query_update(),
        data: {
            queryID: json.queryID
        },
        type: "POST",
        dataType: "json",
        success: function( json ) {
            $( "#qr-status" ).html( json.message );
            if (json.status === "not complete") setTimeout(function(){
                var data = {
                    queryID: json.queryID
                };
                queryProgress( data );
            }, 500);
            if (json.status === "complete"){
                var data = {
                    queryID: json.queryID
                };
                var moveHtml = '<div><button type="button" class="btn btn-default" id="move" data-id="'
                    + json.queryID
                    + '">Move</button></div>';
                $( "#move-button").html( moveHtml );
                $("#move").click(function(){
                    // console.log("In the move function");
                    var queryID = $(this).data("id");
                    // console.log(queryID);
                    $( "#move-button").html( "" );
                    $.ajax({
                        url: Urls.start_retrieve(),
                        data: {
                            queryID: queryID
                        },
                        type: "POST",
                        dataType: "json",
                        success: function( json ) {
                            // console.log("In the qr success function.");
                            retrieveProgress( json );
                        }
                    });
                });
            }
        },
        error: function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem getting the status!" );
            // console.log( "Error: " + errorThrown );
            // console.log( "Status: " + status );
            // console.dir( xhr );
        }

    });

}


$(document).ready(function(){
    // Submit post on submit
    var form = $("form#post-form");
    form.submit(function(event) {
        event.preventDefault();
        // console.log("ajax form submission function called successfully.");
        $("#move-status" ).html( "" );
        form = $(this);
        // console.log(form);
        var serializedForm = form.serialize();
        $.ajax({ type: "POST",
            url: $(this).attr("action"),
            data: serializedForm,
            dataType: "json",
            success: function( json ) {
                queryProgress( json );
            },
            error: function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem starting the job!" );
                // console.log( "Error: " + errorThrown );
                // console.log( "Status: " + status );
                // console.dir( xhr );
            }
        });
    });
});


