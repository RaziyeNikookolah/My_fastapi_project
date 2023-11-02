import pydantic
import datetime


class UserBase(pydantic.BaseModel):
    email:str
    name:str
    phone:str
    
    
class UserRequest(UserBase):
    password:str
    
    class Config:
        orm_mode=True
        
        
class UserResponse(UserBase):
    id:int
    created_at:datetime.datetime
    class Config:
        orm_mod=True
        
        
class PostBase(pydantic.BaseModel):
    # user_id:int
    post_title:str
    post_description:str
    post_image:str
    
class PostRequest(PostBase):
    