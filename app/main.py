from fastapi import FastAPI
from app.routes import user_routes
from contextlib import asynccontextmanager
from app.database.async_connection import create_pool
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.exception_middleware import ExceptionMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await create_pool()
    yield

app = FastAPI(
    title="AI Backend API",
    description="Production-ready FastAPI backend",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(ExceptionMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(user_routes.router)

@app.get("/")
def home():
    return {
        "message": "API is running 🚀"
    }