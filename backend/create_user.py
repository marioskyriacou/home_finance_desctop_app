"""
Create user form terminal. Ask username and password twice.
Creates the user or if the user exists, reset the password.
"""
import getpass
from sqlalchemy import select
from .database import Base, SessionLocal, engine
from .models import User
from .security import hash_password

def main()-> None:
	Base.metadata.create_all(bind=engine)

	user_name = input("Username: ").strip()
	password = getpass.getpass(prompt="Password: ")

	if not user_name or not password:
		print("Username and password are required.")
		return

	if password != getpass.getpass(prompt="Re-enter password: "):
		print("Passwords do not match.")
		return

	with SessionLocal() as db:
		user = db.scalar(select(User).where(User.username == user_name) )

		if user is None:
			db.add(User(username=user_name, hashed_password=hash_password(password)))
			print("User created.")
		else:
			user.hashed_password = hash_password(password)
			print(f"Password for '{user_name}' updated.")

		db.commit()

if __name__ == "__main__":
	main()

