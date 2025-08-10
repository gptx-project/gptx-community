from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Base User Schema
class UserBase(BaseModel):
    """Base schema for user data."""
    
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    wallet_address: Optional[str] = None

# Schema for creating a new user
class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8)

# Schema for updating a user
class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    wallet_address: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

# Schema for user authentication
class UserLogin(BaseModel):
    """Schema for user login."""
    
    username: str
    password: str

# Schema for token response
class Token(BaseModel):
    """Schema for authentication token."""
    
    access_token: str
    token_type: str = "bearer"

# Schema for token data
class TokenData(BaseModel):
    """Schema for token data."""
    
    user_id: Optional[int] = None

# Schema for user response
class User(UserBase):
    """Schema for user response."""
    
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True