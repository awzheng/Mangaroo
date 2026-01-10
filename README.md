# Mangaroo

> AI-Powered Smart Reader - Transform your novels into manga illustrations

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ‼️ Read the DevLog ‼️

I documented the entire development process, technical decisions, and reasoning behind every design choice in the devlog. It covers system design diagrams and decisions, and all the lessons learned along the way. No AI slop, fully authentic. I promise.

Also, I do not support the monetization of AI art. I am using AI art purely for the purpose of this project as a proof of concept and to design a system with FastAPI.

Check it out here: [devlog.md](devlog.md)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Overview

Mangaroo is a web application that transforms PDF novels into manga-style visual experiences. It uses AI to read your novel page-by-page and generate manga illustrations that maintain visual continuity throughout your story.

The app features a Story Bible that tracks characters, settings, and visual elements across pages to ensure consistent art style and character appearances, similar to how a TV show maintains continuity across episodes.

## Diagrams

### Upload & Session Creation

![Upload & Session Creation](assets/diagrams/mangaroo-upload.png)

### Reader Text Display

![Reader Text Display](assets/diagrams/mangaroo-text.png)

### Image Generation

![Image Generation](assets/diagrams/mangaroo-image.png)

### Story Bible Logic

![Story Bible](assets/diagrams/mangaroo-bible.png)

## Features

- **Smart PDF Processing** - Extracts text page-by-page with automatic cleaning and formatting
- **Story Bible Technology** - Maintains character appearances, settings, and visual continuity using AI context tracking
- **AI Manga Generation** - Creates manga-style illustrations using Google's Imagen 3
- **Split-Screen Reader** - Novel text on the left, manga panels on the right
- **Webtoon-Inspired UI** - Clean design with smooth animations and keyboard shortcuts
- **Session Management** - Remembers your place across multiple reading sessions

## Tech Stack

**Backend:**
- FastAPI - Modern, async Python web framework
- Uvicorn - ASGI server
- PyMuPDF (fitz) - PDF text extraction
- Pydantic - Settings management and validation

**Frontend:**
- Jinja2 - Server-side HTML templating
- TailwindCSS (CDN) - Utility-first CSS framework
- Vanilla JavaScript - No frameworks needed

**AI:**
- Google Gemini 1.5 Pro - Text analysis and Story Bible updates
- Google Imagen 3 - Manga-style image generation

## Installation

### Prerequisites

