from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class CommentIn(BaseModel):
    author: str
    content: str

    class Config:
        orm_mode = True

class CommentOut(CommentIn):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True