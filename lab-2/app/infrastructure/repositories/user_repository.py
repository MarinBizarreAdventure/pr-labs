from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, DatabaseError
from app.domain.models.user import User
from app.domain.schemas.user_schemas import UserResponse
from app.infrastructure.database.db import DB
from typing import List, Optional, Tuple
from sqlalchemy import select, func



class UserRepository:
    def __init__(self, db: DB):
        self.db = db  

    def create_user(self, email: str, username: str, password_hash: str) -> Optional[User]:
        db: Session = next(self.db.get_db())
        try:
            user = User(
                email=email,
                username=username,
                password_hash=password_hash
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this email or username already exists")
        except DatabaseError as e:
            db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()

    def get_user_by_email(self, email: str) -> Optional[User]:
        db: Session = next(self.db.get_db())
        try:
            result = db.execute(
                select(User).filter(User.email == email)
            )
            return result.scalars().first()
        except DatabaseError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        db: Session = next(self.db.get_db())
        try:
        
           user = db.execute(
                select(User).filter(User.id == user_id)
           ).scalars().first()
           if user:
                return UserResponse(id=user.id,username=user.username,email=user.email)
           return None
        except DatabaseError as e:
            db.rollback() 
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()

    def update_user(self, user_id: int, update_data: dict) -> Optional[User]:
        db: Session = next(self.db.get_db())
        try:
            user = db.execute(select(User).filter(User.id == user_id)).scalars().first()        
            if user:
                for key, value in update_data.items():
                    setattr(user, key, value)
                db.commit()
                db.refresh(user) 
                return user
            return None
        except IntegrityError:
            db.rollback()
            raise ValueError("Update would violate unique constraints")
        except DatabaseError as e:
            db.rollback()
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()

    def delete_user(self, user_id: int) -> bool:
        db: Session = next(self.db.get_db())
        try:
            result = db.execute(
                select(User).filter(User.id == user_id)
            )
            user = result.scalars().first()            
            if user:
                db.delete(user)  
                db.commit()     
                return True      
            return False          
        except DatabaseError as e:
            db.rollback()          
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()

    def get_all_users(self) -> List[User]:
        db: Session = next(self.db.get_db())
        try:
            result = db.execute(select(User))
            return result.scalars().all()
        except DatabaseError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()


    def get_users_with_pagination(self, offset: int, limit: int) -> List[User]:
        db: Session = next(self.db.get_db())
        try:
            print("Wtf")
            users_query = db.execute(select(User).offset(offset).limit(limit))
            print("wtf2 ",  users_query)
            users = users_query.scalars().all()
            
            return users
        except DatabaseError as e:
            raise Exception(f"Database error occurred: {str(e)}")
        finally:
            db.close()