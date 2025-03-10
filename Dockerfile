# desktop-qt/Dockerfile
FROM ubuntu:20.04

# Установка необходимых пакетов
RUN apt update && apt install -y qt5-default libx11-dev libxkbcommon-dev libxkbcommon-x11-dev cmake

# Копирование кода приложения
COPY . /app

# Сборка приложения
WORKDIR /app
RUN cmake . && make

# Экспорт переменных окружения
ENV DISPLAY=$DISPLAY
ENV QT_X11_NO_MITSHM=1

# Запуск приложения
CMD ["./main"]
