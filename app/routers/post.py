from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional

from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/", response_model=list[schemas.PostResp])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    my_posts = db.query(models.Post).all()
    return my_posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResp)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print()
    print(current_user.email)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResp)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post of id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post of id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResp)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    required_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = required_post.first()

    if not updated_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    required_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return required_post.first()
