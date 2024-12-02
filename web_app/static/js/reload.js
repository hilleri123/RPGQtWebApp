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
        loadMapImage();
    });
    
    socket.on('notes_reload', function(data) {
        console.log('Notes reload event received.');
        console.log(data.message);
        // loadMapImage();
    });
});

function loadCharacter(characterId) {
    const timestamp = new Date().getTime();
    fetch(`/character/${characterId}?t=${timestamp}`)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById('characterContainer');
            if (container) {
                container.innerHTML = ''; // Удаляем предыдущий контент
                container.innerHTML = html; // Загружаем новый контент
            } else {
                console.error('Элемент characterContainer не найден.');
            }
        })
        .catch(error => console.error('Ошибка при загрузке персонажа:', error));
}