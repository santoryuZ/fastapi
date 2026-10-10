from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # If user desnt provides this value then it will be set to True by default.

class PostCreate(PostBase):
    pass



""" Response Models"""

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # title: str
    # content: str
    # published: bool

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    # class Config:
    #     from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]