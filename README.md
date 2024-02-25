# Sympoly Assignment Project

## Description
This project is built using FastAPI to create a RESTful API for Sympoly Assignment.

## Features
- CRUD operations for managing invoices
- Integration with MongoDB using Beanie ODM
- Docker support for containerization

## Quick Start
To get this project up and running locally on your computer:

1. Set up a Python development environment.
2. Fork this repository and clone your fork to your local machine.
3. create .env file (you can rename example.env to .env )
4. run the following comment to create an mongoDb container 
```bash
docker-compose -f docker-compose-db-only.yml up
  ```  
5. Navigate to the project directory and install dependencies using poetry:

```bash
poetry install
```

4. Start the FastAPI server using uvicorn:

```bash
poetry run uvicorn main:app --reload
```

## Environment Variables
To run this project, you will need to add the following environment variables to your .env file:
- `MONGO_HOST` - Connection string for the MongoDB host url
- `MONGO_USER` - The mongoDB user name
- `MONGO_PASS` - The mongoDB user password
- `MONGO_PORT` - The mongoDB connection port 
```.env
MONGO_HOST=mongodb
MONGO_USER=rootuser
MONGO_PASS=rootpass
MONGO_PORT=27017 
```

## Running with Docker
Make sure you have Docker and Docker Compose installed on your machine. Then run:

```bash
docker-compose up --build
```

## API documentation 
after running the app you can vieu the docomation in the flloing utl : 
http://127.0.0.1:8000/docs#/