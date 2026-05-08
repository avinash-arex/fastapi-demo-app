from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import db_models
from util import verify_password
from Oauth2 import create_jwt_token, oauth2_scheme, verify_access_token

router = APIRouter(tags=["Authentication"])


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_access_token(token)
    user = db.query(db_models.dbUser).filter(db_models.dbUser.id == token_data["user_id"]).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.dbUser).filter(db_models.dbUser.email == user_credentials.username).first()

    if user is None or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    jwt_token = create_jwt_token(
        data={
            "user_id": user.id,
            "user_email": user.email
        }
    )
    return {"access_token": jwt_token, "token_type": "bearer"}



