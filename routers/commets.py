from fastapi import Depends,Response,status,HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from database import *
from schemas import *
from models import *
from .token import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Comments"],
    prefix='/comments'
)

@router.get("/")
def get_all_blogs(blog_id:int,request: Request, db: Session=Depends(get_db)):
    blog = db.query(Blog).filter(
        Blog.id == blog_id
    ).first()
    return {"status":True,"data":blog.comments if blog else []}

@router.post("/new-comment")
def add_new_comment(response: Response,comment:Comment,request: Request, _=Depends(verify_access_token), db: Session=Depends(get_db)):
    user_id = request.state.user_data.get("user_id")
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        response.status_code = 404
        return {"status":False,"message":"User not found"}
    
    blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
    if not blog:
        response.status_code = 404
        return {"status":False,"message":"Blog not found"}
    
    new_comment = Comments(publisher_name=user.name,title=comment.title,blog_id=blog.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return {"status": True, "message": "Comment added", "data": {
        "id": new_comment.id,
        "title": new_comment.title,
        "publisher_name": new_comment.publisher_name,
        "created_at": new_comment.created_at
    }}
    