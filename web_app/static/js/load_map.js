function loadAllMapImage() {
    loadMapImage('globalMapContainer', 'get_global_map_image')
    loadMapImage('currentMapContainer', 'get_curr_map_image')
}

function loadMapImage(elementId, route) {
    const mapContainer = document.getElementById(elementId);
    if (mapContainer) {
        mapContainer.innerHTML = ''; // Очищаем контейнер перед добавлением нового изображения
        
        const timestamp = new Date().getTime();

        const img_g = document.createElement('img');
        img_g.src = `/${route}?t=${timestamp}`; // Используем маршрут для получения изображения
        img_g.alt = 'Global Map Image';
        // img_g.id = 'global_image'
        // img_g.onclick = toggleImages
        img_g.style.width = '100%'; // Устанавливаем ширину на 100% контейнера
        img_g.style.height = 'auto'; // Автоматическая высота для сохранения пропорций
        mapContainer.appendChild(img_g);

        // const img_c = document.createElement('img');
        // img_c.src = `/get_curr_map_image?t=${timestamp}`; // Используем маршрут для получения изображения
        // img_c.alt = 'Curr Map Image';
        // img_c.id = 'curr_image'
        // img_c.onclick = toggleImages
        // img_c.classList = ['hidden']
        // img_c.style.width = '100%'; // Устанавливаем ширину на 100% контейнера
        // img_c.style.height = 'auto'; // Автоматическая высота для сохранения пропорций
        // mapContainer.appendChild(img_c);
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