from fastapi import FastAPI, HTTPException
from models import Restaurant
from webscraping import webscraping
from image_to_text import image_to_text
from database import start_db
from schema import individual_serial
from utils import parse_menu_lines
app = FastAPI()

collection = start_db()

@app.get("/")
def default():
    return {"message": "Hello there, I am automation service that provides menu for you favourite restaurant"}


@app.get("/menu")
async def get_menu(restaurant:Restaurant):
    try:
        data = await collection.find_one({'name':restaurant.name.lower()})
        if data is None:
            webscraping(restaurant.name)
            lines = image_to_text()
            items_and_prices = parse_menu_lines(lines)
            data = {
                "name": restaurant.name.lower(),
                "menu_list": items_and_prices
            }
            await collection.insert_one(data)
        else:
            data = individual_serial(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {'data':data}

