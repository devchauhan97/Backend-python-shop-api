from sqlalchemy import Boolean, Column, Integer, String
from app.config.database import Base

class Product(Base):
    __tablename__ = "products"  # This will be the actual table name in MySQL

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    price = Column(String(255), nullable=False)
