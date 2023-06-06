docker-compose build
docker-compose up -d server
docker-compose up --scale client=4
