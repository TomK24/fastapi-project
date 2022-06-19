from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): 
    #email and password will be stored in pydantic UserCreate object
    #hash the password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(
        **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #retrieve new post that just created and store it back in variable so we can return it
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with {id} does not exist")
    return user