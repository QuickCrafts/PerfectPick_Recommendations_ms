@echo off

rem Delete existing containers
docker stop rabbitmq mongo recommendationms
docker rm rabbitmq mongo recommendationms

rem Delete existing recommendation-ms images
docker rmi recommendation-ms

rem Create network
docker network create perfectpicknetwork

rem Create RabbitMQ container
docker run -d --rm --name rabbitmq --network perfectpicknetwork -p 5672:5672 -p 15672:15672 rabbitmq

rem Create MongoDB container
docker run -d --name mongo --network perfectpicknetwork -p 27017:27017 -v mongodbdata:/data/db mongo

rem Build recommendation-ms image
docker build -t recommendation-ms .

rem Create recommendation-ms container
docker run -d --name recommendationms --network perfectpicknetwork -p 8000:8000 recommendation-ms