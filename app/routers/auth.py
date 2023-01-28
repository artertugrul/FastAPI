
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db
from ..utils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model= schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" Invalid credentials E")

    if verify_password(user_credential.password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f" Invalid credentials P")

    token = oauth2.create_acces_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}

