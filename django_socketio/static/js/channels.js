
io.Socket.prototype.subscribe = function(channel) {
    this.send(['__subscribe__', channel]);
    return this;
};

io.Socket.prototype.unsubscribe = function(channel) {
    this.send(['__unsubscribe__', channel]);
    return this;
};