Before you begin, ensure you have:
- **Python 3.9 or higher** installed ([Download here](https://www.python.org/downloads/))
- A **Google Cloud account** with API access
- **Git** (optional, for cloning the repository)

### Step-by-Step Setup

#### 1. Get the Code

Clone the repository or download it as a ZIP:

```bash
git clone https://github.com/awzheng/Mangaroo.git
cd Mangaroo
```

If you downloaded a ZIP file, extract it and navigate to the folder in your terminal.

#### 2. Create a Virtual Environment

A virtual environment keeps your project dependencies separate from other Python projects.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

#### 3. Install Dependencies

With the virtual environment active, install all required packages:

```bash
pip install -r requirements.txt
```

This will install FastAPI, Uvicorn, PyMuPDF, Google AI libraries, and other dependencies.

#### 4. Get Your API Key

Mangaroo requires a Google Gemini API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key (starts with `AIza...`)

**Important:** Keep this key private. Never commit it to version control.

## Configuration

### Setting Up Environment Variables

1. Create a file named `.env` in the project root (same folder as `README.md`)
2. Add your API key to the file:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the key you copied from Google AI Studio.

### Optional Settings

You can customize other settings in the `.env` file:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (these have defaults)
APP_NAME=Mangaroo
DEBUG=false
UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=50
MAX_CONTEXT_LENGTH=8000
IMAGE_STYLE=manga
```

## Running the Application

### Quick Start

With your virtual environment activated and API key configured:

```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Will watch for changes in these directories: ['/path/to/Mangaroo']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Mangaroo is ready!
Upload a PDF novel to transform it into manga
INFO:     Application startup complete.
```

### Opening the App

Open your web browser and navigate to:
```
http://localhost:8000
```

or

```
http://127.0.0.1:8000
```

You should see the Mangaroo upload page.

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

### Production Deployment

For production, remove the `--reload` flag and consider using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Usage

### Uploading a PDF

1. Open the app in your browser (`http://localhost:8000`)
2. Drag a PDF novel onto the upload area, or click to browse
3. The app accepts PDFs up to 50MB in size
4. Click "Start Reading" to begin

### Reading Interface

Once uploaded, you'll see the split-screen reader:

- **Left Panel:** Novel text for the current page
- **Right Panel:** Manga illustration area
- **Top Bar:** Page navigation and controls

### Generating Manga Panels

1. Read the text on the current page
2. Click the "Generate" button in the top right
3. Wait 10-30 seconds for the AI to create the illustration
4. The manga panel will appear on the right side

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` or `A` | Previous page |
| `→` or `D` | Next page |
| `G` | Generate manga panel for current page |

### Story Bible

Click the "Story Bible" toggle to view the AI's understanding of:
- Characters present in the scene
- Their appearances and clothing
- Current setting and time
- Mood and visual style recommendations

This context helps maintain visual consistency across pages.

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError" when running the app

**Problem:** Python can't find the required packages.

**Solution:**
1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
2. Reinstall dependencies: `pip install -r requirements.txt`

#### "Error: API key not configured"

**Problem:** The app can't find your Gemini API key.

**Solution:**
1. Check that `.env` file exists in the project root
2. Verify the file contains `GEMINI_API_KEY=your_key_here`
3. Make sure there are no spaces around the `=` sign
4. Restart the server after editing `.env`

#### "Address already in use" error

**Problem:** Port 8000 is already being used by another application.

**Solution:**
1. Stop any other servers running on port 8000
2. Or use a different port: `uvicorn app.main:app --port 8001`

#### Virtual environment not activating on Windows

**Problem:** Windows security policy blocks script execution.

**Solution:**
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again: `venv\Scripts\activate`

#### Image generation fails or times out

**Problem:** The manga generation button shows an error.

**Possible causes:**
1. API key is invalid or expired - check your Google AI Studio account
2. API quota exceeded - you may need to upgrade your plan
3. Network connectivity issues - check your internet connection
4. The AI safety filters blocked the content - try different text

#### PDF upload fails

**Problem:** Upload shows an error message.

**Possible causes:**
1. File is larger than 50MB - compress the PDF or split it
2. File is corrupted - try opening it in a PDF reader first
3. File is not actually a PDF - check the file extension

### Checking Logs

For detailed error messages, check the terminal where the server is running. Error messages will appear there.

### Recreating the Virtual Environment

If you're having persistent issues, try recreating the virtual environment:

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv  # On Windows: rmdir /s venv

# Create fresh environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Still Having Issues?

1. Check that you're using Python 3.9 or higher: `python --version`
2. Verify all files are in place (see Project Structure below)
3. Try running with debug mode: add `DEBUG=true` to your `.env` file
4. Check the [GitHub Issues](https://github.com/awzheng/Mangaroo/issues) page

## Project Structure

```
Mangaroo/
├── app/                      # Main application code
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI app and routes
│   ├── core/                # Core functionality modules
│   │   ├── __init__.py
│   │   ├── config.py        # Settings and environment variables
│   │   ├── pdf_processor.py # PDF text extraction
│   │   ├── story_manager.py # Story Bible AI context tracking
│   │   └── image_gen.py     # Imagen 3 manga generation
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── index.html       # Upload page
│   │   └── reader.html      # Reading interface
│   └── static/              # Static assets
│       └── css/
│           └── styles.css   # Custom CSS styles
├── uploads/                  # Uploaded PDF storage (auto-created)
├── venv/                     # Virtual environment (you create this)
├── .env                      # Environment variables (you create this)
├── .gitignore               # Git ignore patterns
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── vercel.json              # Deployment configuration
```

## API Reference

The app exposes a REST API documented at `http://localhost:8000/docs` when running.

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Upload page HTML |
| `/reader/{session_id}` | GET | Reader interface HTML |
| `/api/upload` | POST | Upload PDF and create session |
| `/api/get_page_text` | GET | Get text for specific page |
| `/api/generate_panel` | POST | Generate manga panel |
| `/api/story_state` | GET | Get Story Bible state |
| `/api/session/{session_id}` | DELETE | Close reading session |

### Example: Upload a PDF

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@mynovel.pdf"
```

Response:
```json
{
  "success": true,
  "session_id": "abc123",
  "redirect_url": "/reader/abc123",
  "filename": "mynovel.pdf",
  "total_pages": 250
}
```

## Design System

### Colors

| Element | Value | Usage |
|---------|-------|-------|
| Primary | `#60D071` | Buttons, highlights, accents |
| Secondary | `#3C3C3C` | Text, borders |
| Background | `#FFFFFF` | Main background |
| Surface | `#F8F8F8` | Card backgrounds |

### Typography

- **Headings:** Futura
- **Body:** Inter
- **Monospace:** System default

## Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Open a Pull Request

Please ensure your code:
- Follows the existing style
- Includes comments for complex logic
- Works with Python 3.9+
- Doesn't break existing functionality

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Google Generative AI team for Gemini and Imagen APIs
- FastAPI team for the excellent web framework
- PyMuPDF developers for the PDF processing library
- The manga and webtoon community for design inspiration

## Support

- **Documentation:** See this README
- **Issues:** [GitHub Issues](https://github.com/awzheng/Mangaroo/issues)
- **API Docs:** `http://localhost:8000/docs` when running

---

Made by Andrew Zheng
