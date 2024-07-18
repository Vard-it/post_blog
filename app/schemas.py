from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        # orm_mode = True
        from_attributes = True


class PostCreate(PostBase):
    pass


# Response schema, from postbase there will be title content, published
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True


class PostOut(PostBase):
    post_id: int
    votes: int

    class Config:
        # orm_mode = True
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

