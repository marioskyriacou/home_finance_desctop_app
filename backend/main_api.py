from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import Token, UserOut, ItemOut, ItemCreate
from .security import get_current_user, verify_password
from .database import Base, engine, get_db
from .models import User, Item




@asynccontextmanager
async def lifespan(app:FastAPI):
	Base.metadata.create_all(bind=engine)
	yield
app = FastAPI(title="Desktop API", lifespan=lifespan)

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/health")
def health():
	return {"status": "ok"}


@app.post("/auth/login", response_model = Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db:DbSession):

	user = db.scalar(select(User).where(User.username == form.username))

	if (user is None) or  not verify_password(form.password, user.hashed_password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password")

	return Token(access_token=user.access_token)

@app.get("/auth/me", response_model=UserOut)
def me(user:CurrentUser):
	return user

@app.get("items", response_model=list[ItemOut])
def list_items(user:CurrentUser, db:DbSession):
	stmt = select(Item).where(Item.owner_id == user.id).order_by(Item.id.desc())
	return db.scalar(stmt).all()


@app.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(data:ItemCreate, db:DbSession, user:CurrentUser):
	item = Item(name = data.name.strip(),
				description = data.description.strip(),
				owner_id = user.id)
	db.add(item)
	db.commit()
	db.refresh(item)
	return item