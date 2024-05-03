from fastapi import FastAPI, Cookie, Form, HTTPException, Request, Response, status
from database import Database
from os import getenv
import uvicorn
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app:FastAPI):
    startup_db_client()
    yield
    Database.close()

app = FastAPI(lifespan=lifespan)


def startup_db_client():
    args = {}
    
    # grab address and port from system variables
    host = getenv('MONGODB_ADDR')
    port = getenv('MONGODB_PORT')

    # Check if using default path
    if host == None:
        host = 'localhost'
    if port == None:
        port = 27017

    if host:
        args['host'] = host
    if port:
        args['port'] = port
    print(args)
    app.database = Database(host,port).database
    print("Connected to MongoDB")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(request:Request, response: Response, username: str, password:str):
    return True

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)