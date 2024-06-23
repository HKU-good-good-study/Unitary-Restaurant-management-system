from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from .models import Menu, MenuUpdate

router = APIRouter()


@router.post("/", response_description="Create a new menu", status_code=status.HTTP_201_CREATED, response_model=Menu)
async def create_menu(request: Request, menu: Menu = Body(...)):
    menu = jsonable_encoder(menu)
    new_menu = request.app.database["menus"].insert_one(menu)
    created_menu = request.app.database["menus"].find_one(
        {"_id": new_menu.inserted_id}
    )

    return created_menu


@router.get("/", response_description="List all menus", response_model=List[Menu])
async def list_menu(request: Request):
    menus = list(request.app.database["menus"].find(limit=100))
    return menus


@router.get("/{id}", response_description="Get a single menu by id", response_model=Menu)
async def find_menu(id: int, request: Request):
    if (menu := request.app.database["menus"].find_one({"_id": id})) is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")


@router.put("/{id}", response_description="Update a menu", response_model=Menu)
async def update_menu(id: int, request: Request, menu: MenuUpdate = Body(...)):
    menu = {k: v for k, v in menu.dict().items() if v is not None}
    if len(menu) >= 1:
        update_result = request.app.database["menus"].update_one(
            {"_id": id}, {"$set": menu}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")

    if (
            existing_menu := request.app.database["menus"].find_one({"_id": id})
    ) is not None:
        return existing_menu

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")


@router.delete("/{id}", response_description="Delete a menu")
async def delete_menu(id: int, request: Request, response: Response):
    delete_result = request.app.database["menus"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")
