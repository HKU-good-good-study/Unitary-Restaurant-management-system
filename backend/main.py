from dotenv import load_dotenv, find_dotenv
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
from checkout.router import router as checkout_router
from fastapi import FastAPI, Request, Response, HTTPException
from database import Database
from os import getenv
import uvicorn
from contextlib import asynccontextmanager

from menu.routes import router as menu_router
from menu.models import Menu, MenuUpdate
from table.router import router as table_router
from table.schemas import Table, Order
from typing import List


#from constants import menuDb


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_db_client()
    yield
    close_db_client()


app = FastAPI(lifespan=lifespan)

load_dotenv()
app.include_router(table_router, tags=["tables"], prefix="/table")
app.include_router(menu_router, tags=["menus"], prefix="/menu")


def startup_db_client():
    args = {}

    # grab address and port from system variables
    host = getenv("MONGODB_ADDR", "localhost")
    port = int(getenv("MONGODB_PORT", "27017"))

    args["host"] = host
    args["port"] = port
    print(args)

    setattr(app, "database", Database(**args))
    print("Connected to MongoDB")


def close_db_client():
    app.database.close()  # type: ignore
    print("Closed connection to MongoDB")


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

app.include_router(checkout_router)

# Sample Editing Methods
menuDb: List[Menu] = []


@app.get("/menus")
async def get_menus():
    return menuDb


@app.post("/menus")
async def create_menu(menu: Menu):
    menuDb.append(menu)
    return {"id": menu.id}


@app.delete("/menus/{_id}")
async def delete_menu(_id):
    for menu in menuDb:
        if menu.id == _id:
            menuDb.remove(menu)
            return
    raise HTTPException(
        status_code=404, detail=f"Delete user failed, id {_id} not found."
    )


@app.put("/menus/{_id}")
async def update_user(menu_update: MenuUpdate, _id):
    for menu in menuDb:
        if menu.id == _id:
            if menu_update.name is not None:
                menu.name = menu_update.name
            if menu_update.price is not None:
                menu.price = menu_update.price
            if menu_update.ingredient is not None:
                menu.ingredient = menu_update.ingredient
            if menu_update.sold is not None:
                menu.sold = menu_update.sold
            if menu_update.availability is not None:
                menu.availability = menu_update.availability
        return menu.id
    raise HTTPException(status_code=404, detail=f"Could not find user with id: {_id}")


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)
