from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Base Badge Schema
class BadgeBase(BaseModel):
    """Base schema for badge data."""
    
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    criteria: Optional[str] = None
    is_achievement: bool = False
    is_skill: bool = False
    is_contribution: bool = False
    is_soul_bound: bool = True

# Schema for creating a new badge
class BadgeCreate(BadgeBase):
    """Schema for creating a new badge."""
    
    pass

# Schema for updating a badge
class BadgeUpdate(BaseModel):
    """Schema for updating a badge."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    criteria: Optional[str] = None
    is_achievement: Optional[bool] = None
    is_skill: Optional[bool] = None
    is_contribution: Optional[bool] = None
    is_soul_bound: Optional[bool] = None
    contract_address: Optional[str] = None

# Schema for badge response
class Badge(BadgeBase):
    """Schema for badge response."""
    
    id: int
    contract_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Base UserBadge Schema
class UserBadgeBase(BaseModel):
    """Base schema for user badge data."""
    
    user_id: int
    badge_id: int
    is_visible: bool = True

# Schema for creating a new user badge
class UserBadgeCreate(UserBadgeBase):
    """Schema for creating a new user badge."""
    
    pass

# Schema for updating a user badge
class UserBadgeUpdate(BaseModel):
    """Schema for updating a user badge."""
    
    is_visible: Optional[bool] = None
    transaction_hash: Optional[str] = None
    token_id: Optional[int] = None

# Schema for user badge response
class UserBadge(UserBadgeBase):
    """Schema for user badge response."""
    
    id: int
    transaction_hash: Optional[str] = None
    token_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Schema for user badge with badge details
class UserBadgeWithDetails(UserBadge):
    """Schema for user badge with badge details."""
    
    badge: Badge