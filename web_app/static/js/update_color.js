function updateColor(characterId) {
    var color = document.getElementById('colorPicker').value;

    fetch('/update_color', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'character_id': characterId,
            'color': color
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Color updated successfully!');
        } else {
            alert('Failed to update color.');
        }
    })
    .catch(error => console.error('Error:', error));
}