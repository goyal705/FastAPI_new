from fastapi import FastAPI
 
app = FastAPI()
 
@app.get('/')
def getmethod():
    return {"status":True,"message":"Hey"}
 
#this would throw error if is present before /blog/{blog_id} as the pydantic would try to validate
#unpublished as int
@app.get('/blog/unpublished')
def blog():
    return {"status":True,"message":34}
 
#to accept query parameter
@app.get('/blog/publish')
def printname(name):
    return {"status":True,"message":f"Name of the publisher is {name}"}
 
@app.get('/blog/{blog_id}')
def blog(blog_id:int):
    return {"status":True,"message":blog_id}