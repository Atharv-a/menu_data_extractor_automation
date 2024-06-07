from fastapi import FastAPI, HTTPException
from models import Restaurant
from automation.webscraping import webscraping
from config.database import start_db
from schema import individual_serial
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils import find_price
app = FastAPI()

collection = start_db()


@app.get("/")
def default():
    return {"message": "Hello there, I am automation service that provides menu for your favourite restaurant"}


@app.get("/menu")
async def get_menu(restaurant: Restaurant):
    try:
        data = await collection.find_one({'name': restaurant.name.lower()})
        if data is None:
            text = await webscraping(restaurant.name)
            items_and_prices = find_price(text)

            data_to_save = {
                "name": restaurant.name.lower(),
                "menu_list": items_and_prices
            }

            await collection.insert_one(data_to_save)
            data = data_to_save
        else:
            data = individual_serial(data)
        if ('_id' in data):
            data['_id'] = str(data['_id'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        return {'data': data}

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return JSONResponse({"detail": "Not Found"}, status_code=404)


