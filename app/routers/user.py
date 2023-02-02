from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[schemas.UserBack])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model= schemas.UserBack)
def get_user(id: int, db: Session = Depends(get_db)):
    querry = db.query(models.User).filter(models.User.id == id)

    if not querry.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} was not found!")

    user = querry.first()
    return user


@router.post("/", response_model=schemas.UserBack, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    user.password = hash_password(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    querry = db.query(models.User).filter(models.User.id == id)

    if not querry.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} was not found!")

    querry.delete()
    db.commit()

    return
