from fastapi import APIRouter, Depends, HTTPException
from schema.user_schema import CreateUser, LogInUser
from database.connection import Session
from database.dependencies import get_db
from models.usermodel import UserModel
from auth.password import hash_password, verify_password

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
            return {'message':'login successfull'}
        else:
            raise HTTPException(status_code=401, detail='password')
    else:
        raise HTTPException(status_code=401, detail='invalid username or emailid')
    