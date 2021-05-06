docker build --tag homework:1 .
docker run --name homework1 -d -p 8080:80 homework:1
