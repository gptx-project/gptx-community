from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Base Project Schema
class ProjectBase(BaseModel):
    """Base schema for project data."""
    
    name: str
    description: Optional[str] = None
    taiga_project_id: Optional[int] = None
    repository_url: Optional[str] = None
    documentation_url: Optional[str] = None
    logo_url: Optional[str] = None

# Schema for creating a new project
class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    
    pass

# Schema for updating a project
class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    taiga_project_id: Optional[int] = None
    repository_url: Optional[str] = None
    documentation_url: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for project response
class Project(ProjectBase):
    """Schema for project response."""
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Base Task Schema
class TaskBase(BaseModel):
    """Base schema for task data."""
    
    title: str
    description: Optional[str] = None
    taiga_task_id: Optional[int] = None
    status: str = "pending"
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    project_id: int

# Schema for creating a new task
class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    
    pass

# Schema for updating a task
class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    taiga_task_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None

# Schema for task response
class Task(TaskBase):
    """Schema for task response."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True

# Schema for project with tasks
class ProjectWithTasks(Project):
    """Schema for project with tasks."""
    
    tasks: List[Task] = []