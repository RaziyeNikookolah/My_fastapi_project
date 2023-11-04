from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel ,Field

app=FastAPI()
books=[]


class BookRequest(BaseModel) :
    id :Optional[int]=Field(None,
        title='id is optional',
        description='unique field')
    title:str=Field(max_length=150,min_length=1)
    author:str=Field(max_length=150,min_length=1)
    page_count:int=Field(gt=5,lt=1000)
    class Config:
        json_schema_extra={
            'example':{
                'title':'A new book',
                'author':'me',
                'page_count':100
            }
        }
    

@app.get("/posts/{param}/")
async def get_posts(param,text):
    return {"book1":param,"book2":text}


@app.post("/create")
def create_book(new_book=Body()):
    books.append(new_book)
    return {"message":"created"}


@app.post("/books/create_new_book")
def create_book2(new_book:BookRequest):
    book_dict=new_book.dict()
    if not book_dict["id"] :
        book_dict.update({"id":1 if len(books)==0 else books[-1]["id"]+1})
    books.append(book_dict)
    return book_dict

  
@app.get("/books/get_all_books")
def get_all_books():
    return books