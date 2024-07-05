from fastapi import APIRouter, Body, Request, Response, HTTPException, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
from database import Database
import uuid
from .models import Menu, MenuUpdate, Ingredient

db = Database()
router = APIRouter()


async def get_menu(id: str):
    result = await db.fetch_one("menus", {"id": f"{id}"})
    return result


@router.get("/all")
async def get_menus():
    menus = await db.fetch_collection("menus")
    if menus:
        for i in range(len(menus)):
            del menus[i]["_id"]  # remove defualt id given by mongodb
        return menus
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No menu created")


@router.get("/{id}", response_description="Get a single menu by id")
async def get_menu_by_id(id: str):
    menu = await get_menu(id)
    if menu:
        del menu["_id"]
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu not found")


@router.post("/{id}")
async def create_menu(id: str, menu: Menu):
    result = await get_menu(id)
    if result:  # should not exist table having the same id
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"menu exists")

    result = await db.execute("menus", menu.model_dump(), "insert")
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"menu creation failed")


@router.put("/{id}")
async def update_menu(id: str, menu: Menu):
    result = await db.fetch_one("menus", {"id": f"{id}"})
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu not found")

    result = await db.execute("menus", {"filter": {"id": f"{id}"}, "update": {"$set": menu.model_dump()}}, "update")
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"table update failed")

    updated_menu = await get_menu(id)
    if updated_menu:
        del updated_menu["_id"]
        return updated_menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu not found")

@router.delete("/{id}")
async def delete_menu(id: str):
    menu = await db.fetch_one("menus", {"id": f"{id}"})
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu not found")
    result = await db.execute("menus", {"id": f"{id}"}, "delete")  # delete menu from database
    if not result:  # deleteion failed
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"menu deletion failed")

    return {"message": "Menu deleted successfully"}