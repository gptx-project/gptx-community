"""
Run the FastAPI application.

This script is used to run the FastAPI application in development mode.
For production, use a proper ASGI server like Uvicorn or Hypercorn.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )