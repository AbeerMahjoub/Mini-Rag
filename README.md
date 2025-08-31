# Mini RAG project

RAG model for question answering application

## Requirements
 - Python
 
## Installation 
 ### Install the required packages
    $ pip install -r requirements.txt



### Setup the environment variables
    $ cp .env.example .env


## Run the FastAPI server
    $ uvicorn src.main:app --reload --host 0.0.0.0 --port 5000

## Postman Collection
Download the POSTMAN collection from /assets/mini-rag-app.postman_collection.json