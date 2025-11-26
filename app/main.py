"""
========================================
MyMangaka - Main Application Entry Point
========================================

This is the MAIN file that runs the web application.
Think of it as the "front desk" that handles all requests.

KEY CONCEPT: FastAPI
- FastAPI is a web framework for building APIs in Python
- It handles HTTP requests (GET, POST, etc.)
- It serves web pages and processes data

WHAT THIS FILE DOES:
1. Creates the FastAPI application
2. Defines all the URL routes (pages you can visit)
3. Handles file uploads
4. Manages reading sessions
5. Coordinates between PDF processing, AI, and the frontend

ROUTE OVERVIEW:
- GET  /                    → Upload page (index.html)
- GET  /reader/{session_id} → Reader page (reader.html)
- POST /api/upload          → Upload a PDF file
- GET  /api/get_page_text   → Get text from a specific page
- POST /api/generate_panel  → Generate a manga panel
- GET  /api/story_state     → Get current story context
- DELETE /api/session/{id}  → Close a reading session

HOW TO RUN:
    uvicorn app.main:app --reload
    Then open http://localhost:8000 in your browser
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# Standard library imports
import os                    # Operating system operations (file paths, etc.)
import uuid                  # Generate unique IDs for sessions
from pathlib import Path     # Work with file paths easily
from typing import Optional  # Type hints for optional values

# FastAPI imports - the web framework
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
# FastAPI: The main application class
# File, UploadFile: Handle file uploads
# HTTPException: Return error responses
# Request: Access incoming request data
# Form: Handle form data submissions

# Response types
from fastapi.responses import HTMLResponse, JSONResponse
# HTMLResponse: Return HTML pages
# JSONResponse: Return JSON data for API endpoints

# Static files and templates
from fastapi.staticfiles import StaticFiles  # Serve CSS, JS, images
from fastapi.templating import Jinja2Templates  # Render HTML templates

# Our custom modules
from app.core.config import get_settings, ensure_upload_dir
from app.core.pdf_processor import PDFProcessor, get_pdf_info
from app.core.story_manager import StoryBible
from app.core.image_gen import get_image_generator


# ========================================
# APP INITIALIZATION
# ========================================

# Create the FastAPI application instance
# This is the central object that handles everything
app = FastAPI(
    title="MyMangaka",                                    # App name (shown in docs)
    description="AI-Powered Smart Reader - Transform novels into manga",
    version="1.0.0"
)

# ----------------------------------------
# STATIC FILES & TEMPLATES SETUP
# ----------------------------------------
# Get the directory where this file lives
BASE_DIR = Path(__file__).resolve().parent

# Mount static files (CSS, JavaScript, images)
# This makes files in /static accessible via /static URL
# Example: /static/css/styles.css serves app/static/css/styles.css
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Set up Jinja2 templates for rendering HTML
# Templates are HTML files with dynamic content
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Make sure the upload folder exists (use /tmp on Vercel)
# Vercel's serverless functions only allow writes to /tmp
import tempfile
UPLOAD_DIR = os.environ.get("VERCEL", None)
if UPLOAD_DIR:
    # Running on Vercel - use temp directory
    UPLOAD_DIR = tempfile.gettempdir()
else:
    # Running locally - use uploads folder
    UPLOAD_DIR = str(Path(get_settings().upload_dir).resolve())
    os.makedirs(UPLOAD_DIR, exist_ok=True)


# ========================================
# SESSION MANAGEMENT
# ========================================
# When someone uploads a PDF, we create a "session" to track their reading progress
# Sessions are stored in memory (for simplicity)
# In production, you'd use Redis or a database

# Dictionary to store active reading sessions
# Key: session_id (string), Value: ReadingSession object
reading_sessions: dict = {}


class ReadingSession:
    """
    Represents an active reading session.
    
    Each time someone uploads a PDF, we create a ReadingSession.
    It keeps track of:
    - The PDF file they're reading
    - Their Story Bible (character/scene context)
    - Which page they're on
    
    Think of it like a bookmark that also remembers
    what all the characters look like.
    """
    
    def __init__(self, pdf_path: str, filename: str):
        """
        Create a new reading session.
        
        Args:
            pdf_path: Where the uploaded PDF is saved
            filename: Original name of the file
        """
        self.pdf_path = pdf_path          # Path to the saved PDF
        self.filename = filename          # Original filename for display
        self.story_bible = StoryBible()   # AI context tracker
        self.current_page = 0             # Track which page user is on
        
        # Open the PDF and get basic info
        self.processor = PDFProcessor(pdf_path)
        self.processor.open()
        self.total_pages = self.processor.total_pages
        self.metadata = self.processor.get_metadata()
        
    def close(self):
        """
        Clean up when the session ends.
        
        IMPORTANT: Always clean up resources!
        - Close open files
        - Free up memory
        """
        self.processor.close()


# ========================================
# PAGE ROUTES (HTML Pages)
# ========================================
# These routes return full HTML pages that users see in their browser

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Home page - PDF upload interface.
    
    ROUTE: GET /
    
    This is what users see when they first visit the site.
    It shows a drag-and-drop upload area for PDF files.
    
    WHAT'S HAPPENING:
    1. User visits http://localhost:8000/
    2. This function runs
    3. It renders index.html template
    4. User sees the upload page
    
    Args:
        request: The incoming HTTP request (required by Jinja2)
        
    Returns:
        The rendered index.html page
    """
    # templates.TemplateResponse renders an HTML template
    # We pass variables that the template can use
    return templates.TemplateResponse(
        "index.html",                                    # Which template to render
        {"request": request, "title": "MyMangaka - Upload Your Novel"}  # Data for template
    )


