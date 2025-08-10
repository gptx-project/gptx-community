from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...db.models import Contribution, User, Project, Task
from ...utils.auth import get_current_user
from ..schemas import (
    Contribution as ContributionSchema,
    ContributionCreate,
    ContributionUpdate,
    ContributionWithDetails,
)

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"],
)

@router.post("/", response_model=ContributionSchema, status_code=status.HTTP_201_CREATED)
def create_contribution(
    contribution_data: ContributionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new contribution.
    
    Args:
        contribution_data: Contribution data
        current_user: Current user from token
        db: Database session
        
    Returns:
        Contribution: Created contribution
        
    Raises:
        HTTPException: If user, project, or task not found
    """
    # Check if user exists
    user = db.query(User).filter(User.id == contribution_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if project exists
    project = db.query(Project).filter(Project.id == contribution_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if task exists if task_id is provided
    if contribution_data.task_id:
        task = db.query(Task).filter(Task.id == contribution_data.task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
    
    # Create contribution
    contribution = Contribution(**contribution_data.dict())
    
    db.add(contribution)
    db.commit()
    db.refresh(contribution)
    
    return contribution

@router.get("/", response_model=List[ContributionSchema])
def get_contributions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get list of contributions.
    
    Args:
        skip: Number of contributions to skip
        limit: Maximum number of contributions to return
        db: Database session
        
    Returns:
        List[Contribution]: List of contributions
    """
    contributions = db.query(Contribution).offset(skip).limit(limit).all()
    return contributions

@router.get("/user/{user_id}", response_model=List[ContributionSchema])
def get_user_contributions(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get contributions for a user.
    
    Args:
        user_id: User ID
        skip: Number of contributions to skip
        limit: Maximum number of contributions to return
        db: Database session
        
    Returns:
        List[Contribution]: List of contributions
        
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
    
    contributions = (
        db.query(Contribution)
        .filter(Contribution.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contributions

@router.get("/project/{project_id}", response_model=List[ContributionSchema])
def get_project_contributions(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get contributions for a project.
    
    Args:
        project_id: Project ID
        skip: Number of contributions to skip
        limit: Maximum number of contributions to return
        db: Database session
        
    Returns:
        List[Contribution]: List of contributions
        
    Raises:
        HTTPException: If project not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    contributions = (
        db.query(Contribution)
        .filter(Contribution.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contributions

@router.get("/{contribution_id}", response_model=ContributionWithDetails)
def get_contribution(
    contribution_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get contribution by ID.
    
    Args:
        contribution_id: Contribution ID
        db: Database session
        
    Returns:
        Contribution: Contribution information
        
    Raises:
        HTTPException: If contribution not found
    """
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found",
        )
    
    # Get user and project names
    user = db.query(User).filter(User.id == contribution.user_id).first()
    project = db.query(Project).filter(Project.id == contribution.project_id).first()
    
    # Create response with details
    result = ContributionWithDetails(
        **contribution.__dict__,
        user_name=user.username if user else "",
        project_name=project.name if project else "",
    )
    
    # Add task title if task_id is provided
    if contribution.task_id:
        task = db.query(Task).filter(Task.id == contribution.task_id).first()
        if task:
            result.task_title = task.title
    
    return result

@router.put("/{contribution_id}", response_model=ContributionSchema)
def update_contribution(
    contribution_id: int,
    contribution_data: ContributionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update contribution.
    
    Args:
        contribution_id: Contribution ID
        contribution_data: Contribution data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        Contribution: Updated contribution
        
    Raises:
        HTTPException: If contribution not found
    """
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found",
        )
    
    # Update contribution data
    update_data = contribution_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contribution, field, value)
    
    db.commit()
    db.refresh(contribution)
    
    return contribution