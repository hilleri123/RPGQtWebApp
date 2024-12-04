function loadNotes(characterId) {
    const timestamp = new Date().getTime();
    fetch(`/get_notes/${characterId}?t=${timestamp}`)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById('notesContainer');
            if (container) {
                container.innerHTML = ''; // Удаляем предыдущий контент
                container.innerHTML = html; // Загружаем новый контент
            } else {
                console.error('Элемент notesContainer не найден.');
            }
        })
        .catch(error => console.error('Ошибка при загрузке персонажа:', error));
}

