document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('reload', function(data) {
        console.log(data.message);
        // Обновляем страницу
        location.reload();
    });
});