"""
SQL Tables.
"""
from datetime import datetime
from sqlalchemy import DateTime, Text, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
	hashed_password: Mapped[str] = mapped_column(String(255))

class Item(Base):
	__tablename__ = 'items'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100))
	description: Mapped[str] = mapped_column(Text, default="")
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), )
	owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index = True) # links each item to the user who owns it.




