# MyMangaka 📚✨

> AI-Powered Smart Reader - Transform your novels into stunning manga illustrations

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

MyMangaka is an AI-powered web application that transforms PDF novels into manga-style visual experiences. It reads your novel page-by-page and generates beautiful manga illustrations that maintain visual continuity throughout your story.

### Key Features

- 📖 **Smart PDF Processing** - Extracts text page-by-page with clean formatting
- 🧠 **Story Bible Technology** - Maintains character appearances, settings, and visual continuity
- 🎨 **AI Manga Generation** - Creates beautiful manga-style illustrations using Google's Imagen 3
- 🖥️ **Split-Screen Reader** - Novel text on the left, manga panels on the right
- 🎯 **Webtoon-Inspired UI** - Clean, modern design with smooth animations

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Jinja2 Templates, TailwindCSS (CDN)
- **PDF Engine**: PyMuPDF (fitz)
- **AI Engine**: Google Generative AI (Gemini 1.5 Pro + Imagen 3)

## Installation

### Prerequisites

- Python 3.9 or higher
- Google Cloud account with Generative AI API access

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MyMangaka.git
   cd MyMangaka
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Edit the `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   Get your API key from: https://aistudio.google.com/app/apikey

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8000`

## Usage

1. **Upload a PDF** - Drop your novel PDF on the upload page
2. **Read & Generate** - Navigate through pages using the controls
3. **Generate Panels** - Click "Generate" to create manga illustrations
4. **View Story Context** - Toggle the Story Bible to see character/scene tracking

## Project Structure

```
MyMangaka/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Environment configuration
│   │   ├── pdf_processor.py # PDF text extraction
│   │   ├── story_manager.py # Story Bible (context management)
│   │   └── image_gen.py     # Imagen 3 integration
│   ├── templates/
│   │   ├── index.html       # Upload page
│   │   └── reader.html      # Split-screen reader
│   └── static/
│       └── css/
│           └── styles.css   # Custom styles
├── uploads/                  # Uploaded PDFs (created automatically)
├── requirements.txt
├── .env                      # Environment variables
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Upload page |
| `/reader/{session_id}` | GET | Reader interface |
| `/api/upload` | POST | Upload PDF file |
| `/api/get_page_text` | GET | Get text for a specific page |
| `/api/generate_panel` | POST | Generate manga panel |
| `/api/story_state` | GET | Get current Story Bible state |
| `/api/session/{session_id}` | DELETE | Close reading session |

## Design System

| Element | Value |
|---------|-------|
| Primary Color | `#60D071` (Webtoon Green) |
| Secondary Color | `#3C3C3C` (Dark Grey) |
| Background | `#FFFFFF` / `#F8F8F8` |
| Header Font | Futura |
| Body Font | Inter |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` | Previous page |
| `→` | Next page |
| `G` | Generate manga panel |

## Story Bible

The Story Bible is a core feature that maintains visual continuity across pages. It tracks:

- **Characters**: Names, appearances, clothing
- **Settings**: Locations, time of day, atmosphere
- **Visual Style**: Recommended art direction for each scene
- **Story Summary**: Running context of the narrative

This ensures that when you generate a manga panel on page 50, characters look consistent with how they appeared on page 1.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI team for Gemini and Imagen
- FastAPI for the excellent web framework
- The manga and webtoon community for design inspiration

---

Made with ❤️ by the MyMangaka team

