
# app/api/v1/api.py
from fastapi import APIRouter, Response
from pydantic import BaseModel
 
# Import the individual routers
from app.api.auth import router as auth_router
from app.api.product import router as product_router 
from app.api.user import router as user_router
from app.utils.auth import  create_access_token

# Create the master v1 router
api_router = APIRouter()


class UserRequest(BaseModel):
    username:str
    password:str
    
@api_router.get("/api/health")
def health_check():
    return {"message": "API is running!"}


@api_router.post("/api/login")
def login(request:UserRequest, response:Response):
     
    access_token = create_access_token(data={"sub": request.username})

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


api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(user_router)