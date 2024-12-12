from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.schemas.user_schemas import UserCreate, UserUpdate,UserResponse
from app.domain.security.jwt_utils import create_access_token
from app.domain.security.hashing import hash_password, verify_password
from app.domain.models.user import User
from typing import List, Optional
from fastapi import HTTPException
from typing import Tuple


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: UserCreate) -> UserResponse:
        password_hash = hash_password(user_data.password)
        user = self.user_repository.create_user(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash 
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email
        )
    

    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        access_token = create_access_token(data={"sub": user.email})
        return access_token


    def find_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.user_repository.get_user_by_email(email)
        if user:
            user_response = UserResponse(
                id=str(user.id),
                username=user.username,
                email=user.email
            )
            return user_response
        return None

    def modify_user(self, user_id: int, user_data: dict) -> Optional[User]:
        return self.user_repository.update_user(user_id, user_data)

    def remove_user(self, user_id: int) -> bool:
        return self.user_repository.delete_user(user_id)
    

    def find_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            return user
        return None
    

    def delete_user(self, user_id: int, current_user: str) -> None:
        user_to_delete = self.find_user_by_id(user_id)
        if not user_to_delete or user_to_delete.email != current_user:
            raise ValueError("Access forbidden: You can only delete your own account")
        
        success = self.remove_user(user_id)
        if not success:
            raise LookupError("User not found")

    def list_all_users(self) -> List[User]:
        return self.user_repository.get_all_users()
    

    def modify_user_by_email(self, email: str, user_data: dict) -> Optional[UserResponse]:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None

        try:
            updated_user = self.user_repository.update_user(user.id, user_data)
            if updated_user:
                return UserResponse(
                    id=str(updated_user.id),
                    username=updated_user.username,
                    email=updated_user.email
                )
        except ValueError as e:
            if "unique constraints" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Update would violate unique constraints. Please use unique values."
                )
            else:
                raise HTTPException(status_code=500, detail="An error occurred while updating the user.")

        return None
    

    def list_users_with_pagination(self, offset: int, limit: int) -> List[UserResponse]:
        users = self.user_repository.get_users_with_pagination(offset, limit)
        user_responses = [UserResponse(id=user.id, username=user.username, email=user.email) for user in users]
        return user_responses