function chooseOption() {
    // Опции для выбора
    const options = ["бросить", "отмена"];
    
    // Получаем имена персонажей из шаблона
    const characterNames = JSON.parse(document.getElementById('characterNames').textContent);
    
    // Добавляем имена персонажей к опциям
    const allOptions = options.concat(characterNames);
    
    // Спрашиваем пользователя о выборе
    const choice = prompt("Выберите опцию: " + allOptions.join(", "));
    
    if (choice !== null && allOptions.includes(choice)) {
        // Отправляем результат на сервер
        fetch('/process_choice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ choice: choice })
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Ошибка:', error));
    } else {
        alert("Неверный выбор!");
    }
}