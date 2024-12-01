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

    // Обработка события 'character_reload'
    socket.on('character_reload', function(data) {
        console.log('Character reload event received.');
        console.log(data.message);
        loadCharacter(playerId);
    });
});

function loadCharacter(characterId) {
    fetch(`/character/${characterId}`)
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