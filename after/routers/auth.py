from starlette import status
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from email_validator import validate_email, EmailNotValidError
from models import User
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.hash import bcrypt
from jose import jwt, JWTError

router=APIRouter(prefix="/oauth",tags=["Oauth"])

class UserRequest(BaseModel):
    first_name:str
    last_name:str
    email:str
    username:str
    password:str
    role:str
    is_active:bool
    
    class Config:
        json_schema_extra={
            'example':{
                'first_name':'Sara',
                'last_name':'Mohammadi',
                'email':'s.mahammadi.com',
                'username':'Sara',
                'password':'123',
                'role':'normal user',
                'is_active':True
            }
        }
    
def get_db():
    db=SessionLocal()
    try:
        yield db 
        
    finally:
        db.close()
        
        
SECRET_KEY='b8efa28d8ccea55ca6cbce73e5770e2304fc98e5e882913c6d1f66296894bdd4'
ALGORITHM='HS256'

oauth2_bearer = OAuth2PasswordBearer('oauth/token')

db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode={'sub':username, 'id':user_id}
    expires=datetime.utcnow()+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user..")
        return {'username':username,"user_id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user..')

def oauthenticate_user(username:str,password:str,db):
    user=db.query(User).filter(username==User.username).first()
    if not user:
        return False
    if not bcrypt.verify(password,user.hashed_password):
        return False
    return user

@router.post("/token")
async def login_for_access_token(login_form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=oauthenticate_user(login_form.username,login_form.password,db)
    if not user :return {"message":"oauthentication failed.."}
    else : 
        token=create_access_token(user.username, user.id, timedelta(minutes=20))
        return {'access_token':token, 'token_type':'bearer'}

@router.post("/users/create")
async def create_user(db:db_dependency,new_user:UserRequest):
    user_dict=new_user.dict()
    password=user_dict.get('password')
    hashed_password=bcrypt.hash(password)
    del user_dict["password"]
    user_dict.update({"hashed_password":hashed_password})
    user_model=User(**user_dict)
    db.add(user_model)
    db.commit()
    return {"message":"User created","user":user_dict}


