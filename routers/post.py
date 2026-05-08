# routers/post.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Post, RequiredUpdate, ResponsePost, ResponseById
from database import get_db
import db_models
from routers.auth import get_current_user

router = APIRouter(tags=["Post's"])


# 1. Get all posts
@router.get("/posts", response_model=List[ResponsePost])
def get_posts(db: Session = Depends(get_db), current_user: db_models.dbUser = Depends(get_current_user)):
    posts = db.query(db_models.dbPost).order_by(db_models.dbPost.id).all()
    return posts


# 2. Create new post
@router.post("/post", status_code=status.HTTP_201_CREATED)
def new_post(newPost: Post, db: Session = Depends(get_db)):
    newPost_Obj = db_models.dbPost(**newPost.model_dump())
    db.add(newPost_Obj)
    db.commit()
    db.refresh(newPost_Obj)
    return {"message": "New Post Added", "data": newPost_Obj}


# 3. Get post by ID
@router.get("/post/{id}", response_model=ResponseById)
def getpost_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(db_models.dbPost).filter(db_models.dbPost.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post NOT found with ID {id}"
        )
    return post

        
#4 Deleting the post by id
deleted_ids = set()
@router.delete("/post/{id}")
def deletePost_byId(id:int, db:Session = Depends(get_db)):
    
    post = db.query(db_models.dbPost).filter(db_models.dbPost.id == id)
    post_id = id

    # Case 1: Post exists → delete it
    if post.first() is not None:
        deleted_ids.add(post_id)
        post.delete(synchronize_session=False)
        # post.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post deleted successfully"}
    
    # Case 2: Already deleted before
    elif id in deleted_ids:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    # Case 3: Never existed
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found! to delete")


# 5. Full Update (PUT)
@router.put("/post/{id}")
def full_update(id:int, post:Post, db : Session = Depends(get_db)):
    
    query = db.query(db_models.dbPost).filter(db_models.dbPost.id == id)
    existing_post = query.first()
    if existing_post is not None:
        #updating data in DB

        query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        update_post = query.first()
        return{"message":"Post Updated Successfully",
               "Updated Post":update_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not FOUND! so can't Update!")

# 6. Partial Update(PATCH)
@router.patch("/posts/{id}")
def partial_update(id:int,post:RequiredUpdate, db : Session = Depends(get_db)):

    query = db.query(db_models.dbPost).filter(db_models.dbPost.id == id)
    existing_post = query.first()


    if existing_post is not None:

        query.update(post.model_dump(exclude_unset = True), synchronize_session=False)
        db.commit()
        updated_post = query.first()
        return{"Message":"Updated the Required Field's",
               "Partial_Updated_data":updated_post }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not FOUND! so can't Update!")
