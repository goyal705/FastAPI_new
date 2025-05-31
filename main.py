from fastapi import FastAPI
from database import *
from schemas import *
from models import *
from routers import blog,user,commets

app = FastAPI()

app.include_router(commets.router)
app.include_router(blog.router)
app.include_router(user.router)

Base.metadata.create_all(engine)

@app.get("/",tags=["Startup"])
def getmethod():
    return {"status": True, "message": "Hey"}