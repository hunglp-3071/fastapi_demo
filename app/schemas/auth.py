from pydantic import BaseModel
from app.schemas.token import Token

class LoginRequestSchema(BaseModel):
  email: str
  password: str

class LoginResponseSchema(Token):
  pass

class SignUpRequestSchema(LoginRequestSchema):
  name: str