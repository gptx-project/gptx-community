"""Database initialization script."""

from sqlalchemy.exc import IntegrityError

from .database import Base, engine, SessionLocal
from .models import User, Project, Task, Badge, ContributionType, TokenType

def init_db():
    """Initialize the database with tables and initial data."""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if we already have users
        user_count = db.query(User).count()
        if user_count == 0:
            print("Creating initial admin user...")
            admin_user = User(
                email="admin@example.com",
                username="admin",
                full_name="Admin User",
                is_active=True,
                is_verified=True,
            )
            admin_user.set_password("admin")
            db.add(admin_user)
            db.commit()
            print("Admin user created.")
        
        # Check if we already have badges
        badge_count = db.query(Badge).count()
        if badge_count == 0:
            print("Creating initial badges...")
            badges = [
                Badge(
                    name="First Contribution",
                    description="Awarded for making your first contribution",
                    is_achievement=True,
                    is_soul_bound=True,
                ),
                Badge(
                    name="Code Master",
                    description="Awarded for exceptional code contributions",
                    is_skill=True,
                    is_soul_bound=True,
                ),
                Badge(
                    name="Documentation Hero",
                    description="Awarded for excellent documentation contributions",
                    is_skill=True,
                    is_soul_bound=True,
                ),
            ]
            db.add_all(badges)
            db.commit()
            print("Initial badges created.")
        
        # Check if we already have projects
        project_count = db.query(Project).count()
        if project_count == 0:
            print("Creating initial project...")
            project = Project(
                name="Bettercorp Contributor Portal",
                description="Central hub for project collaborators",
                is_active=True,
            )
            db.add(project)
            db.commit()
            print("Initial project created.")
        
        print("Database initialization completed.")
        
    except IntegrityError as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()