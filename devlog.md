# Mangaroo DevLog

This is the start of an authentic and energetic devlog about why and how I built Mangaroo. 
I will justify all of my design choices by sharing my thought processes for every decision I made as I was building Mangaroo. 
I have also included the most frequently asked questions (and the questions that I asked myself!) into this devlog to answer the most common concerns about the project! 
I would appreciate any feedback you may have!

Instagram, Discord @awzheng

## Important: Devlog Updates Underway

Thanks so much for dropping by the Mangaroo DevLog.
You may notice that some parts of the devlog are currently under construction.
That's because I'm in the process of revamping it to match the quality of my other projects, SageWall and Crawlstars.
See them here: [CrawlStars Devlog](https://github.com/awzheng/CrawlStars/blob/main/devlog.md) and [SageWall Devlog](https://github.com/awzheng/SageWall/blob/main/devlog.md)

With WaterlooWorks and ECE 1B filling up my schedule, progress has been halted for now.
I will continue to update the devlog as I make progress on Mangaroo!
Thank you for your patience!
Please show my other projects your support by reading my dev journey!

## Why I made Mangaroo

I've always wondered about the psychology behind what makes some books more memorable and "readable" than others.
How come it was so easy for me as a child in the early 2010s to be content with rereading Diary of a Wimpy Kid and Pokemon books over and over again?
By no means was I a picky reader.
My favourite genre of books was still nonfiction, but fiction has always had a soft spot in my heart.

It's quite strange as well.
I personally believe that these kinds of books were the earliest forms of "brainrot" that I was introduced to, namely books like Diary of a Wimpy Kid and Big Nate.
They were undeniably below the reading level of their target audience (middle school kids), but I found them engaging enough to always drop a quick 15-minute flash read whenever I bumped into them at the bookstore or library.

I also found the same effect when interacting with manga.
By that, I'm talking about reading the limited amount of manga that could be found in Toronto libraries and bookstores.
(I wasn't immersed into the online scene as a child, but I'm very thankful for that.)

However, that doesn't mean that I don't like manga.
Lots of manga are so satisfying to read and reread over and over again since they're immersive and dynamic.
They're a super effective medium for storytelling, and I can see it working for nonfiction works as well, such as biographies and documentaries.

Big disclaimer: I don't support AI art, but since my project is a non-monetized personal adventure, I'm fine with enjoying the results of AI labour in a system that I designed personally.

> Andrew! Do you read manga?

No, not at the moment, but I used to (sometimes), and I'm open to suggestions!

# Episode 1: Starting Out

Now that we got the intro out of the way (please don't attack me for "using AI art!"), we can start the system design process (my favourite).

The main intention behind making Mangaroo was to build something using the FastAPI framework.

## Understanding FastAPI

> Andrew! What's FastAPI? What's a framework?

Before I explain what FastAPI is, let me explain what a framework is.

A framework is a prebuilt collection of code and tools that we use to build our app.

> No! That's a library! Wait, what's the difference between a library and a framework?

Well said!
Yes, a library is a collection of tools.
However, what makes a framework different from a library is the inversion of control.

FastAPI controls the flow of our app and calls our code when specific events trigger HTTP requests (such as user uploading a PDF or clicking Generate). 

As an example, let's say that a reader clicks the Generate button on page 1 of the pdf that they uploaded.
Here's the sequence of events:
1. User clicks "Generate" in the browser
2. JavaScript sends an HTTP POST request to `/api/generate_panel'
3. FastAPI is always listening, and it receives the HTTP request.
4. We get to tell FastAPI exactly what to do when these events trigger. In this case, it's the `generate_panel()` function in python.

FastAPI provides structure to the chaos of our app and is gonna make development a lot smoother.

To me, that's a meaningful advantage in terms of efficiency and productivity.
I chose FastAPI to be the foundation of Mangaroo since it's the perfect tool to call Gemini and Imagen APIs while also practicing my software and system design skills.

Yes, remember that we're using using two AIs in sequence: Gemini and Imagen.
FastAPI natively supports Python's `async` and `await` keywords, which is perfect for our use case. 

> Andrew! What's async and await? Why not just use threads?

Async is way more efficient than threads!
While we wait for Gemini and Imagen APIs to respond to our requests, we can still handle other eaders' requests without the cost of thread context switching.

The server will be able to handle requests from multiple users (readers) concurrently.

For example, while we wait for Gemini to handle a request from Reader A, FastAPI can still start to process a request from Reader B.
The flow of the app won't be held up for any other users by waiting for Gemini and Imagen to respond to Reader A's request.

FastAPI has some other useful features too, notably Swagger UI. 
Swagger is automatically generated by FastAPI at `/docs` (by visiting `http://localhost:8000/docs`).

If you're a fan of these concepts, I recommend checking out the [CrawlStars Devlog](https://github.com/awzheng/CrawlStars/blob/main/devlog.md) which contains concurrency and REST API concepts using Golang and MongoDB.

> Andrew! What? How does swagger generate the docs/documentation automatically? What's the mechanism behidn it?

Swagger docs are generated automatically by FastAPI by the following clues.
- Our route decorators such as `@app.post("/api/upload")`, aka a special syntax that links a function to a specific HTTP request
- Python gives type hints in the function signature, aka defining the expected input and output types
- Docstrings in route functions (if applicable)

It also provides a `/redoc` endpoint as an alternative interface (by visiting `http://localhost:8000/redoc`).
It makes our API documentation way more human-readable so that we can test our endpoints and easily identify bugs.

> Andrew, I now understand what FastAPI is. However, what's Uvicorn?

Uvicorn is an ASCI server that runs our FastAPI application written in python.
ASGI stands for async server gateway interface, making it perfect for our async FastAPI application.
When we run `uvicorn app.main:app`, we're essentially saying "Uvicorn, please run our FastAPI app defined in app/main.py".

## Project Diagrams

I have to confess that I spend 3 entire days just figuring out how to design and lay out the system on eraser.io.
I have sooo many failed attempts that you can view in the appendix.
I had to redo my diagrams and decided to follow the same format as my more recent projects, SageWall and CrawlStars.

See them here: [CrawlStars Devlog](https://github.com/awzheng/CrawlStars/blob/main/devlog.md) and [SageWall Devlog](https://github.com/awzheng/SageWall/blob/main/devlog.md)

### Upload Path

![Upload path system diagram](assets/diagrams/mangaroo-upload.png)

### Text Display Path

![Text display path system diagram](assets/diagrams/mangaroo-text.png)

### Image Generation Path

![Image generation path system diagram](assets/diagrams/mangaroo-image.png)

### Story Bible Logic

![Story bible logic system diagram](assets/diagrams/mangaroo-bible.png)

> Andrew! Story bible? What's a story bible?

The story bible is a class that contains the context of the story in order to generate images that are precise and consistent to the reader's session experience.

For example, let's say we **didn't** use a story bible. If we sent two completely seperate requests to generate images for consecutive pages, the style of the images generated could be completely different.

We *could* throw all our credits by asking Gemini to repeatedly read images and generate a new image based on the images' visual style, but that would get very slow for novels with hundreds of pages and tons of context.

By storing data from each consecutive page using our handy story bible, the AI won't get lost or lost context, thus we'll end up with more consistent images.

### Project Structure

I aimed for a general three-layer architecture as shown below.
```
[Green] Presentation Layer
    ↓
[Purple] Business Logic Layer
    ↓
[Other] Data Access Layer
```
Currently, the business logic layer makes direct external API calls to Gemini and Imagen.
In a larger system, I'd use the Data Access layer to handle external API calls.

And here's the project's core file structure:

```
Mangaroo/
├── api/
│   ├── __init__.py
│   └── index.py                    # Vercel serverless entry point
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application & routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings & environment variables
│   │   ├── pdf_processor.py       # PDF text extraction
│   │   ├── story_manager.py       # Story Bible (Gemini analysis)
│   │   └── image_gen.py           # Image generation (Imagen 3)
│   ├── static/
│   │   └── css/                    # Stylesheets
│   └── templates/
│       ├── index.html              # Upload page
│       └── reader.html             # Reading interface
├── uploads/                        # Temporary PDF storage
├── .env                            # API keys (not in git)
├── requirements.txt                # Python dependencies
├── vercel.json                     # Vercel deployment config
└── README.md
```

Here are some brief descriptions of the project structure in table format:

| Directory/File | Description | Notable Member Functions |
|----------------|-------------|-------------------------|
| `api/index.py` | Vercel serverless entry point that imports the FastAPI app for deployment | N/A |
| `app/main.py` | Main FastAPI application with all route handlers and session management | `upload_pdf()`, `get_page_text()`, `generate_panel()`, `reader()`, `ReadingSession` class |
| `app/core/config.py` | Configuration management using Pydantic to load environment variables from .env file | `get_settings()`, `ensure_upload_dir()`, `Settings` class |
| `app/core/pdf_processor.py` | Handles PDF file operations and text extraction using PyMuPDF | `PDFProcessor.open()`, `PDFProcessor.get_page_text()`, `PDFProcessor.get_metadata()`, `extract_page_text()` |
| `app/core/story_manager.py` | Story Bible that maintains narrative context across pages using Gemini API | `StoryBible.update_state()`, `StoryBible.get_image_prompt()`, `StoryBible._build_analysis_prompt()` |
| `app/core/image_gen.py` | Manga panel generation using Google Imagen 3 API | `ImageGenerator.generate_panel()`, `ImageGenerator.generate_from_story_bible()`, `get_image_generator()` |
| `app/templates/` | Jinja2 HTML templates for the web interface | N/A |
| `app/static/css/` | CSS stylesheets for the frontend | N/A |
| `uploads/` | Directory for temporary storage of uploaded PDF files (local dev only, uses /tmp on Vercel) | N/A |

## My plans to scale Mangaroo's System Design

Yes, I know, lots of people tend to stuff their future plans to the bottom of their writing.
However, since I always start my devlog Episode 1 from a system design standpoint, I'm willing to show off the potential of Mangaroo and get a clear idea of what I can do to scale it.

Let's face it, I'm currently in 1B and I haven't had the time to scale Mangaroo yet.
Lots of my time after building Mangaroo has been spent on CrawlStars, SageWall, school, and co-op search.

However, my plans for the future are to scale this project using my knowledge of distributed systems gained from my other projects, CrawlStars and SageWall.
I'll be revisting the Mangaroo system design in the future and here are some of my plans to take Mangaroo to the next level:

> Andrew, your story bible works for sessions, but how would we scale Mangaroo to a distributed system?

We would have to store the story bibles in a database.
I would choose a database such as MongoDB since it's a NoSQL database that's easy to scale and provides a lot of features out of the box.

A reasonable step in-between where we are now (sessions lost on server refresh) and database storage heaven is to store session IDs in cookies or tokens. 
Additionally, we should implement session cleanup in order to prevent memory leaks.

We could also store the user's PDF file uploads on a cloud database such as AWS S3, which I used in SageWall (read the devlog here: https://github.com/andrewzheng/SageWall/blob/main/devlog.md)

Now that we've established the scope and functions behind Mangaroo, let's get building!

