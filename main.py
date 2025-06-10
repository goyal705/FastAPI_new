from fastapi import FastAPI
from database import *
from schemas import *
from models import *
from routers import blog,user,commets,admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(admin.router)
app.include_router(commets.router)
app.include_router(blog.router)
app.include_router(user.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

@app.get("/",tags=["Startup"])
def getmethod():
    return {"status": True, "message": "Hey this is after another deployment"}