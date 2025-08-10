from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import BaseModel

class Badge(BaseModel):
    """Badge model for gamification badges and achievements."""
    
    # Badge information
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    
    # Badge criteria
    criteria = Column(Text, nullable=True)
    
    # Badge type
    is_achievement = Column(Boolean, default=False)
    is_skill = Column(Boolean, default=False)
    is_contribution = Column(Boolean, default=False)
    
    # Blockchain tracking
    is_soul_bound = Column(Boolean, default=True)
    contract_address = Column(String, nullable=True)
    
    # Relationships
    users = relationship("UserBadge", back_populates="badge")
    
    def __repr__(self):
        """String representation of the badge."""
        return f"<Badge(id={self.id}, name={self.name})>"


class UserBadge(BaseModel):
    """Association model between users and badges."""
    
    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badge.id"), nullable=False)
    
    # Badge issuance information
    is_visible = Column(Boolean, default=True)
    
    # Blockchain tracking
    transaction_hash = Column(String, nullable=True)
    token_id = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="users")
    
    def __repr__(self):
        """String representation of the user badge."""
        return f"<UserBadge(user_id={self.user_id}, badge_id={self.badge_id})>"