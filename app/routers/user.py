from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/get-all-users", response_model=schemas.UserOut)
def get_all_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no user))) ")
    print(user)

    return user


@router.get("/get-user/{id}", response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    # db_user = crud.get_user(db, user_id=id)

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} id was not found.")

    return user


@router.post("/create-user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    user_data.password = utils.hash(user_data.password)

    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with {user_data.email} email address already exists.")

    new_user = models.User(**user_data.dict())

    db.add(new_user)
    db.commit()
    # returning *
    db.refresh(new_user)

    return new_user


