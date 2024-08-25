from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from Routes.LocationRoute import router

from database import load_data

USE_LIFESPAN = True
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Please uncomment the below code to get data upload to databse
    # await load_data()
    yield

app = FastAPI(lifespan=lifespan if USE_LIFESPAN else None)

app.include_router(router, prefix="/location")