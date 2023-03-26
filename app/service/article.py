from sqlalchemy import update
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.database import Base
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


def get_articles(db: Session, user: User, skip: int = 0, limit: int = 100):
    if not user.is_admin:
        return db.query(Article).filter(Article.author_id == user.id).offset(skip).limit(limit).all()

    return db.query(Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: ArticleCreate, user_id: int):
    db_item = Article(**article.dict(), author_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_owner_article(db: Session, user: User, article_id: int):
    if not user.is_admin:
        return db.query(Article).filter(Article.author_id == user.id).filter(Article.id == article_id).first()
    return db.query(Article).filter(Article.id == article_id).first()


def get_article(db: Session, user: User, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def update_article(db: Session, article_id: int, updated_fields: ArticleUpdate):
    db.execute(
        update(Article)
        .where(Article.id == article_id)
        .values(updated_fields.dict(exclude_unset=True))
    )
    db.flush()
    db.commit()
    return updated_fields


def delete_article(db: Session, article: Article):
    db.delete(article)
    db.commit()