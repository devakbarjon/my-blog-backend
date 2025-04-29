from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    description: str
    link: HttpUrl


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    link: Optional[HttpUrl] = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True