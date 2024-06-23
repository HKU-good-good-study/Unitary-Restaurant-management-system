from models import CustomModel
from dataclasses import asdict, dataclass, fields
import uuid

class Order(CustomModel):
    table:str
    time:str # Time order gets created
    id: str
    dish:dict # {name of dish: {"amount":, "description":}}

    class Config:
        title = 'Order'
        schema_extra = {
            "example": {
                "table": "A1",
                "time": "2024-01-30-22:30:12",
                "id": "3",
                "dish": {
                    "Beef Chow Fun": {
                        "amount": 2,
                        "description": "Dry fried beef Shahe noodles"
                    }
                }
            }
        }

class Table(CustomModel):
    id:str
    order:dict | None # store orders by time {date: list[OrderID]}
    status: str # open, booked, serving
    time:str
    seats:int # Table size: how many people can be served on this table

    class Config:
        title = 'Table'
        schema_extra = {
            "example": {
                "id": "A1",
                "order": {
                    "2024-01-30": ["orderO1", "orderO2"]
                },
                "status": "open",
                "time": "2024-01-30-22:30:12",
                "seats": 4
            }
        }