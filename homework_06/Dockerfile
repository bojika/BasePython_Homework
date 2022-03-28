FROM python:3.9-bullseye

ENV PYTHONBUFFERED=1
ENV CONFIG_NAME=DevelopmentConfig

WORKDIR /app

COPY requirements.txt .
COPY prestart.sh .

RUN set -xeu \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && chmod +x prestart.sh

COPY . .

ENTRYPOINT ["bash", "prestart.sh"]

EXPOSE 5000/tcp

CMD python app.py