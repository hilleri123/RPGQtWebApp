function saveAddress(characterId) {
    fetch('/save_address', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'character_id': characterId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Адрес успешно сохранен!');
        } else {
            alert('Ошибка при сохранении адреса.');
        }
    })
    .catch(error => console.error('Ошибка:', error));
}