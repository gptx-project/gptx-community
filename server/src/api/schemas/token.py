from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Token Type Enum
class TokenTypeEnum(str, Enum):
    """Enum for token types."""
    
    CONTRIBUTION = "contribution"
    ACHIEVEMENT = "achievement"
    REWARD = "reward"
    INVESTMENT = "investment"
    OTHER = "other"

# Token Status Enum
class TokenStatusEnum(str, Enum):
    """Enum for token transaction status."""
    
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

# Base Token Schema
class TokenBase(BaseModel):
    """Base schema for token data."""
    
    amount: float = Field(..., gt=0.0)
    type: TokenTypeEnum
    user_id: int
    contribution_id: Optional[int] = None

# Schema for creating a new token
class TokenCreate(TokenBase):
    """Schema for creating a new token."""
    
    pass

# Schema for updating a token
class TokenUpdate(BaseModel):
    """Schema for updating a token."""
    
    amount: Optional[float] = Field(None, gt=0.0)
    type: Optional[TokenTypeEnum] = None
    status: Optional[TokenStatusEnum] = None
    transaction_hash: Optional[str] = None
    contract_address: Optional[str] = None
    token_id: Optional[int] = None
    user_id: Optional[int] = None
    contribution_id: Optional[int] = None

# Schema for token response
class BlockchainToken(TokenBase):
    """Schema for token response."""
    
    id: int
    status: TokenStatusEnum
    transaction_hash: Optional[str] = None
    contract_address: Optional[str] = None
    token_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Schema for token with user and contribution details
class TokenWithDetails(BlockchainToken):
    """Schema for token with user and contribution details."""
    
    user_name: str
    contribution_title: Optional[str] = None