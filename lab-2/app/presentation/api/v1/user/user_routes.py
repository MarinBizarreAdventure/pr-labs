from fastapi import APIRouter, Depends, HTTPException
from app.application.services.user_service import UserService
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.schemas.user_schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from app.domain.security.jwt_utils import get_current_user
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from app.infrastructure.database.db import DB
from typing import List
from typing import Optional
from fastapi import Query
from fastapi import FastAPI, UploadFile, File
import json
import logging


class UserRouter:
    def __init__(self, user_service: UserService):
        self.router = APIRouter()
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/users", response_model=UserResponse)
        async def register(user: UserCreate):
            try:
                return self.user_service.register_user(user)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.post("/login")
        async def login(user: UserLogin):
            access_token = self.user_service.authenticate_user(email=user.email, password=user.password)
            if access_token is None:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            return {"access_token": access_token, "token_type": "bearer"}

        @self.router.get("/secure-data")
        async def secure_data(current_user: str = Depends(get_current_user)):
            return {"message": f"Hello {current_user}, this is secured data!"}

        @self.router.get("/users/{email}", response_model=Optional[UserResponse])
        async def get_user(
            email: str,
            current_user: str = Depends(get_current_user),
        ):
            if current_user != email:
                raise HTTPException(
                    status_code=403,
                    detail="Access forbidden: You can only access your own information"
                )
    
            user = self.user_service.find_user_by_email(email)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
    
            return user

        
        @self.router.put("/users/me", response_model=UserResponse)
        async def update_user(
            user_data: UserUpdate,
            current_user: str = Depends(get_current_user)
        ):
            updated_user = self.user_service.modify_user_by_email(current_user, user_data.dict(exclude_unset=True))
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found")
            return updated_user
        

        @self.router.delete("/users/{user_id}")
        async def delete_user(
           user_id: int,
          current_user: str = Depends(get_current_user),
        ):
            try:
                self.user_service.delete_user(user_id, current_user)
            except ValueError as e:
                raise HTTPException(status_code=403, detail=str(e))
            except LookupError:
                raise HTTPException(status_code=404, detail="User not found")

            return {"detail": "User deleted successfully"}

        
        # @self.router.get("/users", response_model=List[UserResponse])
        # async def list_users(current_user: str = Depends(get_current_user)):
        #     return self.user_service.list_all_users()  
        

        @self.router.get("/users", response_model=List[UserResponse])
        async def list_users(
            offset: int = Query(0, ge=0),
            limit: int = Query(10, ge=1),
            # current_user: str = Depends(get_current_user)
        ):
            user_responses = self.user_service.list_users_with_pagination(offset, limit)
            return user_responses
        

        @self.router.post("/upload-json/")
        async def upload_json(file: UploadFile = File(...)):
            try:
                content = await file.read()

                json_data = json.loads(content)

                logging.info(f"Uploaded JSON: {json_data}")

                return {"message": "File uploaded and logged successfully."}

            except json.JSONDecodeError:
                return {"error": "Invalid JSON file."}