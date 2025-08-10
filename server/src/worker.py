"""Celery worker for background tasks."""

from celery import Celery

from .config.settings import settings

# Create Celery app
celery = Celery(
    "bettercorp",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Configure Celery
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Import tasks
# celery.autodiscover_tasks(["src.tasks"])

@celery.task
def example_task(name: str) -> str:
    """
    Example task.
    
    Args:
        name: Name to greet
        
    Returns:
        str: Greeting message
    """
    return f"Hello, {name}!"