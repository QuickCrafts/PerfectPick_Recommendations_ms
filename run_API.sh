docker network create mynetwork
docker run -d --rm --name rabbitmq --network mynetwork -p 5672:5672 -p 15672:15672 rabbitmq
docker run -d --name mongo --network mynetwork -p 27017:27017 -v mongodbdata:/data/db mongo
docker build -t recommendation-ms . 
docker run -d --name recommendationms --network mynetwork -p 8000:8000 recommendation-ms
