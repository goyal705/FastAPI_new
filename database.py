from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# load_dotenv()
db_pass = os.getenv("db_pass")
DATABASE_URL = f"postgresql://{db_pass}@pg-893078f-tushargoyal628-b233.d.aivencloud.com:24953/defaultdb?sslmode=require"
# DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SESSION_LOCAL = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

mydb = [
    {"blog": 1, "name": "BLog1"},
    {"blog": 2, "name": "BLog2"},
    {"blog": 3, "name": "BLog3"},
    {"blog": 4, "name": "BLog4"},
    {"blog": 5, "name": "BLog5"},
]

blog_db = [{"id":1,"title":"My First Blog","author":"Tushar","published":True,"content":"Lorem Ipsum"}]
