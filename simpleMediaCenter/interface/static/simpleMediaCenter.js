var runUpdate = 0;

$( document ).ready(function() {
    $.ajaxSetup({ cache: false });
    $("#searchFile").click(function(){searchFile()})
    $("#searchDir").click(function(){searchDir()})
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
            /*
            if(json.threadRunning == "1"){ //Thread is running, display loading
                showLoading()
                console.log('thread is Running')
            }
            if(json.threadRunning != "1"){
                hideLoading()
            }
            */
            
            //set player buttons
            if (json.playerStatus == "0"){ //stopped, disable all buttons
                $(".playerbutton").attr('disabled', true);
                
                $("#player-text").text('Player - ' + json.activePlayer + ' - stopped')
            }else if (json.playerStatus == "1"){ //playing
                $(".playerbutton").attr('disabled', false);
                $("#btn-resume").attr('disabled', true);
                
                $("#player-text").text('Player - ' + json.activePlayer + ' - playing ' + json.currentFile)
            }else if (json.playerStatus == "2"){ //paused
                $(".playerbutton").attr('disabled', false);
                $("#btn-pause").attr('disabled', true);
                
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
    window.location = './clearException';
}

function showLoading(){
    $("#loading").show();
}

function hideLoading(){
    $("#loading").hide();
}

function searchFile(){
    window.location = './searchFile?search=' + $("#browserSearch").val();
}

function searchDir(){
    window.location = './searchDir?search=' + $("#browserSearch").val();
}
