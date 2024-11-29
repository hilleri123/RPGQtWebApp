function updateSkill(characterId, skillId, inputId, change) {
    var inputElement = document.getElementById(inputId);
    var newValue = parseInt(inputElement.value) + change;

    fetch('/update_skill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'character_id': characterId,
            'skill_id': skillId,
            'new_value': newValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            inputElement.value = newValue; // Обновляем значение на странице
            // alert('Skill updated successfully!');
        } else {
            alert('Failed to update skill.');
        }
    })
    .catch(error => console.error('Error:', error));
}