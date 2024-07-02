from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict

class Ingredient(BaseModel):
    id: int
    name: str
    weight: float

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
    image: bytes = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "3",
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "450",
                "ingredient": [{"id": 1, "name": "Carrot", "weight": 120.0}], # [{carrot: 120.0}. {}, {}]
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles",
                "image": b"..."
            }
        }

class MenuUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    weight: Optional[float]
    ingredient: Optional[List[Ingredient]]
    sold: Optional[int]
    availability: Optional[bool]
    desc: Optional[str]
    image: Optional[bytes]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "450g",
                "ingredient": [{"id": 1, "name": "Carrot", "weight": 120.0}],
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles",
                "image": b"..."
            }
        }