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