from fastapi import Depends, Query, Response,status,HTTPException,APIRouter
from database import *
from schemas import *
from models import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Blogs"],
    prefix="/blogs"
)

@router.get("/user",response_model=BlogsUser)
def get_blogs_per_user(user_id:int,db: Session = Depends(get_db)):
    user = db.query(Users).filter(
        Users.user_id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for userid {user_id}"
        )
    return {
        "author": user,
        "blogs": user.blogs
    }

@router.get("/")
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

@router.get("/{blog_id}")
def blog(blog_id: int,db: Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id==blog_id).first()
    return {"status":True,"data":blog if blog else []}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=BlogResponse)
def create_blog(request: Blogs ,db: Session=Depends(get_db)):
    new_blog = Blog(title=request.title,author=request.author,published=request.published,context=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete("/{blog_id}",status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/", status_code=status.HTTP_202_ACCEPTED)
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