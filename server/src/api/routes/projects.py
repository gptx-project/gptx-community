from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...db.models import Project, Task
from ...utils.auth import get_current_user
from ..schemas import (
    Project as ProjectSchema,
    ProjectCreate,
    ProjectUpdate,
    Task as TaskSchema,
    TaskCreate,
    TaskUpdate,
    ProjectWithTasks,
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new project.
    
    Args:
        project_data: Project data
        current_user: Current user from token
        db: Database session
        
    Returns:
        Project: Created project
    """
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=List[ProjectSchema])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get list of projects.
    
    Args:
        skip: Number of projects to skip
        limit: Maximum number of projects to return
        db: Database session
        
    Returns:
        List[Project]: List of projects
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectWithTasks)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get project by ID.
    
    Args:
        project_id: Project ID
        db: Database session
        
    Returns:
        Project: Project information with tasks
        
    Raises:
        HTTPException: If project not found
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project

@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update project.
    
    Args:
        project_id: Project ID
        project_data: Project data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        Project: Updated project
        
    Raises:
        HTTPException: If project not found
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Update project data
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project

@router.post("/{project_id}/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create a new task for a project.
    
    Args:
        project_id: Project ID
        task_data: Task data
        current_user: Current user from token
        db: Database session
        
    Returns:
        Task: Created task
        
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
    
    # Create task
    task = Task(**task_data.dict())
    task.project_id = project_id
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

@router.get("/{project_id}/tasks", response_model=List[TaskSchema])
def get_project_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get tasks for a project.
    
    Args:
        project_id: Project ID
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        db: Database session
        
    Returns:
        List[Task]: List of tasks
        
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
    
    tasks = db.query(Task).filter(Task.project_id == project_id).offset(skip).limit(limit).all()
    return tasks

@router.get("/{project_id}/tasks/{task_id}", response_model=TaskSchema)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get task by ID.
    
    Args:
        project_id: Project ID
        task_id: Task ID
        db: Database session
        
    Returns:
        Task: Task information
        
    Raises:
        HTTPException: If project or task not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task

@router.put("/{project_id}/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update task.
    
    Args:
        project_id: Project ID
        task_id: Task ID
        task_data: Task data to update
        current_user: Current user from token
        db: Database session
        
    Returns:
        Task: Updated task
        
    Raises:
        HTTPException: If project or task not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Update task data
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    return task