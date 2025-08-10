from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel

class ContributionType(str, enum.Enum):
    """Enum for contribution types."""
    
    CODE = "code"
    DESIGN = "design"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    REVIEW = "review"
    FINANCIAL = "financial"
    OTHER = "other"

class ContributionStatus(str, enum.Enum):
    """Enum for contribution status."""
    
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class Contribution(BaseModel):
    """Contribution model for tracking user contributions."""
    
    # Contribution information
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Contribution type and status
    type = Column(Enum(ContributionType), nullable=False)
    status = Column(Enum(ContributionStatus), nullable=False, default=ContributionStatus.PENDING)
    
    # Contribution value
    value = Column(Float, nullable=False, default=0.0)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=True)
    
    # Blockchain tracking
    transaction_hash = Column(String, nullable=True)
    token_amount = Column(Float, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
    task = relationship("Task", back_populates="contributions")
    
    def __repr__(self):
        """String representation of the contribution."""
        return f"<Contribution(id={self.id}, type={self.type}, user_id={self.user_id})>"