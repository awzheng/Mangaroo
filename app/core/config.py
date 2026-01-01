"""
========================================
Configuration Module for Mangaroo
========================================

This file handles loading settings from environment variables.
Think of it as the "settings panel" for the entire app.

KEY CONCEPT: Environment Variables
- Instead of hardcoding sensitive data (like API keys) in code,
  we store them in a .env file that stays on your computer
- This keeps secrets safe when sharing code on GitHub

WHAT THIS FILE DOES:
1. Reads the .env file to get your API key
2. Provides default settings for the app
3. Makes these settings available to other parts of the app
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# pydantic_settings: A library that makes it easy to load
# and validate settings from environment variables
from pydantic_settings import BaseSettings

# lru_cache: A decorator that "remembers" results so we don't
# reload the settings file every time we need them
from functools import lru_cache

# os: Python's built-in module for interacting with the
# operating system (creating folders, etc.)
import os


# ----------------------------------------
# SETTINGS CLASS
# ----------------------------------------
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    HOW IT WORKS:
    - Each variable below corresponds to a value in your .env file
    - Variable names are case-insensitive (gemini_api_key = GEMINI_API_KEY)
    - If a value isn't in .env, the default value here is used
    
    EXAMPLE:
    If your .env has: GEMINI_API_KEY=abc123
    Then: settings.gemini_api_key will equal "abc123"
    """
    
    # ---- API Keys ----
    # Your Google Gemini API key for AI features
    # This is read from GEMINI_API_KEY in .env
    gemini_api_key: str = ""
    
    # ---- App Configuration ----
    # The name of our application
    app_name: str = "Mangaroo"
    
    # Debug mode: when True, shows more detailed error messages
    # Set to False in production for security
    debug: bool = False
    
    # ---- File Storage Settings ----
    # Where uploaded PDF files are saved
    upload_dir: str = "uploads"
    
    # Maximum file size allowed (in megabytes)
    # Prevents users from uploading huge files that slow down the server
    max_file_size_mb: int = 50
    
    # ---- AI Generation Settings ----
    # Maximum length of text to send to the AI at once
    # Longer text = more context but slower/more expensive
    max_context_length: int = 8000
    
    # Default art style for generated images
    image_style: str = "manga"
    
    class Config:
        """
        Pydantic configuration for how to load settings.
        """
        # Name of the environment file to read
        env_file = ".env"
        
        # File encoding (UTF-8 supports international characters)
        env_file_encoding = "utf-8"
        
        # "ignore" means extra variables in .env won't cause errors
        extra = "ignore"


# ----------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------
@lru_cache()  # This decorator caches the result
def get_settings() -> Settings:
    """
    Get the application settings.
    
    WHY USE THIS FUNCTION?
    - The @lru_cache decorator means we only read .env once
    - Every call after the first returns the cached settings
    - This makes the app faster and more efficient
    
    HOW TO USE:
        from app.core.config import get_settings
        settings = get_settings()
        api_key = settings.gemini_api_key
    
    Returns:
        Settings: The application settings object
    """
    return Settings()


def ensure_upload_dir():
    """
    Create the upload directory if it doesn't exist.
    
    WHY IS THIS NEEDED?
    - When users upload PDFs, we need somewhere to save them
    - This function checks if the folder exists
    - If not, it creates the folder automatically
    
    EXAMPLE:
        If upload_dir = "uploads" and folder doesn't exist,
        this creates the "uploads" folder in your project
    """
    settings = get_settings()
    # os.makedirs creates the folder
    # exist_ok=True means don't error if it already exists
    os.makedirs(settings.upload_dir, exist_ok=True)
