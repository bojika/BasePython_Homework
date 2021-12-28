FROM python:3.9-alpine

WORKDIR /opt/app

# COPY only supports the basic copying of local files into the container, while ADD
# has some features (like local-only tar extraction and remote URL support) that are not immediately obvious.
# Consequently, the best use for ADD is local tar file auto-extraction into the image, as in ADD rootfs.
# For other items (files, directories) that do not require ADD’s tar auto-extraction capability,
# you should always use COPY.
COPY requirements.txt ./requirements.txt

RUN set -xeu \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

# скопируем все, что не было скопировано раньше с учетом ограничений .dockerignore
# * означает запретить все
# ! означает сделать исключение
COPY . .

# Это только для информации, сообщает, что наше пирожениее слушает этот порт.
# Сделано только для удобства, чтобы человек, не знакомый с проектом, мог монять, какие порты нужно пробросить.
# Возможно еще указать -P при запуске контейнера, тогда будет использована информация из EXPOSE, чтобы АВТОМАТИЧЕСКИ
# пробросить указанный порт в порт >= 1024.
# определить выделенный порт можно через docker inspect
EXPOSE 8000/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
