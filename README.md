# Microservice for building a sequence of tasks 

## Task: 
Create a microservice **"Build System"**. 
The microservice has files in yaml format with builds and tasks. 
Tasks have dependencies. 
The service should have a single entry point **"POST/get_tasks"** and return a list of tasks sorted by dependencies on a JSON request {"build": "name"}.

## Service implementation:
The **BuildManager** class generates a list of tasks for each build 
when uploading files. 
The list contains tasks in the order of priority execution of dependencies. 
When requesting a list for build, a ready-made list of tasks is returned. 
Task search speed - **O(1)**.

## Stack:
- Python
- FastAPI
- PyTest
- Uvicorn
- Docker

## Debugging:
The settings for debugging the project are in the file **settings.py**. 
Debugging is started from a file **debug_server.py**.

## Deploying:
The docker container is deployed on the host on port **8000**. 
Build image and launch a container:  
`docker-compose up --build`