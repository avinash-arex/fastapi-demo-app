from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import UserLogin
import db_models
from util import verify_password
from Oauth2 import create_jwt_token

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(db_models.dbUser).filter(db_models.dbUser.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential's")
    
    elif verify_password(user_credentials.password,user.password) is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential's")
    
    else:
        jwt_token = create_jwt_token(
                                        data={
                                            "user_id":user.id,
                                            "user_email":user.email
                                            }
                                    )
        return {"token" : jwt_token, "token_type" :"bearer"}



