function loadAllMapImage() {
    loadMapImage('globalMapContainer', 'get_global_map_image')
    loadMapImage('currentMapContainer', 'get_curr_map_image')
}

function loadMapImage(elementId, route) {
    const mapContainer = document.getElementById(elementId);
    if (mapContainer) {
        const timestamp = new Date().getTime();
        const imgId = `image_${elementId}`;

        let img = document.getElementById(imgId); // Проверяем, существует ли уже изображение

        if (img) {
            // Если изображение уже существует, обновляем только src
            img.src = `/${route}?t=${timestamp}`;
        } else {
            // Если изображения нет, создаем его
            img = document.createElement('img');
            img.src = `/${route}?t=${timestamp}`; // Используем маршрут для получения изображения
            img.alt = 'Map Image';
            img.id = imgId;
            img.style.width = '100%'; // Устанавливаем ширину на 100% контейнера
            img.style.height = 'auto'; // Автоматическая высота для сохранения пропорций
            mapContainer.appendChild(img);
        }
    } else {
        console.error(`Element with id "${elementId}" not found.`);
    }
}

function toggleImages() {
    const image1 = document.getElementById('globalMapContainer');
    const image2 = document.getElementById('currentMapContainer');

    if (image1.classList.contains('hidden')) {
        image1.classList.remove('hidden');
        image2.classList.add('hidden');
    } else {
        image1.classList.add('hidden');
        image2.classList.remove('hidden');
    }
}

// Вызов функции для загрузки изображения после загрузки страницы
window.onload = loadAllMapImage;