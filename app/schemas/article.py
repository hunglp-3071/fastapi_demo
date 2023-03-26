from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    body: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ArticleUpdate(BaseModel):
    title: Optional[str]
    body: Optional[str]

    class Config:
        orm_mode = True