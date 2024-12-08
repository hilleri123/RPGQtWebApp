document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Получаем текущий URL и извлекаем ID игрока
    var currentUrl = window.location.pathname;
    var pathParts = currentUrl.split('/');
    var playerId = pathParts[pathParts.length - 1];

    console.log("Текущий ID игрока:", playerId);

    // Обработка события 'reload'
    socket.on('reload', function(data) {
        console.log(data.message);
        location.reload();
    });

    socket.on('character_reload', function(data) {
        console.log('Character reload event received.');
        console.log(data.message);
        loadCharacter(playerId);
    });
    
    socket.on('map_reload', function(data) {
        console.log('Map reload event received.');
        console.log(data.message);
        loadAllMapImage();
    });
    
    socket.on('notes_reload', function(data) {
        console.log('Notes reload event received.');
        console.log(data.message);
        loadNotes(playerId);
    });
});
