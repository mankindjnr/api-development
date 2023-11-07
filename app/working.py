from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from decouple import config

from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, Base, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


host = config('HOST')
database = config('DATABASE')
user = config('USER')
password = config('PASSWORD')

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="mankindjnr", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABSE CONN IS A SUCCESS")
        break
    except Exception as error:
        print("DATABSE CONN IS A FAILURE", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=list[schemas.PostResp])
def get_posts(db: Session = Depends(get_db)):
    my_posts = db.query(models.Post).all()
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResp)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResp)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post of id {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post of id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResp)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    required_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = required_post.first()

    if not updated_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    required_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return required_post.first()


# =================================USER MANAGEMENT============================================

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResp)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User of id {id} not found")
    return user