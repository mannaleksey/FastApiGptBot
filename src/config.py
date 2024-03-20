import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ['API_KEY']
MONGODB_URL = os.environ['MONGODB_URL']


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.python_db
