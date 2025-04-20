#!/bin/bash


if ! docker network inspect signaling-network >/dev/null 2>&1; then
  docker network create signaling-network
fi

# Docker run
docker run -p 8080:8080 \
  --name room-signaling-server-container \
  --network signaling-network \
  -it \
  --env-file .env \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd)/src:/app \
  room-signaling-server-image