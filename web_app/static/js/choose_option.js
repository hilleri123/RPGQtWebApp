function openModal(character_id, item_id) {
    // Показать модальное окно
    document.getElementById('myModal').style.display = 'block';

    // Запрашиваем данные персонажей с сервера
    fetch('/get_characters')
        .then(response => response.json())
        .then(characterData => {
            const optionsList = document.getElementById('optionsList');
            optionsList.innerHTML = ''; // Очищаем список перед добавлением новых элементов

            characterData.forEach(character => {
                const li = document.createElement('li');
                li.textContent = character.name;
                li.onclick = () => selectOption(character_id, item_id, character.id); // Устанавливаем обработчик клика с использованием ID
                optionsList.appendChild(li);
            });

            // Добавляем дополнительные опции "бросить" и "отмена"
            ['бросить'].forEach(option => {
                const li = document.createElement('li');
                li.textContent = option;
                li.onclick = () => selectOption(character_id, item_id, option); // Обработка как строка
                optionsList.appendChild(li);
            });
        })
        .catch(error => console.error('Ошибка при получении данных персонажей:', error));
}

function closeModal() {
    // Скрыть модальное окно
    document.getElementById('myModal').style.display = 'none';
}

function selectOption(character_id, item_id, to_character_id) {
    closeModal(); // Закрываем модальное окно после выбора

    // Определяем, что отправлять на сервер (ID или текст)
    const dataToSend = typeof to_character_id === 'string' ? 
    { 
        'character_id': character_id, 
        'item_id': item_id, 
        choice_text: to_character_id 
    } : { 
        'character_id': character_id, 
        'item_id': item_id, 
        choice_id: to_character_id 
    };

    // Отправляем результат на сервер
    fetch('/process_choice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Ошибка:', error));
}