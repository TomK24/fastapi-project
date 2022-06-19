from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

from app.database import Base


#Create A class for post that extends on the pydantic base model
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True #If user doesn't provide published - will default to true
    #rating: Optional[int] = None #This is a fully optional field. If user doesn't provide it will default to None
# take this model and put it in the create posts method

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass #inherits everything from postbase.

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Post(PostBase): #response model
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #new property called owner that will return a pydantic model type called UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel): #response model got the get posts request when performing a join to get votes for each post
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #schema will only accept 1 or less