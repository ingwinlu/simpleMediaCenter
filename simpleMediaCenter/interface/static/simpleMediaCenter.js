var runUpdate = 0;

$( document ).ready(function() {
    $.ajaxSetup({ cache: false });
    runUpdate = setInterval("update()", 3000);
});


function update(){
    $.getJSON("./status/")
        .done(function( json ) {
            if (json.playerStatus == "0"){ //stopped
                $("#btn-pause").attr('disabled', true);
                $("#btn-stop").attr('disabled', true);
                $("#btn-pause").html('<span class="glyphicon glyphicon-pause"></span>Pause')
            }else if (json.playerStatus == "1"){ //playing
                $("#btn-pause").attr('disabled', false);
                $("#btn-stop").attr('disabled', false);
                $("#btn-pause").html('<span class="glyphicon glyphicon-pause"></span>Pause')
            }else if (json.playerStatus == "2"){ //paused
                $("#btn-pause").attr('disabled', false);
                $("#btn-stop").attr('disabled', false);
                $("#btn-pause").html('<span class="glyphicon glyphicon-pause"></span>Play')
            }
            console.log( "JSON Data: " + json.playerStatus );
            
        })
        .fail(function( jqxhr, textStatus, error ) {
            clearInterval(runUpdate)
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            alert("Could not load json, is the Server running?")
        });
}