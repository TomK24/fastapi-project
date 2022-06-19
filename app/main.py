# from turtle import title
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,user, auth, vote
from .config import settings



#models.Base.metadata.create_all(bind=engine) #this line actually creates the tables, if any are not present on the database
# The above line is now not needed as Alembic will create the tables we need according to whats in the models.py file
app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
###Difference between Pydantic and ORM model###
#The Post class in the schemas.py file is an extension of the pydantic library base model. This is our schema. This is being referenced in our path operation eg post: Post, this snippit saves the pydantic model into a variable named post.
#The other model in models.py. This is SQLalchemy model that defines what the specific database and table look like
#So: Schema/pydantic model defines the structure of a request and a response. We can define exactly what request should look like and define exactly what a response should look like. Can define a model to dictate exactly what fields to send back, don't always want to return all fields. 
#The ORM model defines the columns for our table in postgres. It us used to perform queries and create delete update etc. fundamentally different to pydantic model. Technically we dont need pydantic model, but it really helps us ensure the data we get in is exactly what we expect
###

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "fav foods", "content": "PIZZA", "id": 2}]


app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)#include all the path operations/routes and look for a match We use these router objects to break our code into separate files.
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



