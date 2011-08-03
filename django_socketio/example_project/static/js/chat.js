$(function() {

    var name;

    var timestamp = function() {
        var d = new Date();
        var h = d.getHours(), m = d.getMinutes(), s = d.getSeconds();
        var pad = function(s) {return (s.length == 1 ? '0' : '') + s;}
        return [pad(h), pad(m), pad(s)].join(':');
    };

    $('form').submit(function() {
        var value = $('#message').val();
        if (value) {
            if (!name) {
                name = value;
                $('#submit').val('Send message');
                socket.send({name: name, message: 'enters'});
            } else {
                socket.send({name: name, message: value});
            }
        }
        $('#message').val('');
        return false;
    });

    var socket = new io.Socket();
    socket.connect();
    socket.on('connect', function() {
        socket.subscribe('blah');
    });

    socket.on('message', function(data) {
        data.time = timestamp();
        $('#message-template').tmpl(data).appendTo('#messages');
    });

    $('#message').focus();

});
