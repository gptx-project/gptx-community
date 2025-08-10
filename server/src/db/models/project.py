from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel

class Project(BaseModel):
    """Project model for storing project information."""
    
    # Project information
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    taiga_project_id = Column(Integer, nullable=True, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    # Project metadata
    repository_url = Column(String, nullable=True)
    documentation_url = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    
    # Relationships
    tasks = relationship("Task", back_populates="project")
    contributions = relationship("Contribution", back_populates="project")
    
    def __repr__(self):
        """String representation of the project."""
        return f"<Project(id={self.id}, name={self.name})>"


class Task(BaseModel):
    """Task model for storing task information synchronized with Taiga."""
    
    # Task information
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    taiga_task_id = Column(Integer, nullable=True, unique=True, index=True)
    
    # Task status
    status = Column(String, nullable=False, default="pending")
    priority = Column(String, nullable=True)
    
    # Task assignment
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")
    contributions = relationship("Contribution", back_populates="task")
    
    def __repr__(self):
        """String representation of the task."""
        return f"<Task(id={self.id}, title={self.title})>"