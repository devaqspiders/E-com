from fastapi import APIRouter, Depends, HTTPException, Response
from schema.user_schema import CreateUser, LogInUser, RefreshTokenRequest
from database.connection import Session
from database.dependencies import get_db
from models.usermodel import UserModel
from auth.password import hash_password, verify_password
from auth import jwtgen
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from auth.jwtgen import create_access_token
from auth.security import get_current_user


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

load_dotenv()
router = APIRouter()

@router.post('/signup')
def signup(user: CreateUser, db: Session=Depends(get_db)):
    user = UserModel(name=user.name, email=user.email, hashed_password=hash_password(user.password))
    db.add(user)
    db.commit()
    return {"message":"user created"}

@router.post('/login')
def login(user: LogInUser, db: Session=Depends(get_db)):
    db_user = db.query(UserModel).filter((UserModel.email==user.username) | (UserModel.name==user.username)).first()
    if db_user is not None:
        if verify_password(user.password, db_user.hashed_password):
            access_token = jwtgen.create_access_token(id=str(db_user.id), name=db_user.name, role=db_user.role, email=db_user.email)
            refresh_token=jwtgen.create_refresh_token(id=str(db_user.id), name=db_user.name, role=db_user.role, email=db_user.email)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            }
        else:
            raise HTTPException(status_code=401, detail='password')
    else:
        raise HTTPException(status_code=401, detail='invalid username or emailid')
    
@router.post('/refresh')
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            request.refresh_token,
            SECRET_KEY,
            ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh Token"
        )
    req_token = create_access_token(
        id=payload['id'],
        name=payload['name'],
        role=payload['role'],
        email=payload['email']
    )
    return {"access_token":req_token}

@router.get('/profile')
def profile(payload: dict=Depends(get_current_user)):
    return payload

@router.get('/logout')
def logout(payload: dict=Depends(get_current_user)):
    return Response({'message':'logout successfull'},status_code=200)
