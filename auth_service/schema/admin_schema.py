from pydantic import BaseModel, EmailStr

class GetUserResponse(BaseModel):
    name: str 
    email: EmailStr
    role: str
    model_config = {
        "from_attributes": True
    }

class ModifyUser(BaseModel):
    name : str | None = None
    email : EmailStr | None = None
    role : str | None = None

    model_config={
        "from_attributes": True
    }