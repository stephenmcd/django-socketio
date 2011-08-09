$(function() {

    var name, started = false;

    var addMessage = function(data) {
        var d = new Date();
        data.time = $.map([d.getHours(), d.getMinutes(), d.getSeconds()],
                          function(s) {
                              s = String(s);
                              return (s.length == 1 ? '0' : '') + s;
                          }).join(':');
        $('#message-template').tmpl(data).appendTo('#messages');
    };

    $('form').submit(function() {
        var value = $('#message').val();
        if (value) {
            if (!started) {
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
    socket.on('connect', function() {
        socket.subscribe('room-' + window.room);
        $('form').slideDown(function() {
            $('#message').focus();
        });
    });

    socket.on('message', function(data) {
        switch (data.action) {
            case 'in-use':
                alert('Name is in use, please choose another');
                break;
            case 'started':
                started = true;
                $('#submit').val('Send message');
                addMessage({name: name, message: 'joins'});
                break;
            default:
                if (started) {
                    if (data.action != 'message') { // join or leave
                        data.message = data.action + 's';
                    }
                    addMessage(data);
                    break;
                }
        }
    });

    $('#message').focus();

});
