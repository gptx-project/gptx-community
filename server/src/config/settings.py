import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """Application settings."""
    
    # Project information
    PROJECT_NAME: str = "Bettercorp Contributor Portal"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "Central hub for project collaborators"
    
    # API settings
    API_PREFIX: str = "/api"
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/bettercorp"
    )
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Taiga API settings
    TAIGA_API_URL: str = os.getenv("TAIGA_API_URL", "https://api.taiga.io/api/v1/")
    TAIGA_USERNAME: str = os.getenv("TAIGA_USERNAME", "")
    TAIGA_PASSWORD: str = os.getenv("TAIGA_PASSWORD", "")
    
    # Blockchain settings
    BLOCKCHAIN_PROVIDER_URL: str = os.getenv(
        "BLOCKCHAIN_PROVIDER_URL", 
        "http://localhost:8545"
    )
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create settings instance
settings = Settings()