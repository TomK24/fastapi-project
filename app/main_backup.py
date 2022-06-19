# from turtle import title
from ast import Raise
from email.policy import HTTP
from random import Random
from tkinter.messagebox import NO
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from requests import session
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post,user, auth

models.Base.metadata.create_all(bind=engine) #this line actually creates the tables, if any are not present on the database

app=FastAPI()

###Difference between Pydantic and ORM model###
#The Post class in the schemas.py file is an extension of the pydantic library base model. This is our schema. This is being referenced in our path operation eg post: Post, this snippit saves the pydantic model into a variable named post.
#The other model in models.py. This is SQLalchemy model that defines what the specific database and table look like
#So: Schema/pydantic model defines the structure of a request and a response. We can define exactly what request should look like and define exactly what a response should look like. Can define a model to dictate exactly what fields to send back, don't always want to return all fields. 
#The ORM model defines the columns for our table in postgres. It us used to perform queries and create delete update etc. fundamentally different to pydantic model. Technically we dont need pydantic model, but it really helps us ensure the data we get in is exactly what we expect
###

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "fav foods", "content": "PIZZA", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(auth.router)
app.include_router(user.router)#include all the path operations/routes and look for a match We use these router objects to break our code into separate files.

@app.get("/")
def root():
    return {"message": "Hello World"}



