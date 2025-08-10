from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from passlib.context import CryptContext

from .base import BaseModel

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    """User model for authentication and profile data."""
    
    # Authentication fields
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    
    # Profile fields
    full_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Blockchain fields
    wallet_address = Column(String, nullable=True, index=True)
    
    # Relationships
    contributions = relationship("Contribution", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    tokens = relationship("Token", back_populates="user")
    
    def set_password(self, password: str) -> None:
        """
        Hash and set the user password.
        
        Args:
            password: Plain text password
        """
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """
        Verify the user password.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        return pwd_context.verify(password, self.hashed_password)
    
    def generate_verification_token(self) -> str:
        """
        Generate a verification token for email verification.
        
        Returns:
            str: Verification token
        """
        import secrets
        self.verification_token = secrets.token_urlsafe(32)
        self.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
        return self.verification_token