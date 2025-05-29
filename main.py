from fastapi import FastAPI
from database import *
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def getmethod():
    return {"status": True, "message": "Hey"}


# this would throw error if is present before /blog/{blog_id} as the pydantic would try to validate
# unpublished as int
@app.get("/blog/unpublished")
def blog():
    return {"status": True, "message": 34}


# to accept query parameter
@app.get("/blog/publish")
def printname(name):
    return {"status": True, "message": f"Name of the publisher is {name}"}


@app.get("/blog/{blog_id}")
def blog(blog_id: int):
    for single in mydb:
        if blog_id == single["blog"]:
            return {"status": True, "message": {"blog_name": single["name"]}}
    return {"status": False, "message": "No Blog Found For Given ID"}


class Blog(BaseModel):
    id: int
    title: str
    author: str
    published: Optional[bool]
    content: str


@app.post("/blog")
def create_blog(request: Blog):
    blog_id = request.id
    # if blog_id in 
    for blog in blog_db:
        if blog.get("id") == blog_id:
            return {"status":False,"message":"Blog already exists for same id","blog":blog}
    new_blog = request.model_dump()
    blog_db.append(new_blog)
    return {"status":True,"message":f"Blog created successfully for id {blog_id}","blog":new_blog}
    