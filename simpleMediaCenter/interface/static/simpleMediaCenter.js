$( document ).ready(function() {
    $.ajaxSetup({ cache: false });
    update()
    setInterval("update()", 3000);
    

});


function update(){
    $.getJSON("./status")
        .done(function( json ) {
            if (json.playerStatus == "0"){ //stopped
                $("#btn-pause").prop('disabled', true);
                $("#btn-stop").prop('disabled', true);
            }else if (json.playerStatus == "1"){ //playing
                $("#btn-pause").prop('disabled', false);
                $("#btn-stop").prop('disabled', false);
            }else if (json.playerStatus == "2"){ //paused
                $("#btn-pause").prop('disabled', false);
                $("#btn-stop").prop('disabled', false);
            }
            console.log( "JSON Data: " + json.playerStatus );
            
        })
        .fail(function( jqxhr, textStatus, error ) {
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
        });
}