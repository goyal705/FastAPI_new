from datetime import datetime, timedelta, timezone
from database import *
from sqlalchemy import Column,Integer,String,Boolean,Text,DateTime,BigInteger,ForeignKey
from sqlalchemy.sql import func
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    author = Column(Integer,ForeignKey("users.user_id"))
    published = Column(Boolean)
    context = Column(Text)
    user = relationship("Users", back_populates="blogs")
    comments = relationship("Comments",back_populates="blog", cascade="all, delete-orphan")
    #BLog.user gives full Users object
    
class Comments(Base):
    __tablename__ = "comments"
    
    id = Column(Integer,primary_key=True,index=True)
    publisher_name = Column(String)
    title = Column(String)
    blog_id = Column(Integer,ForeignKey("blogs.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    blog = relationship("Blog",back_populates="comments")

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    mobile = Column(BigInteger, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True) #default is true
    
    blogs = relationship("Blog", back_populates="user", cascade="all, delete-orphan")
    otp = relationship("OtpRecords", back_populates="user")
    #same Users.blogs gives all the blog objects for the user object


    def set_password(self, plain_password: str):
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.password)

class OtpRecords(Base):
    __tablename__ = "otprecords"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.user_id"))
    mobile_no = Column(BigInteger)
    otp = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expire_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(minutes=15))
    
    user = relationship("Users",back_populates="otp")