
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post_votes])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=  None, search: Optional[str]="", skip:int=0):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()
    results  =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id  == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

 
    return results



@router.get("/my-posts", response_model=  List[schemas.PostsBack])
def get_my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    my_post_queery = db.query(models.Post).filter(models.Post.user_id == current_user.id)

    if not my_post_queery.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"no post found for user {current_user.name}")
    
    return  my_post_queery.all()


@router.get("/{id}", response_model=schemas.Post_votes)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)

    if post_querry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found!")

    result  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    return result


@router.post("/", response_model=schemas.PostsBack, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.patch("/{id}")
def update_post(post: schemas.Post, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)

    if post_querry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found!")

    if post_querry.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized the perform the action")
           
   
    post_querry.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_querry.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if post_querry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found!")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized the perform the action")

    post_querry.delete(synchronize_session=False)
    db.commit()

    return
