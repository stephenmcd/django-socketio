$(function() {

    var socket = new io.Socket();
    socket.connect();
    socket.on('connect', function() {
    });
    socket.on('message', function(data) {
    });

});
