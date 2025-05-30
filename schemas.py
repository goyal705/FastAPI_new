from typing import Optional,List
from pydantic import BaseModel,field_validator,EmailStr
from datetime import datetime
import re

class Blogs(BaseModel):
    # id: int
    title: str
    author: int
    published: Optional[bool]
    content: str
    
# class ShowBlog(Blogs):
#     class Config():
#         orm_mode = True

class User(BaseModel):
    name: str
    username: str
    mobile: int
    email: str
    password: str
    role: str

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v):
        v_str = str(v)
        if not re.match(r"^[6-9]\d{9}$", v_str):
            raise ValueError("Mobile number must be 10 digits and start with 6-9")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z]{5,}[0-9]{3,}$", v):
            raise ValueError("Username must start with at least 5 letters and end with at least 3 digits")
        return v

class UserOut(BaseModel):
    user_id: int
    name: str
    username: str
    mobile: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class AuthorResponse(BaseModel):
    # user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class BlogResponse(BaseModel):
    id: int
    title: str
    published: bool
    context: str
    # author: int
    user: AuthorResponse  # This will pull the author details

    class Config:
        orm_mode = True
        
class BlogsUser(BaseModel):
    author: AuthorResponse
    blogs:List[BlogResponse]
    
    class Config:
        orm_mode = True
        
class Login(BaseModel):
    username:str
    password:str
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    user_id:int
    role:str