from sqlalchemy import Boolean, Column, Integer, String
from app.config.database import Base

class UserModel(Base):
    __tablename__ = "users"  # This will be the actual table name in MySQL

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
