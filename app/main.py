from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from decouple import config
from .routers import post, users, auth

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

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
