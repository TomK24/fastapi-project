# from turtle import title
from email.policy import HTTP
from random import Random
from tkinter.messagebox import NO
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "fav foods", "content": "PIZZA", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#Create A class for post that extends on the pydantic base model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #If user doesn't provide published - will default to true
    rating: Optional[int] = None #This is a fully optional field. If user doesn't provide it will default to None
# take this model and put it in the create posts method

try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='1234', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('database connection was successful')
except Exception as error:
    print('connection failed')
    print("Error: ", error)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    #return {"data": my_posts}# this is a list, FastAPI will automatically serialize it and convert it into JSON
    return {'data': posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}
# title str, content str want user to send these things, nothing else.

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):#Pass fastAPI the post pydantic model. FastAPI will automatically validate data recieved.
             #The new_post object is a pydantic model of class Post
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s ) RETURNING *""", (post.title,post.content,post.published)) #Usage of fstrings here would make system vulnerable to sql injection. By using this method we ensure our sql library 'sanitizes' the inputs
    new_post = cursor.fetchone() #fetches the post we just created and saves into variable
    conn.commit() #This is when the actual changes to the database are made (the post is added)
    return {"data":new_post}

@app.get("/posts/{id}") #ID field here is a path parameter
def get_post(id: int, response: Response): #Get a specific post that user asks for
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #return {'message': 'post was succesfully deteled'} #When sending a delete request, we shouldn't be sending anything back hence this line will produce an error
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updated_post}