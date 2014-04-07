var runUpdate = 0;

$( document ).ready(function() {
    $.ajaxSetup({ cache: false });
    update()
    runUpdate = setInterval("update()", 3000);
});


function update(){
    $.getJSON("./status/")
        .done(function( json ) {
            //check if exception occured
            if(json.exceptionStatus == "1"){ //exception occured
                showException(json.exceptionTitle,json.exceptionBody)
            }
            
            
            //set player buttons
            if (json.playerStatus == "0"){ //stopped
                $("#btn-pause").attr('disabled', true);
                $("#btn-resume").attr('disabled', true);
                $("#btn-stop").attr('disabled', true);
                
                $("#player-text").text('Player - ' + json.activePlayer + ' - stopped')
            }else if (json.playerStatus == "1"){ //playing
                $("#btn-pause").attr('disabled', false);
                $("#btn-resume").attr('disabled', true);
                $("#btn-stop").attr('disabled', false);
                
                $("#player-text").text('Player - ' + json.activePlayer + ' - playing ' + json.currentFile)
            }else if (json.playerStatus == "2"){ //paused
                $("#btn-pause").attr('disabled', true);
                $("#btn-resume").attr('disabled', false);
                $("#btn-stop").attr('disabled', false);
                
                $("#player-text").text('Player - ' + json.activePlayer + ' - paused ' + json.currentFile)
            }
        })
        .fail(function( jqxhr, textStatus, error ) {
            clearInterval(runUpdate)
            var err = textStatus + ", " + error;
            console.log( "Request Failed: " + err );
            showException('Connection lost', 'Connection to Media Center lost, is the server still running?')
        });
}

function showException(title, body){
    $("#exception-title").text(title)
    $("#exception-body").text(body)
    $("#exception").show();
}

function clearException(){
    $("#exception").hide();
    window.location = "./clearException";
}
