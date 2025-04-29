from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.schemas.comments import CommentBase


class PostBase(BaseModel):
    title: str = Field(..., example="My First Blog Post")
    content: str = Field(..., example="This is the content of the post.")
    photo: Optional[str] = Field(None, example="https://example.com/image.jpg")

class LikeUpdate(BaseModel):
    likes: int

class PostOut(PostBase):
    id: int
    likes: int
    views: int
    photo: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    comments: List[CommentBase]

    class Config:
        orm_mode = True