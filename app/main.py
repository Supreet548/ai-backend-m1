from fastapi import FastAPI
from app.routes import user_routes
from contextlib import asynccontextmanager
from app.database.async_connection import create_pool
from app.middleware.logging_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await create_pool()
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(LoggingMiddleware)

app.include_router(user_routes.router)

@app.get("/")
def home():
    return {
        "message": "API is running 🚀"
    }