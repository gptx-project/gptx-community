from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...db.models import User
from ...utils.auth import create_access_token
from ..schemas import UserCreate, User as UserSchema, Token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Register a new user.
    
    Args:
        user_data: User data
        db: Database session
        
    Returns:
        User: Created user
        
    Raises:
        HTTPException: If user with email or username already exists
    """
    # Check if user with email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if user with username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url,
        wallet_address=user_data.wallet_address,
    )
    user.set_password(user_data.password)
    
    # Add user to database
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get access token for user.
    
    Args:
        form_data: Form data with username and password
        db: Database session
        
    Returns:
        Token: Access token
        
    Raises:
        HTTPException: If username or password is incorrect
    """
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # Check if user exists and password is correct
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
    )
    
    return {"access_token": access_token, "token_type": "bearer"}