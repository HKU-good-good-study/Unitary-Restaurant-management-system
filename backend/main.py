from fastapi import Depends, FastAPI, Cookie, Form, HTTPException, Request, Response, status
from auth.jwt_bearer import verify_jwt
from auth.jwt_handler import generate_token
from models.user import User
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

@app.post("/register")
async def register(username: str, password: str):
    user = User(username, password)
    user.save()
    return {"message": f"User {username} created successfully"}

@app.post("/login")
async def login(request:Request, response: Response, username: str, password:str):
    user = User.find_one(username)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if user.check_password(password):
        token = generate_token(user.username)
        response.set_cookie(key="access_token", value=token)
        return {"message": f"User {user.username} login successful", "token": token}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)