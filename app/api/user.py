from pydantic import BaseModel
from app.config.database import get_db
from fastapi import Depends,APIRouter,requests
from sqlalchemy.orm import Session
import app.models.user as user

router = APIRouter()

class UserRequest(BaseModel):
    username:str
    password:str

@router.get('/api/users')
def get_user(db:Session =Depends(get_db)):
    #user_record = db.query(user.UserModel).filter(user.UserModel.user_name == request.username).first();
    # Fetch all todos from the database
    todos = db.query(user.UserModel).all()
    return todos

@router.post('/api/user')
def create_user(request:UserRequest, db:Session =Depends(get_db)):
    user_record = db.query(user.UserModel).filter(user.UserModel.user_name == request.username).first();
    # Fetch all todos from the database
    
    if user_record is not  None:
        return user_record