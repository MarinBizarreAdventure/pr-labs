from sqlalchemy import Column, Integer, String
from app.infrastructure.database.db import DB

db = DB()

class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128))
