from dotenv import dotenv_values
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

from app.dependencies import get_db
from app.schemas.user import UserCreate
from app.service import user as UserService
from app.routers import auth, articles

app = FastAPI()

app.include_router(auth.router)
app.include_router(articles.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/init_db")
def init_db(db: Session = Depends(get_db)) -> None:
    config = dotenv_values('.env')
    email = config['ADMIN_EMAIL']
    password = config['ADMIN_PASSWORD']

    user = UserService.get_user_by_email(db, email)

    if not user:
        user_in = UserCreate(
            email=email,
            password=password,
            is_admin=True,
        )

        UserService.create_user(db, user=user_in)
