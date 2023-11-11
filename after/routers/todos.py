
from typing import Annotated, Optional
from database import engine, Base,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from fastapi import APIRouter,Depends, Path, HTTPException
from models import Todo
from starlette import status
from .auth import get_current_user

router=APIRouter(prefix="/todos",tags=["Todos"])

def get_db():
    db=SessionLocal()
    try:
        yield db 
        
    finally:
        db.close()
        
        
class TodoRequest(BaseModel):
    title:str=Field(min_length=2,description="Todo Title")
    description:str=Field(max_length=1000,min_length=2,description="Todo Description")
    priority :int=Field(lt=6,ge=1,description="Priority of Todo")
    completed:bool=Field(False,description="Todo Completed or not")
    
    class Config:
        json_schema_extra={
            'example':{
                'title':'A new todo',
                'description':'todo sample description',
                'priority':1,
                'completed':False
            }
        }
    

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]

@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create(user:user_dependency, db:db_dependency,new_todo:TodoRequest):
    user_dict=new_todo.dict()
    user_dict.update({"owner_id":user["user_id"]})
    todo_model=Todo(**user_dict)
    db.add(todo_model)
    db.commit()


@router.put("/update",status_code=status.HTTP_204_NO_CONTENT)
async def update(user:user_dependency, db:db_dependency,new_todo:TodoRequest,old_todo_id=Path(gt=0)):
    todo=db.query(Todo).filter(Todo.id==old_todo_id).first()
    if todo and todo.owner_id==user["user_id"]:       
        result=db.query(Todo).filter(Todo.id==old_todo_id).update(new_todo.dict(),synchronize_session=False)
        db.commit()
    
    if not todo:
        raise HTTPException(status_code=404,detail="Not found")   
    if todo.owner_id!=user["user_id"]:
        raise HTTPException(status_code=403,detail="Not allowed") 

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Todo).all()
    
@router.get("/{todo_id}",status_code=status.HTTP_200_OK)
async def todo_detail(db:db_dependency,todo_id:int=Path(gt=0)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if todo is not None:
        return todo  
    else: raise HTTPException(status_code=404,detail="Not exsist...")


@router.delete("/{todo_id}")
async def delete(db:db_dependency,todo_id:int=Path(gt=0)):
    result=db.query(Todo).filter(Todo.id==todo_id).delete()
    db.commit()
    if result==0:
        raise HTTPException(status_code=404,detail="Not found")    
    