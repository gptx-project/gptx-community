from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel

class TokenType(str, enum.Enum):
    """Enum for token types."""
    
    CONTRIBUTION = "contribution"
    ACHIEVEMENT = "achievement"
    REWARD = "reward"
    INVESTMENT = "investment"
    OTHER = "other"

class TokenStatus(str, enum.Enum):
    """Enum for token transaction status."""
    
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

class Token(BaseModel):
    """Token model for blockchain token transactions and balances."""
    
    # Token information
    amount = Column(Float, nullable=False)
    type = Column(Enum(TokenType), nullable=False)
    
    # Transaction information
    transaction_hash = Column(String, nullable=True, index=True)
    status = Column(Enum(TokenStatus), nullable=False, default=TokenStatus.PENDING)
    
    # Blockchain information
    contract_address = Column(String, nullable=True)
    token_id = Column(Integer, nullable=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    contribution_id = Column(Integer, ForeignKey("contribution.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="tokens")
    contribution = relationship("Contribution")
    
    def __repr__(self):
        """String representation of the token."""
        return f"<Token(id={self.id}, amount={self.amount}, type={self.type})>"