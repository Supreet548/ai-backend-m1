from fastapi import FastAPI
from app.routes import user_routes
from app.database.async_connection import create_pool

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_pool()

app.include_router(user_routes.router)

@app.get("/")
def home():
    return {
        "message": "API is running 🚀"
    }