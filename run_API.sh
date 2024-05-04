echo "Delete existing Recommendations container"
docker stop rabbitmq mongo recommendationms
docker rm rabbitmq mongo recommendationms

echo "Delete existing Recommendations image"
docker rmi recommendation-ms

docker network create perfectpicknetwork

echo "Up message queue and mongo DB server"
docker run -d --rm --name rabbitmq --network perfectpicknetwork -p 5672:5672 -p 15672:15672 rabbitmq
docker run -d --name mongo --network perfectpicknetwork -p 27017:27017 -v mongodbdata:/data/db mongo

echo "Build image Recommendations"
docker build -t recommendation-ms .
docker run -d --name recommendationms --network perfectpicknetwork -p 8000:8000 recommendation-ms