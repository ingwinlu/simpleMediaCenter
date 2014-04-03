var runUpdate = 0;

$( document ).ready(function() {
    $.ajaxSetup({ cache: false });
    update()
    runUpdate = setInterval("update()", 3000);
});


function update(){
    $.getJSON("./status/")
        .done(function( json ) {
            if (json.playerStatus == "0"){ //stopped
                $("#btn-pause").attr('disabled', true);
                $("#btn-resume").attr('disabled', true);
                $("#btn-stop").attr('disabled', true);
                
                $("#player-text").text('Player - ' + json.playerType + ' - stopped')
            }else if (json.playerStatus == "1"){ //playing
                $("#btn-pause").attr('disabled', false);
                $("#btn-resume").attr('disabled', true);
                $("#btn-stop").attr('disabled', false);
                
                $("#player-text").text('Player - ' + json.playerType + ' - playing ' + json.currentFile)
            }else if (json.playerStatus == "2"){ //paused
                $("#btn-pause").attr('disabled', true);
                $("#btn-resume").attr('disabled', false);
                $("#btn-stop").attr('disabled', false);
                
                $("#player-text").text('Player - ' + json.playerType + ' - paused ' + json.currentFile)
            }
            //console.log( "JSON Data: " + json.playerStatus );
            
        })
        .fail(function( jqxhr, textStatus, error ) {
            clearInterval(runUpdate)
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            alert("Could not load json, is the Server running?")
        });
}