@app.get("/reader/{session_id}", response_class=HTMLResponse)
async def reader(request: Request, session_id: str):
    """
    Reader page - Split-screen manga reader interface.
    
    ROUTE: GET /reader/{session_id}
    
    After uploading a PDF, users are redirected here.
    This is the main reading experience:
    - Left side: Novel text
    - Right side: Generated manga panels
    
    The {session_id} in the URL tells us WHICH PDF they're reading.
    Example: /reader/abc123 → read the PDF for session "abc123"
    
    Args:
        request: The incoming HTTP request
        session_id: Unique identifier for the reading session
        
    Returns:
        The rendered reader.html page
        
    Raises:
        HTTPException 404: If the session doesn't exist
    """
    # Check if this session exists
    if session_id not in reading_sessions:
        # 404 = "Not Found" error
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get the session data
    session = reading_sessions[session_id]
    
    # Render the reader template with session data
    return templates.TemplateResponse(
        "reader.html",
        {
            "request": request,
            "title": f"Reading: {session.filename}",
            "session_id": session_id,
            "filename": session.filename,
            "total_pages": session.total_pages,
            "metadata": session.metadata
        }
    )


# ========================================
# API ROUTES (Data Endpoints)
# ========================================
# These routes return JSON data, not HTML pages
# They're called by JavaScript in the frontend

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and create a reading session.
    
    ROUTE: POST /api/upload
    
    This is called when users drop a PDF on the upload area.
    
    FLOW:
    1. Receive the uploaded file
    2. Validate it (is it a PDF? is it too big?)
    3. Save it to the uploads folder
    4. Create a ReadingSession
    5. Return the session ID so frontend can redirect to reader
    
    Args:
        file: The uploaded file (FastAPI handles the upload)
              File(...) means this parameter is required
        
    Returns:
        JSON with session_id and redirect URL
        
    Raises:
        HTTPException 400: If file is invalid or too large
        HTTPException 500: If processing fails
    """
    # ---- Step 1: Validate file type ----
    # Check if it's actually a PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # ---- Step 2: Check file size ----
    settings = get_settings()
    contents = await file.read()  # Read the file contents into memory
    
    # Calculate size in bytes, compare to limit
    if len(contents) > settings.max_file_size_mb * 1024 * 1024:  # Convert MB to bytes
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB"
        )
    
    # ---- Step 3: Generate unique session ID ----
    # uuid4 generates a random unique ID
    # [:8] takes just the first 8 characters for a shorter ID
    session_id = str(uuid.uuid4())[:8]
    
    # ---- Step 4: Save the file ----
    # Add session_id to filename to make it unique
    safe_filename = f"{session_id}_{file.filename}"
    file_path = Path(UPLOAD_DIR) / safe_filename
    
    # Write the file to disk
    with open(file_path, "wb") as f:  # "wb" = write binary
        f.write(contents)
    
    # ---- Step 5: Create reading session ----
    try:
        session = ReadingSession(str(file_path), file.filename)
        reading_sessions[session_id] = session  # Store in our dictionary
        
        # Return success response
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "total_pages": session.total_pages,
            "metadata": session.metadata,
            "redirect_url": f"/reader/{session_id}"  # Where to go next
        })
    except Exception as e:
        # If something goes wrong, clean up the file we saved
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@app.get("/api/get_page_text")
async def get_page_text(session_id: str, page: int = 0):
    """
    Get the text content of a specific page.
    
    ROUTE: GET /api/get_page_text?session_id=xxx&page=0
    
    Called by the frontend when user navigates between pages.
    
    WHAT IT DOES:
    1. Find the reading session
    2. Extract text from the requested page
    3. Return text along with navigation info
    
    Args:
        session_id: Which session (from URL query parameter)
        page: Which page to get (0-indexed, default is 0)
        
    Returns:
        JSON with page text and navigation info
        
    Example Response:
        {
            "success": true,
            "page": 0,
            "total_pages": 100,
            "text": "Chapter 1...",
            "has_next": true,
            "has_prev": false
        }
    """
    # Find the session
    if session_id not in reading_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = reading_sessions[session_id]
    
    # Validate page number
    if page < 0 or page >= session.total_pages:
        raise HTTPException(
            status_code=400, 
            detail=f"Page {page} out of range (0-{session.total_pages - 1})"
        )
    
    try:
        # Get the page text
        text = session.processor.get_page_text(page)
        
        # Update current page tracking
        session.current_page = page
        
        # Return response with navigation helpers
        return JSONResponse({
            "success": True,
            "page": page,
            "total_pages": session.total_pages,
            "text": text,
            "has_next": page < session.total_pages - 1,  # Is there a next page?
            "has_prev": page > 0  # Is there a previous page?
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate_panel")
async def generate_panel(
    session_id: str = Form(...),
    page: int = Form(...)
):
    """
    Generate a manga panel for the specified page.
    
    ROUTE: POST /api/generate_panel
    
    This is the MAGIC endpoint - it creates the manga art!
    
    FLOW:
    1. Get the page text
    2. Update Story Bible (analyze characters, scene, etc.)
    3. Generate image using Imagen 3
    4. Return the image data
    
    Args:
        session_id: Which session (from form data)
        page: Which page to generate art for
        
    Returns:
        JSON with:
        - success: Did it work?
        - image_data: Base64 encoded image (can be displayed in HTML)
        - story_state: Updated story context
        - prompt_used: What we asked the AI to generate
    """
    # Find session
    if session_id not in reading_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = reading_sessions[session_id]
    
    # Validate page
    if page < 0 or page >= session.total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Page {page} out of range"
        )
    
    try:
        # ---- Step 1: Get page text ----
        page_text = session.processor.get_page_text(page)
        
        # ---- Step 2: Update Story Bible ----
        # This analyzes the text and extracts:
        # - Characters in the scene
        # - Their appearances
        # - The setting
        # - Mood and visual style
        story_state = await session.story_bible.update_state(page_text)
        
        # ---- Step 3: Generate the manga panel ----
        generator = get_image_generator()
        result = await generator.generate_from_story_bible(story_state)
        
        # ---- Step 4: Return results ----
        return JSONResponse({
            "success": result["success"],
            "page": page,
            "image_data": result.get("image_data"),      # The actual image!
            "story_state": story_state,                   # For displaying context
            "prompt_used": result.get("prompt_used", ""), # What we asked AI
            "error": result.get("error")                  # Error message if failed
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/story_state")
async def get_story_state(session_id: str):
    """
    Get the current Story Bible state for a session.
    
    ROUTE: GET /api/story_state?session_id=xxx
    
    Useful for displaying character info in the UI
    or debugging the AI's understanding of the story.
    
    Args:
        session_id: Which session to get state for
        
    Returns:
        JSON with the current story state
    """
    if session_id not in reading_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = reading_sessions[session_id]
    
    return JSONResponse({
        "success": True,
        "session_id": session_id,
        "story_state": session.story_bible.to_dict()
    })


@app.delete("/api/session/{session_id}")
async def close_session(session_id: str):
    """
    Close a reading session and clean up resources.
    
    ROUTE: DELETE /api/session/{session_id}
    
    Called when user is done reading or closes the page.
    
    CLEANUP:
    - Closes the PDF file
    - Deletes the uploaded file
    - Removes session from memory
    
    Args:
        session_id: Which session to close
        
    Returns:
        JSON confirmation message
    """
    if session_id not in reading_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = reading_sessions[session_id]
    session.close()  # Close the PDF
    
    # Try to delete the uploaded file
    try:
        os.remove(session.pdf_path)
    except:
        pass  # Ignore errors if file already deleted
    
    # Remove from our sessions dictionary
    del reading_sessions[session_id]
    
    return JSONResponse({
        "success": True,
        "message": "Session closed"
    })


# ========================================
# STARTUP & SHUTDOWN EVENTS
# ========================================
# These functions run when the server starts/stops

@app.on_event("startup")
async def startup_event():
    """
    Initialize resources when the server starts.
    
    This runs ONCE when you start the server (uvicorn).
    Use it for:
    - Creating directories
    - Setting up database connections
    - Loading models
    """
    # Upload directory is already set up in the global scope
    print("🎨 MyMangaka is ready!")
    print("📚 Upload a PDF novel to transform it into manga")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up resources when the server stops.
    
    This runs when you stop the server (Ctrl+C).
    Use it for:
    - Closing database connections
    - Saving state
    - Cleaning up temporary files
    """
    # Close all open reading sessions
    for session_id, session in reading_sessions.items():
        session.close()
    print("👋 MyMangaka shutting down...")


# ========================================
# DIRECT RUN SUPPORT
# ========================================
# This allows running the file directly with: python -m app.main

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    # host="0.0.0.0" makes it accessible on your network
    # port=8000 is the default FastAPI port
    # reload=True automatically restarts when code changes
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
