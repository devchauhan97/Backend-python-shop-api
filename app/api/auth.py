from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils.auth import verify_password, create_access_token
from app.config.database import get_db
import app.models.models as models
import user

router = APIRouter()
 

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/auth/login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user_record = db.query(user.UserModel).filter(user.UserModel.user_name == request.username).first()

    if not user_record:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(request.password, user_record.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user_record.user_name})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,  # set to True in HTTPS production
        max_age=60 * 60 * 24,
        path="/",
    )

    return {"access_token": access_token, "token_type": "bearer"}

