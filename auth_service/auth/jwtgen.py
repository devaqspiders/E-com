from jose import jwt
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os

load_dotenv()

ACC_EXPIRE = os.getenv("ACC_EXPIRE")
REFRESH_EXPIRE = os.getenv("REFRESH_EXPIRE")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(**data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=int(ACC_EXPIRE))
    to_encode['exp'] = expire
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_refresh_token(**data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=int(REFRESH_EXPIRE))
    to_encode['exp'] = expire
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )