from fastapi import FastAPI,Depends, Query, Response,status,HTTPException
from database import *
from schemas import *
from models import *
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def getmethod():
    return {"status": True, "message": "Hey"}


# # this would throw error if is present before /blog/{blog_id} as the pydantic would try to validate
# # unpublished as int
# @app.get("/blog/unpublished")
# def blog():
#     return {"status": True, "message": 34}


# # to accept query parameter
# @app.get("/blog/publish")
# def printname(name):
#     return {"status": True, "message": f"Name of the publisher is {name}"}


@app.get("/blogs/{blog_id}")
def blog(blog_id: int,db: Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id==blog_id).first()
    return {"status":True,"data":blog if blog else []}

@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create_blog(request: Blogs ,db: Session=Depends(get_db)):
    new_blog = Blog(title=request.title,author=request.author,published=request.published,context=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#need to learn response_model separately
@app.get("/blog")
def get_blogs(response: Response,id: Optional[int] = Query(None), db: Session=Depends(get_db)):
    if id is None:
        blogs = db.query(Blog).all()
        if not blogs:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status":False,"data":[],"message":"No Blogs Found"}
        return {"status":True,"data":blogs,"message":"Blogs Found"}
    else:
        blog = db.query(Blog).filter(Blog.id==id).first()
        if not blog:            
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status":False,"data":[],"message":f"No Blog Found for id {id}"}
        return {"status":True,"data":blog}
            
@app.delete("/blog/{blog_id}",status_code=status.HTTP_204_NO_CONTENT)
def destory_db(blog_id: int, db: Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    db.delete(blog)
    db.commit()
    
    return {"status": True, "message": f"Blog with id {blog_id} deleted successfully"}

@app.put("/blog", status_code=status.HTTP_202_ACCEPTED)
def update_krdo(blog: Blogs, db: Session = Depends(get_db)):
    existing_blog = db.query(Blog).filter(Blog.title == blog.title).first()
    if not existing_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with title '{blog.title}' not found"
        )
    
    existing_blog.author = blog.author
    existing_blog.published = blog.published
    existing_blog.context = blog.content

    db.commit()
    db.refresh(existing_blog)

    return {
        "status": True,
        "message": f"Blog '{blog.title}' updated successfully",
        "data": {
            "id": existing_blog.id,
            "title": existing_blog.title,
            "author": existing_blog.author,
            "published": existing_blog.published,
            "content": existing_blog.context,
        }
    }

@app.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user(request:User, response: Response ,db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == request.username) |
        (Users.email == request.email) |
        (Users.mobile == request.mobile)
    ).first()
    
    if existing_user:
        if existing_user.username == request.username:
            detail = "User with same username already exists"
        elif existing_user.email == request.email:
            detail = "User with same email already exists"
        elif existing_user.mobile == request.mobile:
            detail = "User with same mobile number already exists"
        else:
            detail = "Duplicate user"

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": False, "message": detail}
    
    new_user = Users(
        name=request.name,
        username=request.username,
        mobile=request.mobile,
        email=request.email,
        role=request.role
    )
    
    new_user.set_password(request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
# hhahahaha