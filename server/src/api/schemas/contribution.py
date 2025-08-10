from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Contribution Type Enum
class ContributionTypeEnum(str, Enum):
    """Enum for contribution types."""
    
    CODE = "code"
    DESIGN = "design"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REVIEW = "review"
    FINANCIAL = "financial"
    OTHER = "other"

# Contribution Status Enum
class ContributionStatusEnum(str, Enum):
    """Enum for contribution status."""
    
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

# Base Contribution Schema
class ContributionBase(BaseModel):
    """Base schema for contribution data."""
    
    title: str
    description: Optional[str] = None
    type: ContributionTypeEnum
    value: float = Field(0.0, ge=0.0)
    user_id: int
    project_id: int
    task_id: Optional[int] = None

# Schema for creating a new contribution
class ContributionCreate(ContributionBase):
    """Schema for creating a new contribution."""
    
    pass

# Schema for updating a contribution
class ContributionUpdate(BaseModel):
    """Schema for updating a contribution."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ContributionTypeEnum] = None
    status: Optional[ContributionStatusEnum] = None
    value: Optional[float] = Field(None, ge=0.0)
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    transaction_hash: Optional[str] = None
    token_amount: Optional[float] = Field(None, ge=0.0)

# Schema for contribution response
class Contribution(ContributionBase):
    """Schema for contribution response."""
    
    id: int
    status: ContributionStatusEnum
    transaction_hash: Optional[str] = None
    token_amount: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Schema for contribution with user and project
class ContributionWithDetails(Contribution):
    """Schema for contribution with user and project details."""
    
    user_name: str
    project_name: str
    task_title: Optional[str] = None