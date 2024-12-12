from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr  
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[^\s]+$')  
    password: str = Field(..., min_length=6)  

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char in '@$!%*?&' for char in value):
            raise ValueError('Password must contain at least one special character: @$!%*?&')
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = Field(None, min_length=3, max_length=50)  
    password: str = Field(None, min_length=6)  

class UserResponse(BaseModel):
    id: int
    username: str  
    email: str
    
    class Config:
        orm_mode = True