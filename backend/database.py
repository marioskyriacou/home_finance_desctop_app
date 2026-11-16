from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings


# create URL where the base is and how to login
DB_URL = URL.create(
	drivername='postgresql+psycopg',
	database=settings.db_name,
	username=settings.db_user,
	password=settings.db_password,
	host=settings.db_host,
	port=settings.db_port,
)

# connection with base
engine = create_engine(DB_URL,  pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
	"""Base class for all database models."""
	pass


def get_db():
	"""
	gives each web request its own session and closes it when the request
	ends.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


