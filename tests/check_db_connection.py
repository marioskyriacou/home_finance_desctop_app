from sqlalchemy import text
from backend.database import engine

conn = engine.connect()
print(conn.execute(text('SELECT version()')).scalar())
conn.close()