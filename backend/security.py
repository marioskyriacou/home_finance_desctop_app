from datetime import datetime, timezone, timedelta
from typing import Annotated

import bcrypt
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
	return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
	try:
		return bcrypt.checkpw(password.encode(), hashed_password.encode())
	except ValueError:
		return False

def create_access_token(username:str)-> str:
	expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

	return jwt.encode({"sub": username, "exp": expire},
					  settings.secret_key, algorithm=ALGORITHM)

def get_current_user(
		token: Annotated[str, Depends(oauth2_scheme)],
		db: Annotated[Session, Depends(get_db)]) -> User:

	unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
								 detail="Could not validate credentials",
								 headers={"WWW-Authenticate": "Bearer"})

	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
	except jwt.ExpiredSignatureError:
		raise unauthorized

	user = db.scalar(select(User).where(User.username == payload.get("sub")))

	if user is None:
		raise unauthorized

	return user
