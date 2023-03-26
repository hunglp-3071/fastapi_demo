from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from app.schemas.user import User
from app.service import user as UserService
from app.service import article as ArticleService
from app.dependencies import get_db, get_current_active_user
from app.schemas.article import Article, ArticleUpdate, ArticleCreate

router = APIRouter(
    prefix="/api/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Page[Article])
def http_get_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    articles = ArticleService.get_articles(db, current_user, skip=skip, limit=limit)
    return paginate(articles)


@router.get("/{article_id}", response_model=Article)
def http_get_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_article = ArticleService.get_article(db, current_user, article_id=article_id)

    if db_article is None:
        raise HTTPException(status_code=404, detail="Not found")

    return db_article


@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
def create_user_article(
    article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return ArticleService.create_article(db=db, article=article, user_id=current_user.id)


@router.put("/{article_id}", response_model=ArticleUpdate)
def http_update_article(
    article_id: int,
    updated_fields: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_article = ArticleService.get_owner_article(db, current_user, article_id=article_id)

    if db_article is None:
        raise HTTPException(status_code=404, detail="Not found")
    return ArticleService.update_article(db, article_id, updated_fields)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def http_delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_article = ArticleService.get_owner_article(db, current_user, article_id=article_id)

    if db_article is None:
        raise HTTPException(status_code=404, detail="Not found")

    return ArticleService.delete_article(db, db_article)


add_pagination(router)