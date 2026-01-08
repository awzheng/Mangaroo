```eraser.io
title Mangaroo Image Generation
direction down

"User" [shape: oval, icon: user, color: blue]

"templates/" [color: green] {
  "reader.html" [icon: layout, color: green]
  "Click Generate" [shape: oval, icon: wand]
  "Display Image" [shape: oval, icon: image]
}

"app/" [color: purple] {
  "main.py" [icon: server, color: purple]
  "Lookup Session" [shape: oval, icon: search]
  "Get Page Text" [shape: oval, icon: text]
  "reading_sessions{}" [shape: cylinder, icon: server, color: purple]
}

"core/story_manager/" [color: blue] {
  "story_manager.py" [icon: brain, color: blue]
  "Analyze Scene" [shape: oval, icon: refresh]
}

"core/image_gen/" [color: pink] {
  "image_gen.py" [icon: image, color: pink]
  "Build Prompt" [shape: oval, icon: edit]
  "Generate Image" [shape: oval, icon: wand]
}

"Google Gemini 1.5 Pro" [shape: cloud, icon: brain, color: blue]
"Google Imagen 3" [shape: cloud, icon: image, color: green]



"User" > "reader.html": "On reader page"
"reader.html" > "Click Generate": "Button click"
"Click Generate" > "main.py": "POST /api/generate_panel"
"main.py" > "Lookup Session": "generate_panel()"
"Lookup Session" > "reading_sessions{}": "sessions[id]"
"reading_sessions{}" > "Get Page Text": processor.get_ page_text()
"Get Page Text" > "story_manager.py": bible.update_ state(text)
"story_manager.py" > "Analyze Scene": "update_state()"
"Analyze Scene" > "Google Gemini 1.5 Pro": "Extract chars/scene"
"Google Gemini 1.5 Pro" > "image_gen.py": "Return state JSON"
"image_gen.py" > "Build Prompt": generate_from_ story_bible()
"Build Prompt" > "Generate Image": "_build_prompt()"
"Generate Image" > "Google Imagen 3": client.models. generate_image()
"Google Imagen 3" > "Display Image": "Return to main.py"
"Display Image" > "User": "Show in right panel"
```