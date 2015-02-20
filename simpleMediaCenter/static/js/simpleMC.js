function updateUI(state){
    if(state.status == 'stopped'){
        $('#btn-stop').addClass("disabled");
        $('#btn-play').removeClass("disabled");
        $('#btn-pause').addClass("disabled");
    }else if (state.status == 'playing'){
        $('#btn-stop').removeClass("disabled");
        $('#btn-play').addClass("disabled");
        $('#btn-pause').removeClass("disabled");
    }else if (state.status == 'paused'){
        $('#btn-stop').removeClass("disabled");
        $('#btn-play').removeClass("disabled");
        $('#btn-pause').removeClass("disabled");
    }else{
        $('#btn-stop').addClass("disabled");
        $('#btn-play').addClass("disabled");
        $('#btn-pause').addClass("disabled");
    }
    // update progressbar + timer
    if(state.status = 'playing'){
        $('#progress').css("width", state.position / state.duration * 100 + '%');
        $('#progress-text').text(state.position + " of " + state.duration);
    }else{
        $('#progress').css("width", '0%');
        $('#progress-text').text('');
    }
    
    // update currently playing
    $('#player-text').text(state.title + " at " + state.location);
}

$(document).ready(function(){

    // socketio bindings
    namespace = '/controller';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // say hello to the server
    socket.on('connect', function() {
        socket.emit('new_connection');
    });
    socket.on('disconnect', function(){
        updateUI('disconnect')
    });
    // update playerstatus
    socket.on('player_status', function(state) {
        updateUI(state)
        console.log(JSON.stringify(state, null, 4));
    });
    // button controlls
    $('#btn-stop').click(function(event) {
        socket.emit('player_stop');
        return false;
    });
    $('#btn-play').click(function(event) {
        socket.emit('player_play');
        return false;
    });
    $('#btn-pause').click(function(event) {
        socket.emit('player_pause');
        return false;
    });
    $('#btn-volume-down').click(function(event) {
        socket.emit('player_vol_down');
        return false;
    });
    $('#btn-volume-up').click(function(event) {
        socket.emit('player_vol_up');
        return false;
    });
    //setup progressbar
    $('#progress-section').click(function(event){
        var $div = $(event.target);
        var offset = $div.offset();
        var width = $div.width();
        var percent = Math.round((event.clientX - offset.left) * 100 / width);
        socket.emit('set_pos', {position: percent});
        return false;
    });
});