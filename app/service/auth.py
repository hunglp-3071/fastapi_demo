from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.service.base import BaseServices
from app.dependencies import get_db

from app.schemas.auth import LoginResponseSchema



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

ACCESS_TOKEN_EXPIRE_MINUTES = 1440
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8abcd"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str , password: str, db: Session = Depends(get_db)):
  user = UserRepositories(db).get_user_by_email(email)
  if not user:
      return False
  if not verify_password(password, user.hashed_password):
      return False
  return user

def create_access_token(data: dict):
  token_expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode = data.copy()
  to_encode.update({"exp": token_expire_time})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return LoginResponseSchema(access_token=encoded_jwt,token_type="bearer",expires_in=token_expire_time)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = UserRepositories(db).get_user_by_email(email)
  if user is None:
    raise credentials_exception
  return user