from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import LoginRequestSchema, LoginResponseSchema, SignUpRequestSchema
from app.service.auth import authenticate_user, create_access_token

from app.models.database import UserRepositories

from app.dependencies import get_db

router = APIRouter(prefix="/auth")

@router.post("/signup", response_model=str)
def signup(
  form_data: SignUpRequestSchema,
  db: Session = Depends(get_db)
):
  existed_user = UserRepositories(db).get_user_by_email(form_data.email)
  if existed_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  user = UserRepositories(db).create_user(user=form_data)

  return "Success"

@router.post("/signin", response_model=LoginResponseSchema)
def signin(
  form_data: LoginRequestSchema,
  db: Session = Depends(get_db)
) -> LoginResponseSchema:
  user = authenticate_user(form_data.email, form_data.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token({"sub": user.email})

  return access_token

# duplicate signin, using for docs
@router.post("/token", response_model=LoginResponseSchema)
def token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
) -> LoginResponseSchema:
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token({"sub": user.email})

  return access_token