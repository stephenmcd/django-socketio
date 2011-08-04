$(function() {

    var name, connected = false;

    var addMessage = function(data) {
        var d = new Date();
        var h = d.getHours(), m = d.getMinutes(), s = d.getSeconds();
        var pad = function(s) {return (s.length == 1 ? '0' : '') + s;}
        data.time = [pad(h), pad(m), pad(s)].join(':');
        $('#message-template').tmpl(data).appendTo('#messages');
    };

    $('form').submit(function() {
        var value = $('#message').val();
        if (value) {
            if (!connected) {
                name = value;
                socket.send({room: window.room, action: 'start', name: name});
            } else {
                socket.send({room: window.room, action: 'message', message: value});
            }
        }
        $('#message').val('');
        return false;
    });

    var socket = new io.Socket();
    socket.connect();

    socket.on('message', function(data) {
        switch (data.action) {
            case 'in-use':
                alert('Name is in use, please choose another');
                break;
            case 'start':
                socket.subscribe(window.room);
                connected = true;
                $('#submit').val('Send message');
                break;
            case 'join':
                addMessage(data);
                break;
            case 'leave':
                addMessage(data);
                break;
            case 'message':
                addMessage(data);
                break;
        }
    });

    $('#message').focus();

});
