from typing import List
from models import Menu, MenuUpdate

# Example Data Table
menuDb: List[Menu] = [
    Menu(
        id=4,
        name="Beef Chow Fun",
        price="45.50",
        weight="325",
        sold="45",
        availability="true",
        desc="Dry fried beef Shahe noodles"
    ),
    Menu(
        id=5,
        name="Beef 2",
        price="45.50",
        weight="325",
        sold="45",
        availability="true",
        desc="Dry fried beef Shahe noodles"
    ),
    Menu(
        id=6,
        name="Beef 3",
        price="45.50",
        weight="325",
        sold="45",
        availability="true",
        desc="Dry fried beef Shahe noodles"
    )
]