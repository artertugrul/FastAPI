from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_querry = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote  = vote_querry.first()

    post_querry = db.query(models.Post).filter(models.Post.id ==  vote.post_id)
    post = post_querry.first()

    if post:
        if (vote.dir == 1):
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail=f"user {current_user.id }  already voted on {vote.post_id}")

            new_vote = models.Vote(post_id = vote.post_id, user_id= current_user.id)
            db.add(new_vote)
            db.commit()
            return  {"message": "successfully voted"}
        elif not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Vote does not exist")
        
        else:
            if not   found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Vote does not exist")
            vote_querry.delete(synchronize_session=False)
            db.commit()

            return {"message":  "vote  deleted!"}
    else:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"post does not exist")





        