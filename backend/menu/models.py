from typing import Optional, List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field, ConfigDict


class Ingredient(TypedDict):
    name: str
    weight: int


class Menu(BaseModel):
    __pydantic_config__ = ConfigDict(extra='forbid')

    id: int = Field(...)
    name: str = Field(...)
    price: float = Field(...)
    weight: float = Field(...)
    ingredient: List[Ingredient] = Field(...)
    sold: int = Field(...)
    availability: bool = Field(...)
    desc: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "3",
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "120",
                "ingredient": "[{'name': 'Carrot', 'weight': 120}]",
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles"
            }
        }


class MenuUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    ingredient: Optional[List[Ingredient]]
    sold: Optional[int]
    availability: Optional[bool]
    desc: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "120",
                "ingredient": "[{'name': 'Carrot', 'weight': 120}]",
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles"
            }
        }