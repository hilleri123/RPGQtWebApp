# desktop-qt/Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Создание символьной ссылки на файл зоны времени и запись зоны в /etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Установка необходимых пакетов
RUN apt update && apt install -y python3 python3-pip python3-pyqt5 libx11-dev libxkbcommon-dev libxkbcommon-x11-dev tzdata

# Установка PyQt5
RUN pip3 install --no-cache-dir pyqt5

# Копирование кода приложения
COPY . /app

# Экспорт переменных окружения
ENV DISPLAY=$DISPLAY
ENV QT_X11_NO_MITSHM=1

# Запуск приложения
CMD ["python3", "/app/main.py"]