from fastapi import FastAPI
from routes import base
from routes import data
from motor.motor_asyncio import AsyncMetorClient
from helpers.config import get_settings



app = FastAPI()

@app.onevent('startup')
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn = AsyncMetorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]


@app.onevent('shutdown')
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(base.base_router)

app.include_router(data.data_router)
