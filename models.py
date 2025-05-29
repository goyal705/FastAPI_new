from database import *
from sqlalchemy import Column,Integer,String,Boolean,Text,DateTime,BigInteger
from sqlalchemy.sql import func
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    author = Column(String)
    published = Column(Boolean)
    context = Column(Text)

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

    def set_password(self, plain_password: str):
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.password)

