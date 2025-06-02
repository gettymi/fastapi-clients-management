from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

BASE =declarative_base()

class Client(BASE):

    __tablename__='clients'

    id =  Column(Integer,primary_key=True,unique=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    phone_number = Column(String,nullable=False)

class User(BASE):
    __tablename__='users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,index=True)
    hashed_password = Column(String,nullable=False)
    role = Column(String,default="user")