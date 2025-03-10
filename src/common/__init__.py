from .autoresize import AutoResizingListWidget, AutoResizingTextEdit
from .base_map_widget import BaseMapWidget
from .base_map_label import BaseMapLabel
from .base_map_object import BaseMapObject
from .datetime_editor import DateTimeEditWidget
from .skill_label_list import SkillListWidget
from .log_widget import LogWidget
from .html_text_edit_widget import HtmlTextEdit
from .base_list_item_widget import BaseListItemWidget
from .base_list_widget import BaseListWidget
import socket






def get_local_ip():
    """Возвращает локальный IP-адрес."""
    try:
        # Создаем временное соединение для определения IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Используем адрес Google DNS для получения локального IP (не будет отправлено реальное соединение)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Не удалось получить локальный IP: {e}")
        local_ip = "127.0.0.1"  # Используем localhost в случае ошибки
    finally:
        s.close()
    return local_ip
