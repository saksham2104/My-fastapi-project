from fastapi import FastAPI
from app.db.connector import database
from app.routers import names

app = FastAPI()

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()

app.include_router(names.router, prefix="/api")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
