from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app.oath2 import get_current_user
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oath2
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)): #Create a request using (get_db) for this API request

    posts = db.query(models.Post).all() #This abstracts all the sql logic away. It generates the sql query based on what we tell it we want in python
    return {'data':posts} #printing db.query(models.Post) will print out A SQL statement

#@router.get("/")
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 100, 
    skip: int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all() #old query without vote counts
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() to get posts of only logged in user
    #return {"data": my_posts}# this is a list, FastAPI will automatically serialize it and convert it into JSON
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all() #This will be a left outer join
    #print(results)
    return posts

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}
# title str, content str want user to send these things, nothing else.

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #print(current_user.email)
    new_post = models.Post(
        owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve new post that just created and store it back in variable so we can return it
    return new_post

@router.get("/{id}",response_model=schemas.PostOut) #ID field here is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)): #Get a specific post that user asks for
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()#find first instance. .all() will look through whole database - old query without vote counts

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"post with id: {id} was not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #return {'message': 'post was succesfully deteled'} #When sending a delete request, we shouldn't be sending anything back hence this line will produce an error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not authorized")
    post_query.delete(synchronize_session=False) #refer to synchronization strategies
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="Not authorized")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()