from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey

class Todo(Base):
    __tablename__='todos'
    
    id=Column(Integer,primary_key=True, index=True)
    title=Column(String)
    description =Column(String)
    priority =Column(Integer)
    completed=Column(Boolean,default=False)
    owner_id=Column(Integer, ForeignKey("users.id"))
    
    
class User(Base):
    __tablename__='users'
    
    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String,unique=True)
    username=Column(String,unique=True)
    hashed_password=Column(String)
    role=Column(String)
    is_active=Column(Boolean,default=True)