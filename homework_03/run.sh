#/bin/bash

# остановить контейнер
docker stop hw_03

# удалить контейнер
docker rm hw_03

# создать сеть, по  умолчанию bridge
docker network create otus-net

# запустить конейнер
docker run -d -it --name hw_03 \
                  --volume /etc/localtime:/etc/localtime:ro \
                  -p 8000:8000 \
                  --rm \
                  --network otus-net \
                  hw_03:latest
