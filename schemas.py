from pydantic import BaseModel, EmailStr,constr

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: constr(pattern=r'^\d+$')

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password: constr(min_length=8)