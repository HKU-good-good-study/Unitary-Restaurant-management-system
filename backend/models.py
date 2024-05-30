from typing import Optional
from pydantic import BaseModel, Field


class Menu(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    price: float = Field(...)
    weight: int = Field(...)
    sold: int = Field(...)
    availability: bool = Field(...)
    desc: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Wid": "3",
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "325",
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles"
            }
        }


class MenuUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    weight: Optional[int]
    sold: Optional[int]
    availability: Optional[bool]
    desc: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beef Chow Fun",
                "price": "45.50",
                "weight": "325",
                "sold": "45",
                "availability": "true",
                "desc": "Dry fried beef Shahe noodles"
            }
        }


