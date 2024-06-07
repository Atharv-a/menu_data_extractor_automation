import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()


def start_db():
    uri = os.environ.get('DATABASE_URL')

    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client.menu_db
        collection = db['menus']
        collection.create_index("name", unique=True)

    except Exception as e:
        print(e)

    return collection
