from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...db.models import Badge, UserBadge, User
from ...utils.auth import get_current_user
from ..schemas import (
    Badge as BadgeSchema,
    BadgeCreate,
    BadgeUpdate,
    UserBadge as UserBadgeSchema,
    UserBadgeCreate,
    UserBadgeUpdate,
    UserBadgeWithDetails,
)

router = APIRouter(
    prefix="/badges",
    tags=["badges"],
)

@router.post("/", response_model=BadgeSchema, status_code=status.HTTP_201_CREATED)
def create_badge(
    badge_data: BadgeCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new badge.
    
    Args:
        badge_data: Badge data
        current_user: Current user from token
        db: Database session
        
    Returns:
        Badge: Created badge
    """
    badge = Badge(**badge_data.dict())
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge

@router.get("/", response_model=List[BadgeSchema])
def get_badges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get list of badges.
    
    Args:
        skip: Number of badges to skip
        limit: Maximum number of badges to return
        db: Database session
        
    Returns:
        List[Badge]: List of badges
    """
    badges = db.query(Badge).offset(skip).limit(limit).all()
    return badges

@router.get("/{badge_id}", response_model=BadgeSchema)
def get_badge(
    badge_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get badge by ID.
    
    Args:
        badge_id: Badge ID
        db: Database session
        
    Returns:
        Badge: Badge information
        
    Raises:
        HTTPException: If badge not found
    """
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )
    return badge

@router.put("/{badge_id}", response_model=BadgeSchema)
def update_badge(
    badge_id: int,
    badge_data: BadgeUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update badge.
    
    Args:
        badge_id: Badge ID
        badge_data: Badge data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        Badge: Updated badge
        
    Raises:
        HTTPException: If badge not found
    """
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )
    
    # Update badge data
    update_data = badge_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(badge, field, value)
    
    db.commit()
    db.refresh(badge)
    
    return badge

@router.post("/user-badges", response_model=UserBadgeSchema, status_code=status.HTTP_201_CREATED)
def award_badge_to_user(
    user_badge_data: UserBadgeCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Award a badge to a user.
    
    Args:
        user_badge_data: User badge data
        current_user: Current user from token
        db: Database session
        
    Returns:
        UserBadge: Created user badge
        
    Raises:
        HTTPException: If user or badge not found, or if user already has the badge
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_badge_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if badge exists
    badge = db.query(Badge).filter(Badge.id == user_badge_data.badge_id).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found",
        )
    
    # Check if user already has the badge
    existing_user_badge = (
        db.query(UserBadge)
        .filter(
            UserBadge.user_id == user_badge_data.user_id,
            UserBadge.badge_id == user_badge_data.badge_id,
        )
        .first()
    )
    if existing_user_badge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this badge",
        )
    
    # Create user badge
    user_badge = UserBadge(**user_badge_data.dict())
    
    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)
    
    return user_badge

@router.get("/user-badges/user/{user_id}", response_model=List[UserBadgeWithDetails])
def get_user_badges(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get badges for a user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        List[UserBadgeWithDetails]: List of user badges with badge details
        
    Raises:
        HTTPException: If user not found
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get user badges with badge details
    user_badges = (
        db.query(UserBadge)
        .filter(UserBadge.user_id == user_id)
        .all()
    )
    
    result = []
    for user_badge in user_badges:
        badge = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
        if badge:
            result.append(
                UserBadgeWithDetails(
                    **user_badge.__dict__,
                    badge=badge,
                )
            )
    
    return result

@router.put("/user-badges/{user_badge_id}", response_model=UserBadgeSchema)
def update_user_badge(
    user_badge_id: int,
    user_badge_data: UserBadgeUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update user badge.
    
    Args:
        user_badge_id: User badge ID
        user_badge_data: User badge data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        UserBadge: Updated user badge
        
    Raises:
        HTTPException: If user badge not found
    """
    user_badge = db.query(UserBadge).filter(UserBadge.id == user_badge_id).first()
    if not user_badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User badge not found",
        )
    
    # Update user badge data
    update_data = user_badge_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_badge, field, value)
    
    db.commit()
    db.refresh(user_badge)
    
    return user_badge