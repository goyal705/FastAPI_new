from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
db_pass = os.getenv("db_pass")
# print("db_pass",db_pass)
db_pass = "AVNS_i4-D6sp7v-GJggvkclF"
DATABASE_URL = os.environ.get("DATABASE_URL").format(db_pass)

engine = create_engine(DATABASE_URL)
SESSION_LOCAL = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

mydb = [
    {"blog": 1, "name": "BLog1"},
    {"blog": 2, "name": "BLog2"},
    {"blog": 3, "name": "BLog3"},
    {"blog": 4, "name": "BLog4"},
    {"blog": 5, "name": "BLog5"},
]

blog_db = [{"id":1,"title":"My First Blog","author":"Tushar","published":True,"content":"Lorem Ipsum"}]
