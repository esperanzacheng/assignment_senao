# HTTP APIs for Account and Password Management:
Two RESTful HTTP APIs for creating(POST) and verifying(PUT) an account and password.

## Table of Contents
* [API Document](#api-document)
* [User Guide](#user-guide)
* [Demo Route](#demo-route)

<span id="api-document"></span>
## API Document
* [SwaggerHub](https://app.swaggerhub.com/apis-docs/esperanzacheng1117/assignment_senao/1.0#/)
* After running on your machine, use **port 8000** for testing - http://127.0.0.1:8000/api/user


<span id="user-guide"></span>
## User Guide
1. Pull Docker image from my DockerHub based on your machine
    * [amd64](https://hub.docker.com/r/esperanzacheng/senao-amd): Windows / Intel-based Mac
    ```
    docker pull esperanzacheng/senao-amd:latest
    ```
    * [arm64](https://hub.docker.com/r/esperanzacheng/senao-arm): Mac with Apple silicon
    ```
    docker pull esperanzacheng/senao-arm:latest
    ```
2. Download the zip file I attached in the email. The file includes:
    * docker-compose.yml
    * .env
3. Unzip the file and open a terminal at that folder
4. Compose up the docker with
```
docker compose up
```

<span id="demo-route"></span>
## Demo Route
http://34.202.229.227/api/user
