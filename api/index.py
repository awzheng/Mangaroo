"""
Vercel Serverless Entry Point
This file is the entry point for Vercel's serverless functions.
It imports the FastAPI app from the main module.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Vercel looks for 'app' or 'handler' in this file
# FastAPI apps work directly with Vercel's Python runtime

