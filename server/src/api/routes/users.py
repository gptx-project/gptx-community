from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...db.models import User
from ...utils.auth import get_current_user
from ..schemas import User as UserSchema, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get current user information.
    
    Args:
        current_user: Current user from token
        db: Database session
        
    Returns:
        User: Current user information
    """
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update current user information.
    
    Args:
        user_data: User data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        User: Updated user information
    """
    user = db.query(User).filter(User.id == current_user.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update user data
    update_data = user_data.dict(exclude_unset=True)
    
    # Handle password update separately
    if "password" in update_data:
        user.set_password(update_data.pop("password"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        User: User information
        
    Raises:
        HTTPException: If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.get("/", response_model=List[UserSchema])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get list of users.
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        db: Database session
        
    Returns:
        List[User]: List of users
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users