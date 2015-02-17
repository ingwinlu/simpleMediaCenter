function updateUI(state){
    if(state.player == 'stop'){
        $('#btn-stop').addClass("disabled");
        $('#btn-play').removeClass("disabled");
        $('#btn-pause').addClass("disabled");
    }else if (state.player == 'play'){
        $('#btn-stop').removeClass("disabled");
        $('#btn-play').addClass("disabled");
        $('#btn-pause').removeClass("disabled");
    }else if (state.player == 'pause'){
        $('#btn-stop').removeClass("disabled");
        $('#btn-play').removeClass("disabled");
        $('#btn-pause').addClass("disabled");
    }
    
    // update progressbar + timer
}

$(document).ready(function(){
            namespace = '/controller';
            var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
            // say hello to the server
            socket.on('connect', function() {
                socket.emit('new_connection', {});
            });
            var state = {};
            // update playerstatus
            socket.on('new_state', function(new_state) {
                state = new_state
                updateUI(state)
                alert(JSON.stringify(state, null, 4));
            });
            // button controlls
            $('#btn-stop').click(function(event) {
                socket.emit('controller', {player: 'stop'});
                return false;
            });
            $('#btn-play').click(function(event) {
                socket.emit('controller', {player: 'play'});
                return false;
            });
            $('#btn-pause').click(function(event) {
                socket.emit('controller', {player: 'pause'});
                return false;
            });
            $('#btn-volume-down').click(function(event) {
                socket.emit('controller', {volume: state.volume-10});
                return false;
            });
            $('#btn-volume-up').click(function(event) {
                socket.emit('controller', {volume: state.volume+10});
                return false;
            });
        });