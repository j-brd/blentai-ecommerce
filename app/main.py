from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth, product, order
from fastapi import FastAPI, Request
from app.core.exceptions import InvalidTokenError, UserNotFoundError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="API E-commerce",
    description="API Backend E-commerce (register/login only)",
    version="1.0.0"
)

@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

# Register des routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(order.router)