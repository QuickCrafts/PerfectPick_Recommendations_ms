#!/bin/bash

# Remove existing containers and network if they exist
docker rm -f myfastapi mymongo rabbitmq 2>/dev/null
docker network rm mynetwork 2>/dev/null

# Pull the MongoDB image
docker pull mongo

# Pull the RabbitMQ image
docker pull rabbitmq:3.13-management

# Build the FastAPI application image
docker build -t fastapi-app .

# Create a Docker network
docker network create mynetwork

# Run the FastAPI application container
docker run -d --name myfastapi --network mynetwork -p 80:80 fastapi-app

# Run the MongoDB container
docker run -d --name mymongo --network mynetwork -v mongodbdata:/data/db mongo

# Run the RabbitMQ container
docker run -d --name rabbitmq --network mynetwork -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management