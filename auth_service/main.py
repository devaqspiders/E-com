from models.usermodel import UserModel
from database.connection import Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from router.user_route import router as user_router
from exception.password import PasswordValidationException

app = FastAPI()
app.include_router(user_router, prefix='/api/v1/user')
Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def password_exception_handler(
    request: Request,
    exc: PasswordValidationException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )