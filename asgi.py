"""
Deployment entry point for TrustGuard AI.
This module sets up the Python path dynamically so that both
the 'ml' package (in root) and the 'app' package (in backend/)
can be imported without manual PYTHONPATH manipulation.
"""
import sys
from pathlib import Path

# Add the backend directory to sys.path so 'app.x' imports work
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI application
from app.main import app
