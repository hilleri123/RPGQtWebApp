import os
import shutil
from PyQt5.QtWidgets import QFileDialog

def open_img(directory, parent=None):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly

    # Открываем диалог выбора файла
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Выберите изображение",
        "",
        "Изображения (*.png *.jpg *.jpeg *.bmp);; All files (*)",
        options=options
    )
    if not file_path:
        return
    file_name = os.path.basename(file_path)
    if os.path.isfile(os.path.join(directory, file_name)):
        print(f"Warning: Файл c именем '{file_name}' уже существует в директории '{IMGS_DIR}'.")

    destination_path = os.path.join(directory, file_name)
    shutil.copy2(file_path, destination_path)

    return file_name