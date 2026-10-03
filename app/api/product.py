from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils.auth import verify_password, create_access_token
from app.config.database import get_db
import app.models.models as models
import user

router = APIRouter()

class ProductApi(BaseModel):
    access_token: str
    token_type: str

# 1. GET Endpoint (React will fetch this to show the list)
@router.get("/api/products")
def get_todos(db: Session = Depends(get_db)):
    # Fetch all todos from the database
    todos = db.query(models.Product).all()
    return todos

# 2. POST Endpoint (React will call this to add a new item)
@router.post("/api/products")
def create_todo(item: TodoItem, db: Session = Depends(get_db)):
     
    new_todo = models.Product(product_name=item.product_name, price=item.price)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# 3. DELETE Endpoint (React will call this to delete an item)
@router.delete("/api/products/{product_id}")
def delete_todo(product_id: int, db: Session = Depends(get_db)):
    todo_to_delete = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if todo_to_delete is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(todo_to_delete)
    db.commit()
    return {"message": "Product deleted successfully"}

