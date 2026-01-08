```eraser.io
title Mangaroo Reader Text Display
direction down
"User" [shape: oval, icon: user, color: blue]
"templates/" [color: green] {
  "reader.html" [icon: layout, color: green]
  "Request Text" [shape: oval, icon: send]
  "Display Text" [shape: oval, icon: text]
}
"app/" [color: purple] {
  "main.py" [icon: server, color: purple]
  "Lookup Session" [shape: oval, icon: search]
  "Return JSON" [shape: oval, icon: file-text]
  "reading_sessions{}" [shape: cylinder, icon: server, color: purple]
}
"core/" [color: orange] {
  "pdf_processor.py" [icon: file-code, color: orange]
  "Extract Page" [shape: oval, icon: text]
  "Clean Text" [shape: oval, icon: filter]
}

"User" > "reader.html": "Load page"
"reader.html" > "Request Text": "GET /api/get_page_text"
"Request Text" > "main.py": ?session_id =...&page=N
"main.py" > "Lookup Session": "get_page_text()"
"Lookup Session" > "reading_sessions{}": "sessions[id]"
"reading_sessions{}" > "pdf_processor.py": "session.processor"
"pdf_processor.py" > "Extract Page": "get_page_text(N)"
"Extract Page" > "Clean Text": "_clean_text()"
"Clean Text" > "Return JSON": "Return to main.py"
"Return JSON" > "Display Text": "Send response"
"Display Text" > "User": "Show in left panel"
```