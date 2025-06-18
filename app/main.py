from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth

app = FastAPI(
    title="API E-commerce",
    description="API Backend E-commerce (register/login only)",
    version="1.0.0"
)

# Register des routers
app.include_router(auth.router)