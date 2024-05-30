from fastapi import (
    Depends,
    FastAPI,
    Cookie,
    Form,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from database import Database
from os import getenv
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_db_client()
    yield
    Database.close()


app = FastAPI(lifespan=lifespan)


def startup_db_client():
    args = {}

    # grab address and port from system variables
    host = getenv("MONGODB_ADDR")
    port = getenv("MONGODB_PORT")

    # Check if using default path
    if host == None:
        host = "localhost"
    if port == None:
        port = 27017

    if host:
        args["host"] = host
    if port:
        args["port"] = port
    print(args)
    app.database = Database(host, port).database
    print("Connected to MongoDB")


origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)
