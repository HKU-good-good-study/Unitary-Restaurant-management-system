from fastapi import Depends, FastAPI, Cookie, Form, HTTPException, Request, Response, status
from auth.router import router as auth_router
from database import Database
from os import getenv
import uvicorn
from contextlib import asynccontextmanager

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
async def root(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return {"message": "No valid token"}
    
    payload = verify_jwt(token)
    if not payload:
        return {"message": "No valid token"}

    return {"message": f"Hello {payload['username']}, your token expires at {payload['exp']}"}
    
    
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)