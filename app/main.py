from fastapi import FastAPI
from typing import Optional
from random import randint
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, vote

from . import models
from .database import engine, Base, get_db

# with alembic, we no longer need this, it used to tell sqlalchemy to create the tables but now we have alembic
# keeping it doesn't break anything but it doesn't do anything either
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world"}
