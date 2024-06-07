from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str


class Menu(BaseModel):
    name: str
    menu_list: list