from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship

#This script creates postgres SQL tables using SQL alchemy. 

class Post(Base): #This will create a table in our database called 'posts' with all the correct columns below
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)#We want the sql server to set the value here
    created_at =Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User") #automatically create post property fetch user from User table based on owner_id


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)