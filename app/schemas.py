from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# =================================user ============================================
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# =================================post ============================================

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResp(PostBase):
    id: int
    created: datetime
    owner_id: int
    owner: UserResp

    class Config:
        orm_mode = True

class PostVotes(PostBase):
    Post: PostResp
    votes: int

    class Config:
        orm_mode = True

# =================================Token============================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# =================================Vote============================================
class Vote(BaseModel):
    post_id: int
    direction: conint(ge=-1, le=1)