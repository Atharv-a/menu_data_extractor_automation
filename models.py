from pydantic import BaseModel
from typing import List

class Restaurant(BaseModel):
    name: str

class ListItem(BaseModel):
    item: str
    price: int

class Menu(BaseModel):
    name: str
    menu_list: List[ListItem]
