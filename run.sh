docker build -t ml-starter .
docker run -d --name ml-starter -p 80:80 -v /home/robert/Repositories/ml-starter/external-folder:/mounted_volume ml-starter:latest
