from fastapi import APIRouter, HTTPException, Depends, status
import db_models
from sqlalchemy.orm import Session
from database import get_db
from models import UsersData, CreateUser
from typing import List
from util import hash_password
from routers.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# 1. getting all users(id,email)
@router.get("/", response_model=List[UsersData])
def get_users(db: Session = Depends(get_db), current_user: db_models.dbUser = Depends(get_current_user)):
    users = db.query(db_models.dbUser).all()
    return users


# 2. Creating the new User
@router.post("/", response_model=UsersData, status_code=status.HTTP_201_CREATED)
def creating_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = db_models.dbUser(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UsersData)
def read_current_user(current_user: db_models.dbUser = Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=UsersData)
def getUser_byId(id: int, db: Session = Depends(get_db), current_user: db_models.dbUser = Depends(get_current_user)):
    user = db.query(db_models.dbUser).filter(db_models.dbUser.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry! No User found with that id number: {id}")

    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user")

    return user
    
