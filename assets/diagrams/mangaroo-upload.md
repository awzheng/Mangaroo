```eraser.io
title Mangaroo Upload & Session Creation
direction right
"User" [shape: oval, icon: user, color: blue]
"templates/" [color: green] {
  "index.html" [icon: layout, color: green]
  "Validate File" [shape: oval, icon: check]
  "Submit Upload" [shape: oval, icon: send]
}
"app/" [color: purple] {
  "main.py" [icon: server, color: purple]
  "Receive Upload" [shape: oval, icon: inbox]
  "Save to Disk" [shape: oval, icon: save]
}
"core/" [color: orange] {
  "pdf_processor.py" [icon: file-code, color: orange]
  "Open PDF" [shape: oval, icon: folder-open]
  "Extract Metadata" [shape: oval, icon: info]
  
  "story_manager.py" [icon: brain, color: orange]
  "Initialize Bible" [shape: oval, icon: book]
}
"uploads/" [shape: cylinder, icon: database, color: blue]
"reading_sessions{}" [shape: cylinder, icon: server, color: blue]
"User" > "index.html": Upload PDF
"index.html" > "Validate File": "Check .pdf, <50MB"
"Validate File" > "Submit Upload"
"Submit Upload" > "main.py": "POST /api/upload"
"main.py" > "Receive Upload": "upload_pdf()"
"Receive Upload" > "Save to Disk": "Write with session_id"
"Save to Disk" > "uploads/": "Store file"
"Save to Disk" > "pdf_processor.py": PDFProcessor (path)
"pdf_processor.py" > "Open PDF": "fitz.open()"
"Open PDF" > "Extract Metadata": "get_metadata()"
"Extract Metadata" > "story_manager.py": "Return to main.py"
"story_manager.py" > "Initialize Bible": "StoryBible()"
"Initialize Bible" > "reading_sessions{}": "Create ReadingSession"
"reading_sessions{}" > "User": "Redirect /reader/{id}"
```