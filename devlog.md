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

Uvicorn is an ASGI server that runs our FastAPI application written in python.
ASGI stands for Async Server Gateway Interface, making it perfect for our async FastAPI application.
It also supports other features in case I wish to expand Mangaroo or experiment with other tools:
- WebSocket support
- HTTP/2 support
- HTTP/3 support
- Long-lived connections (reusing connections for multiple requests)

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

# Episode 2: Upload Path

My devlogs follow the path of data flow through the system diagram. 
We'll begin by examining `main.py` and follow through all the functions in the upload path.
Don't worry about frontend yet, Episode 3 covers reader UI in more depth!

![Upload path diagram](assets/diagrams/mangaroo-upload.png)

## main.py 

The general path within `main.py` includes session creation, the upload route, and saving the upload path to the session.

### ReadingSession

`ReadingSession` is the backbone of our upload flow. Each PDF upload creates one session object that coordinates the PDF processor, Story Bible, and user state. 

> Andrew! Why create a whole class for sessions? Why not just use a dictionary to store PDF paths?

Making a class is better because classes group both data and methods (functions).
Each session manages its own cleanup using `close()`, and sets its own processor and story bible.
It also includes type safety, making it easier to understand what a session contains.

Each user's ReadingSession is composed of other objects such as PDFProcessor and StoryBible.
Thus, the typical life cycle for a ReadingSession is construction → active use → cleanup.

In case you're still wondering about dictionaries:
Dictionaries store data, but classes encapsulate both data AND behavior. 
Our ReadingSession needs methods like `close()` to manage its own lifecycle.
A dictionary can't clean up after itself since it's just a data container.

Furthermore, classes provide a clear API contract (what methods exist) that dictionaries don't offer. 
Type hints help, but they don't enforce behavior.

```python
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
```

As you can see, ReadingSession just contains our init and close functions which are just the fundamentals of object-oriented programming.
`close()` is important to avoid memory leaks.

> Andrew! What happens when the server restarts?

At the moment, when the server restarts, user sessions are lost.

> Seriously? How do you plan to scale this?

We could store the sessions in cookies or a database if we wanted to.
If you love databases, I would highly recommend checking out [CrawlStars](https://github.com/andrewzheng/CrawlStars) (MongoDB) and [SageWall](https://github.com/andrewzheng/SageWall) (AWS S3)!

Also, I don't plan to commercialize this anytime soon.
I would never try to scale something using AI art.
Gross behaviour!
This project is more of a for-fun exercise to prove that I can build a full-stack app using FastAPI.

### upload_pdf() Route Handler

`upload_pdf()` includes the entire upload flow: validation → storage → session creation → response.
It sounds like a lot, but don't worry, we'll go through it step by step.

```python
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and create a reading session.
    
    ROUTE: POST /api/upload
    
    FLOW:
    1. Receive the uploaded file
    2. Validate it (is it a PDF? is it too big?)
    3. Save it to the uploads folder
    4. Create a ReadingSession
    5. Return the session ID so frontend can redirect to reader
    """
    # ---- Step 1: Validate file type ----
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # ---- Step 2: Check file size ----
    settings = get_settings()
    contents = await file.read()  # Read the file contents into memory
    
    if len(contents) > settings.max_file_size_mb * 1024 * 1024:  # Convert MB to bytes
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB"
        )
    
    # ---- Step 3: Generate unique session ID ----
    session_id = str(uuid.uuid4())[:8]
    
    # ---- Step 4: Save the file ----
    safe_filename = f"{session_id}_{file.filename}"
    file_path = Path(UPLOAD_DIR) / safe_filename
    
    with open(file_path, "wb") as f:  # "wb" = write binary
        f.write(contents)
    
    # ---- Step 5: Create reading session ----
    try:
        session = ReadingSession(str(file_path), file.filename)
        reading_sessions[session_id] = session  # Store in our dictionary
        
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "total_pages": session.total_pages,
            "metadata": session.metadata,
            "redirect_url": f"/reader/{session_id}"
        })
    except Exception as e:
        # If something goes wrong, clean up the file we saved
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
```

It starts off by identifying as an API call with `@app.post("/api/upload")`.
Then, it follows the steps below.

#### 1. Validate file type

Our first line of defense is to check the file name to ensure that it's a valid PDF file.
In some systems such as testing the app on Google Chrome on MacOS, the upload file window only allows PDF uploads anyway.

> Andrew! What happens if someone renames a malicious file to have a .pdf extension?

This will be addressed down below when we talk about PyMuPDF!
Just know that for now, we're building multiple security layers that fail independently for a multi-layer defense strategy.

#### 2. Validate file size

After converting MB to bytes, we check that the file is smaller than `settings.max_file_size_mb` which is defined as 50MB in settings from `get_settings()` which retrieves information from `app/core/config.py`.
Here's the excerpt from `config.py` to prove it:

```python
    # Maximum file size allowed (in megabytes)
    # Prevents users from uploading huge files that slow down the server
    max_file_size_mb: int = 50
```
Whew!

> Andrew! Why do we validate both the file extension and file size? Why can't we just try to open it as a PDF?

Slow down, tiger!
It's better to check early and fail fast than to get stuck too deep in a sunk cost.
Extension checking is a super cheap, fast and intuitive way to check if it's a PDF file.

> Andrew! What's the worst that could happen without validation?

Our app might process a malicious file upload causing server crashes or DoS attacks, such as someone uploading a 10GB file.
That's why we have multiple layers of validation to filter out evil users.

> Andrew! What does `await file.read()` do?

Good eye! `await` is one of our FastAPI async keywords.
`await` is used to pause the execution of the current function (and let the cpu work on other tasks)until the awaited operation completes.
In this case, it pauses the `upload_pdf()` function until the file is read.
In the meantime, our app can work on handling other readers' requests, generating images, and managing the story.

Think of Mangaroo as a pizzeria with a single chef (FastAPI).
It takes a while for the pizza (PDF File) to bake (process).
A lazy (synchronous) chef would stand there and watch the pizza bake until it's done.
They would freeze and refuse to take other orders.
An efficient (asynchronous) chef, on the other hand, would use the downtime to take other orders, prepare ingredients, and clean the kitchen.

Thus, in technical terms, while we `await file.read()`, the current coroutine yields control back to the event loop, allowing other coroutines (such as other users' file uploads, story generation, etc.) to run.

Mangaroo is what we call I/O bound because it spends most of its time waiting for I/O operations (file reading, API calls, etc.) to complete.

If Mangaroo did not have async, it would be held up by 2 slow operations on the critical path:
1. File I/O, reading PDFs from disk (which takes ~100ms for a 10MB file)
2. API Calls which take at least 2-3 seconds for Gemini and 5-10 seconds for Imagen

> Andrew! Would `upload_pdf()` still work without `await`?

Unfortunately not.
If it takes too long to read one user's PDF file, our app would be stuck processing that request and wouldn't be able to handle other users' requests.

Using the pizzeria analogy, the lazy chef would be staring at the oven as the customers wait in line, the other pizzas remain unmade, and the kitchen gets dirtier.

Thus, step 2 is an async file size check: the second half of the validation process for reader A's upload.

#### 3. Generate unique session ID

After validating file input, we generate a Universally Unique Identifier (UUID) for reader A's upload.

> Andrew! Why use UUID instead of incrementing numbers (1, 2, 3...) for session IDs? What does `[:8]` do?

UUID is a 128-bit number that is used to identify information in computer systems.
This means that it can range in value from 0 to 2^128 - 1 (think 0...0 to 1...1 in binary), which is approximately 3.4 x 10^38.

Thus, since there are so many possible values, it's virtually impossible for multiple users to share a UUID.
To put it into perspective, the chance of overlap is 1 in 2^64.
You're more likely to be struck by lighting twice while winning the lottery!

On the other hand, if the UIDs were incremental, user 1000 would be able to try accessing session 999 or 1001 and so on.
One user won't accidentally access another user's session.

One tradeoff of having these ridiculously long UUIDs is that they're hard to read and render.
Since the UUID can get really long (making it hard to render/read), `[:8]` is used to truncate it to the first 8 characters to make it more human-readable.

At the moment, the possibility of Mangaroo useres sharing an UUID is negligible.

> Andrew! What if you happened to scale Mangaroo and users shared the same 8-character UID?

There are two main production fixes we could implement to solve that issue.

The first solution would be to check UUID before insert.
If a newly generated UUID already matches an existing 8-character UID, then it will simply be regenerated.

The second solution for a full-enterprise grade platform would be to just use the full UUID.

#### 4. Save the file

Step 4 is quite simple.
We save the file to a session directory with the session ID + original filename as the path.
This is represented in the system design diagram as the cylindrical uploads/ node!

> Andrew! Why save the file instead of just keeping it in memory?

Keeping it in disk has many advantages.
- PyMuPDF (aka Fitz) can't open files in memory. I will explain this in detail below.
- If we're servicing many concurrent users, the price of RAM (many many gigabytes) would get dangerously expensive.
- We've already written the user upload to disk when checking file size.

#### 5. Create reading session

Finally it's time to create a reading session.
It tries to call the `ReadingSession` constructor we defined earlier and stores key information such as session ID, file path, and total pages in a JSON response.

This is an example of a three-layer error architecture.

Layer 1: Validation errors (4xx) such as 400 (file too large/wrong extension), 404 (session not found) where we return user-friendly error messages.

Layer 2: Processing errors (5xx) such as 500 (internal server error such as PDF parsing failed/database down) where we return a generic error message, preventing us from exposing the system internals to the user and instead logging details server-side.

Layer 3: Failure cleanup: our `try/except` block ensures that we delete the file if an error occurs. We won't end up leaking resources when errors bubble up (such as when I ran into many repeated errors when configuring and debugging).

Finally, we're ready to start processing the PDF and extract text to generate images with!

## pdf_processor.py

Moving along the path of the system design diagram: after saving the PDF to the session uploads/ directory, we move on to `pdf_processor.py` to process the PDF.

The `PDFProcessor` class is essentially a wrapper for the the PyMuPDF (fitz) library to safely handle PDF operations. 
It follows the open/close pattern for resource management.

```python
class PDFProcessor:
    """
    Handles PDF file operations and text extraction.
    
    WHAT IS A CLASS?
    - A class is like a blueprint for creating objects
    - It groups related functions (methods) and data together
    - PDFProcessor is our "tool" for working with one PDF file
    
    HOW TO USE:
        processor = PDFProcessor("mybook.pdf")  # Create processor
        processor.open()                         # Open the PDF
        text = processor.get_page_text(0)       # Get page 1 text
        processor.close()                        # Close when done
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize (set up) the PDF processor.
        
        __init__ is a special method that runs when you create a new object.
        
        Args:
            pdf_path: The file path to the PDF (e.g., "uploads/mybook.pdf")
        """
        self.pdf_path = Path(pdf_path)
        
        # These will be set when we open the PDF
        # The underscore prefix (_doc) indicates "private" - internal use only
        self._doc: Optional[fitz.Document] = None  # The PDF document object
        self._total_pages: int = 0                  # Number of pages
        
    def open(self) -> bool:
        """
        Open the PDF document for reading.
        
        WHY SEPARATE OPEN/CLOSE?
        - Opening a file takes resources (memory)
        - We open once, do all our work, then close
        - This is more efficient than opening for each operation
        
        Returns:
            True if the PDF opened successfully, False if there was an error
        """
        try:
            self._doc = fitz.open(self.pdf_path)
            self._total_pages = len(self._doc)
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False
    
    def close(self):
        """
        Close the PDF document and free up memory.
        
        IMPORTANT: Always close files when done!
        """
        if self._doc:
            self._doc.close()
            self._doc = None
    
    @property
    def total_pages(self) -> int:
        """
        Get total number of pages in the PDF.
        
        @property decorator makes this act like a variable:
        - Instead of: processor.total_pages()
        - You write: processor.total_pages
        """
        return self._total_pages
```

Some key notes about `PDFProcessor`:

The constructor initializes the session's state:
- PDF metadata: path, filename, page count
- Story Bible: for tracking narrative context
- Reading position: current_page = 0
- PDF processor: opened and ready to extract text

The open/close pattern is a common practice for file handling in other languages.
Now let's answer your barrage of FAQs:

> Andrew! What's `@property`?

`@property` is a Python decorator.
Decorators are functions that wrap another function to transform its behavior.
Thus, `@property` modifies the `total_pages` method to act like an input variable for the `PDFProcessor` class.

As an example, the first code block below is equivalent to the second block despite their different syntax.

Block 1 (decorator syntax):

```python
@property
def total_pages(self):
    return self._total_pages
```

Block 2 (wrapper syntax):

```python
def total_pages(self):
    return self._total_pages
total_pages = property(total_pages)  # Wrapper
```

> What function do we get from `@property`?

We get the function of being able to access the `total_pages` variable without having to call the `total_pages()` method.

> Why do we need to access `total_pages` without calling the `total_pages()` method?

It makes our future code (which takes `total_pages` as a variable) much easier to read and maintain.
It also made me a more well-rounded and knowledgeable software dev overall!

> Andrew! Why use a wrapper for PyMuPDF instead of using it directly?

Creating a wrapper class is a much better practice in software engineering.
It makes our code way easier to read and maintain.
It can be kinda compared to creating helper functions for custom classes in your object-oriented programming class in order to access typically private or protected variables/functions.

> Andrew! What even is PyMuPDF and why did you choose it over other PDF libraries?

PyMuPDF is a Python binding (a wrapper for code written in other programming languages) for the MuPDF library which is a framework written in C.
That means that, in a way, we have gifted Mangaroo the horsepower of an F1 engine (C) with a simple steering wheel (Python API)!
There are also some alternatives to PyMuPDF, such as PyPDF2 (slower, but more lightweight) and pdfplumber (better for tables).

We've imported `pymupdf` by the name of `fitz` since it's a convention.
It's done a great job at extracting text, and it also has the capability to extract images, metadata, and even render pages.

When PyMuPDF (aka Fitz) opens an invalid file with a .pdf extension, it will throw an exception and we will remain safe.

> Andrew! Why did you separate `__init__()` and `open()`? Why not open the PDF in the constructor?

This comes down the the fact that seperating the initialization (construction) and the function (opening) of an object is a much better practice than keeping them jumbled together.
By seperating `__init__()` and `open()`, we can read and debug the code much more efficiently.
It also makes the resource lifetime explicitly clear.
Thus, we can first focus on creating the `PDFProcessor` object, and then we can decide whether to open the PDF later on.

As an added bonus, our system design diagram (user upload data path) is clear and linear, making it super easy to read and follow, especially for beginners!

## story_manager.py

`StoryBible` is the absolute hero of quantifying what I've achieved through Mangaroo.
By running some calculations, I've narrowed down the fact that I reduced context token usage by **92%** by storing plot context in a JSON instead of forcing Gemini to reread the story and rewatch all of our images every time we want to create a new page (in order to preserve a relatively consistent user experience).

Essentially, the `StoryBible` class maintains narrative context across pages. 
It starts with an empty state and builds up character/scene knowledge (extracted and returned by Gemini) as we read.

```python
class StoryBible:
    """
    The Story Bible maintains narrative and visual context across pages.
    
    ANALOGY: Think of it like a TV show's "series bible"
    - Character sheets: What does each character look like?
    - Setting guides: What does each location look like?
    - Plot summary: What's happened so far?
    
    This ensures visual consistency - like how animated characters
    always look the same episode to episode.
    """
    
    def __init__(self):
        """
        Initialize the Story Bible with an empty state.
        
        The state dictionary tracks everything we know about the story.
        It starts empty and builds up as we read more pages.
        """
        # The main state dictionary - this is what we're tracking
        self.state: Dict = {
            # Description of the current scene for the manga panel
            "current_scene": "",
            
            # List of characters with their visual descriptions
            # Each character: {name, appearance, clothing, expression, position}
            "characters": [],
            
            # Recommended art style for this scene
            # e.g., "dramatic shadows", "soft lighting", "action lines"
            "visual_style": "",
            
            # Running summary of the story so far
            "story_summary": "",
            
            # Emotional tone: "tense", "romantic", "action-packed", etc.
            "mood": "",
            
            # When the scene takes place
            "time_of_day": "",
            
            # Background/setting details
            "location_details": ""
        }
        
        # Set up the connection to Google's AI
        self._configure_genai()
        
    def _configure_genai(self):
        """
        Configure the Google Generative AI client.
        
        This sets up our connection to Google's Gemini AI.
        We need a valid API key for this to work.
        """
        settings = get_settings()
        
        if settings.gemini_api_key:
            # Configure the library with our API key
            genai.configure(api_key=settings.gemini_api_key)
            
            # Create a Gemini 1.5 Pro model instance
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            # No API key - AI features won't work
            self.model = None
```

`StoryBible` contains a dictionary that tracks essential information such as:
- `current_scene`
- `characters`
- `visual_style`
- `story_summary`
- `mood`
- `time_of_day`
- `location_details`

Which we initialize as empty.

> Andrew! What is the "Story Bible" concept? Where does this term come from?

Maintaining a Story Bible (aka show bible or pitch bible) is a practice used in the film industry to keep writing and design on track.
It's not just a word that I made up!
Read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Bible_(screenwriting)).

Having a story bible gives Mangaroo very distinct advantages as a standalone FastAPI app rather than a generic AI wrapper:

- OOP system design
- 92% reduced context token usage
- O(1) memory complexity
- Much faster image generation
- Consistent image generation aka lower chance of AI slop

> Andrew! How did you calculate the reduction in context token usage?

Let's quantify the Story Bible's impact on API costs.
**Control** (no Story Bible):
- Send entire conversation history with each request
- Page 1: 500 tokens (just the text)
- Page 2: 500 + 500 = 1000 tokens (page 1 + page 2)
- Page 3: 500 + 500 + 500 = 1500 tokens
- Pattern: O(n²) token growth
For a 100-page novel:
- Total tokens = 500 × (1 + 2 + 3 + ... + 100) 
- = 500 × 5050 = 2,525,000 tokens

**Story Bible approach**:
- Send only: current page text (500) + JSON context (200)
- Every request: 700 tokens
- Pattern: O(1) token growth
For 100 pages:
- Total tokens = 700 × 100 = 70,000 tokens

(2,525,000 - 70,000) / 2,525,000 = 97.2% reduction!
Even accounting for occasional re-syncs or longer context, we're seeing >90% reduction in practice.

After initializing the `StoryBible`, we call `self._configure_genai()` to configure the connection to Google's AI.

> Andrew! Why Gemini 1.5 Pro instead of Flash or other models?

At the time of making Mangaroo (Nov 2025), Gemini 1.5 Pro was the best model for my use case.
It's great at handling JSON format extraction (character names, descriptions) and reasoning with complex tasks such as extracting story context.
I'm thinking of switching to Gemini 3 Flash in the future.

Anyway, now that our environment is set up and configured correctly, we've reached all nodes in our Upload & Session Creation diagram path. Time to move onto displaying text!

# Episode 3: Reader Text Display Path

Reader text display is a super clean RESTful API design.
- Frontend requests page resources by using stateless GET endpoints
- Backend processes request and returns page resources using session-scoped PDF processors
- Jinja2 bridges server-side data to client-side JavaScript

Thus by seperating our concerns, we can build and improve each layer independently.

![Reader path diagram](assets/diagrams/mangaroo-text.png)

## reader.html

The reader interface uses vanilla JavaScript to fetch page text asynchronously and update the DOM. This creates a smooth, SPA-like experience without a full framework.

The following function `loadPageText` is loaded with exciting async/await, so don't be intimidated by it!

```javascript
/**
 * Load text content for a specific page
 * Called when navigating between pages
 * @param {number} page - Page number to load (0-indexed)
 */
async function loadPageText(page) {
    try {
        // Fetch page text from API
        const response = await fetch(`/api/get_page_text?session_id=${sessionId}&page=${page}`);
        const data = await response.json();

        if (data.success) {
            // Format text into paragraphs
            // Split on double newlines (paragraph breaks)
            const paragraphs = data.text.split('\n\n').filter(p => p.trim());
            const formattedText = paragraphs.map(p => `<p>${p.trim()}</p>`).join('');

            // Insert text with fallback for empty pages
            textDisplay.innerHTML = formattedText || '<p class="text-gray-400 text-center">This page appears to be empty.</p>';

            // Add page turn animation
            textDisplay.classList.add('page-turn-animation');
            setTimeout(() => {
                textDisplay.classList.remove('page-turn-animation');
            }, 400);

            // Update state
            currentPage = page;
            currentPageSpan.textContent = page + 1;  // Display as 1-indexed

            // Update navigation buttons
            prevBtn.disabled = !data.has_prev;
            nextBtn.disabled = !data.has_next;

            // Scroll text panel to top
            document.getElementById('textContent').scrollTop = 0;

            // Reset manga panel for new page
            resetMangaPanel();
        } else {
            showToast('Error loading page');
        }
    } catch (error) {
        console.error('Error loading page:', error);
        showToast('Error loading page');
    }
}

// Event Listeners - wire up buttons to functions
prevBtn.addEventListener('click', () => {
    if (currentPage > 0) {
        loadPageText(currentPage - 1);
    }
});

nextBtn.addEventListener('click', () => {
    if (currentPage < totalPages - 1) {
        loadPageText(currentPage + 1);
    }
});

// [...]

// Initialize: load first page when page loads
loadPageText(0);
```

Aha!
Our function is an `async function` which means that it returns not an immediate value but a Promise!
A Promise is a type of object that represents a value that may not be available yet, but will be in the future.

In this case, `loadPageText` returns a Promise that gets resolved when the page text is loaded.

> Andrew! What does the Promise contain? What will it look like once it's resolved?

The Promise will contain the page text once it's resolved.

> Andrew! Why do we need to make this an async/await function? Wouldn't it be faster if it was just a normal function?

Well, remember that we're making an API call to the FastAPI backend. 
This is an asynchronous operation, so we need to use async/await to handle it.
It preserves our "pizzeria" strategy of not blocking the main thread while waiting for the API call to complete.

Using async/await also makes the code more readable and easier to understand for humans.
It's much easier to read than a nested callbacks or promises.
That's how we avoid what some developers call "callback hell" or the "pyramid of doom".

Now, let's move onto the try catch block.
You'll first notice 2 consts: `response` and `data`.

- `response` is the raw response from the API call, meaning that it's a `Response` object from the `fetch` API.
- `data` is the JSON data from the API call, meaning that it's a parsed JSON object from the `response.json()` call. It's esssentially just `response` turned into a JSON object.

If we're successful in our API call, we'll get a `success` key set to `true` and a `text` key set to the page text.
Then, we simply format the `data` into HTML and insert it into the document object model (DOM) for reader display as the `currentPage` state.

We also call `resetMangaPanel` to reset the manga panel for the new page.

In case of an error in the try-catch block or the API call fails, we'll tell the user that there was an error loading the page.

> Andrew! Why did you decide to use vanilla JavaScript instead of React/Vue/Svelte?

Vanilla JavaScript is a good choice for this use case because it illustrates the core concepts behind web development and API calls. 
I already have meaningful experience with React for my personal website, so I don't want to overcomplicate this project with a framework.
Instead, I'm staying true to fundamentals and showing API calls in action.

The tradeoff is that we have to do more manual DOM manipulation and less component reusability, but it's a good learning experience.
For an ereader that focuses on system design and backend expansions, vanilla JS is already enough.

> Andrew! Speaking of API fundamentals, what even is `fetch()`?

`fetch()` is a modern, promise-based API for making HTTP requests.
It was really clean syntax with async/await.
Plus, it returns a `Response` object which handles errors well since it doesn't immediately reject on HTTP errors.

### Jinja2 Template Variables

The reader.html template receives data from the FastAPI backend via Jinja2 templating.
This bridges Python handling our backend and JavaScript handling our frontend.

```html
<script>
    // These values come from Jinja2 template variables
    // They're set in main.py when rendering this page
    const sessionId = '{{ session_id }}';    // Unique ID for this reading session
    // eslint-disable-next-line
    const totalPages = {{ total_pages | default(0) }};    // How many pages in the PDF

    // Track current state
    let currentPage = 0;        // Which page we're on (0-indexed)
    let isGenerating = false;   // Prevent multiple simultaneous generations
</script>
```

> Andrew! What is Jinja2 and why do we need it?

Jinja2 is what we call a templating engine for Python.
It lets you embed Python values in HTML, using the `{{ variable_name }}` syntax.
It processes our template server-side before sending it to the reader's browser.

This makes data available immediately to the reader's browser, and reduces the number of API calls needed.
It's used by Flask, FastAPI, Ansible, and many other Python projects.
(It's also why VSCode is telling me that I have some "errors" in reader.html, it just doesn't recognize Jinja2 syntax.)

## main.py

Back onto main.py, now we're ready to start displaying text properly!

### get_page_text()

This route returns the text content for a specific page. 
It's called by the frontend JavaScript when navigating between pages.

```python
@app.get("/api/sessions/{session_id}/pages/{page_number}")
async def get_session_page(session_id: str, page_number: int):
    """
    Get the text content of a specific page.
    
    ROUTE: GET /api/sessions/{session_id}/pages/{page_number}
    
    Args:
        session_id: Which session (from URL query parameter)
        page_number: Which page to get (0-indexed, default is 0)
        
    Returns:
        JSON with page text and navigation info
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
```

You'll first notice that `get_page_text` will GET the page text from the unique session ID and page number.
The session must be validated to ensure it exists.

The text is returned as a JSON response with navigation helpers such as `has_next` and `has_prev`.
This helps manage the UI state and prevent out-of-bounds errors such as trying to navigate to a non-existent page.
In case there's still an error, we'll raise a 400-series error with the error message.

> Andrew! What's the difference between 400, 404, and 500 errors?

4xx errors are client-side errors, while 5xx errors are server-side errors.
Here's a brief breakdown of the errors we might encounter on Mangaroo:

- 400 Bad Request: client sent invalid data (page out of range)
- 404 Not Found: resource doesn't exist (session not found)
- 500 Internal Server Error: server-side bug (PDF processing crash)

We identify these errors by their status codes, and return them to the frontend.
User-facing messages should be friendly and not just HTTP codes.

### reading_sessions{}

The `reading_sessions` dictionary is our simple in-memory session store. It maps session IDs to `ReadingSession` objects.

```python
# Dictionary to store active reading sessions
# Key: session_id (string), Value: ReadingSession object
reading_sessions: dict = {}

# Example usage:
# 1. Create session: reading_sessions["abc123"] = ReadingSession(...)
# 2. Lookup session: session = reading_sessions["abc123"]
# 3. Check exists: if "abc123" in reading_sessions: ...
# 4. Delete session: del reading_sessions["abc123"]
```

The `reading_sessions` dictionary is a simple stateful in-memory session store. 
It maps session IDs to `ReadingSession` objects.
It's also lightning-fast to access, with an average case of O(1).

> Andrew! Why use a Python dictionary instead of a database?

Using a dictionary for Mangaroo is perfect for a quick prototype or learning purposes.
It's extremely fast and simple, but not suitable for production since sessions are lost on server restart.
Some options to scale would be using FastAPI's built-in session middleware, or using a database like MongoDB or PostgreSQL.

If you're interested in a project where I chose to use a database instead of a dictionary, check out the CrawlStars devlog [here](https://github.com/andrewzheng/crawlstars/blob/main/devlog.md)!

> Andrew! What happens when the server restarts?

To put it bluntly, all sessions are lost (dictionary cleared).
Users get 404 errors when trying to access their sessions and need to re-upload their PDFs.


## pdf_processor.py

The PDFProcessor's text extraction methods handle the core functionality: getting text from specific pages and cleaning it for display.

Before we dive into specific functions, let's first design the PDFProcessor class and its signature wrapper function, `extract_page_text()`.

> Andrew! Why did you decide to make an entire PDFProcessor class instead of just using the `extract_page_text()` function?

I decided to create a PDFProcessor class to reuse the same PDF object for multiple page extractions which is more efficient API design.
Having convnenience functions such as `extract_page_text()` is more user-friendly for the frontend.
It also follows the single-responsibility principle where each function does one thing well.

Think of it like buying a car for prolonged use (such as processing many pages of a PDF novel) rather than just renting the car's function (such as calling a bunch of methods on the PDFProcessor class).
Using a class fits the use case of maintaining a consistent story state as the reader reads through the novel.

### extract_page_text()

`extract_page_text()` provides a simpler interface for one-off PDF operations without managing object lifecycles.
It's essentially a neat wrapper around the PDFProcessor class.

```python
def extract_page_text(pdf_path: str, page_number: int) -> str:
    """
    Quick function to extract text from a single page.
    
    USE THIS WHEN:
    - You just need one page's text
    - You don't want to manage open/close yourself
    
    Example:
        text = extract_page_text("book.pdf", 0)  # Get first page
    """
    processor = PDFProcessor(pdf_path)
    try:
        processor.open()
        return processor.get_page_text(page_number)
    finally:
        # 'finally' ensures close() runs even if there's an error
        processor.close()
```

As you can see, `extract_page_text()` is a neat wrapper around the PDFProcessor class containing the key functions `open()`, `get_page_text()`, and `close()`.
The `try/finally` block ensures that the PDFProcessor is closed properly even if an error occurs.

As a sidenote, PyMuPDF does support other text extraction formats such as "dict", "html", "xml", and "blocks".
However, plain text is the cleanest and most consistent format for our use case of just displaying e-text.

### get_page_text()

`get_page_text()` handles the actual text extraction from PDF pages, with validation and error handling.

```python
def get_page_text(self, page_number: int) -> str:
    """
    Extract text from a specific page.
    
    Args:
        page_number: Which page to read (0-indexed, so page 1 = 0)
        
    Returns:
        The extracted text from that page
        
    Raises:
        ValueError: If the PDF isn't open or page number is invalid
    """
    # Safety check: make sure the PDF is open
    if not self._doc:
        raise ValueError("PDF not opened. Call open() first.")
    
    # Safety check: make sure page number is valid
    if page_number < 0 or page_number >= self._total_pages:
        raise ValueError(f"Page {page_number} out of range (0-{self._total_pages - 1})")
    
    # Get the page object from the document
    page = self._doc[page_number]
    
    # Extract text using the "text" format
    text = page.get_text("text")
    
    # Clean up the text before returning
    text = self._clean_text(text)
    return text
```

As you can see, `get_page_text()` takes the PDF previously extracted by PyMuPDF from the upload path functions (also in `pdf_processor.py`).
`get_page_text()` also contains multiple safety checks to fail fast by showing errors 

You might also notice the syntax on `_clean_text()`.
It starts with an underscore since it's a convention when we create a private method.

### _clean_text()

Cleaning PDF text removes formatting artifacts and normalizes whitespace. This makes text more readable and easier for AI to process.

```python
def _clean_text(self, text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace.
    
    WHY CLEAN TEXT?
    - PDFs often have weird formatting artifacts
    - Extra newlines, multiple spaces, etc.
    - Clean text is easier to read and process
    
    Args:
        text: The raw text extracted from PDF
        
    Returns:
        Cleaned up text
    """
    import re
    
    # Replace 3+ newlines with just 2 (paragraph break)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace 2+ spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove whitespace from start and end
    text = text.strip()
    
    return text
```

Many of us have had the experience of trying to copy paste some text from a PDF and getting a bunch of extra newlines and spaces for no reason.
Thus, `_clean_text()` is a chain of methods that uses regex patterns such as `\n{3,}` (which means "3 or more newlines") to remove formatting artifacts and normalize whitespace.

> Andrew! Can you explain the exact regex patterns that you used here?

For reducing excess lines, the "lower bound" is 3 and the "upper bound" is infinite. We get to detect any number of newlines series that are 3 or more, and `sub` them with just 2 newlines.

For reducing excess spaces, the "lower bound" is 2 and the "upper bound" is infinite. We get to detect any number of spaces series that are 2 or more, and `sub` them with just 1 space.

The tradeoff here is that we might lose some intentional formatting (poetry, code blocks) in exchange for a more readable and consistent format.
However, chances are that a PDF novel that our readers consider worthy of illustration are likely not going to be strictly formatted in an academic or abstract way.

Now that the text has been cleaned, it's ready to be displayed to the reader and also ready to be sent to Gemini for analysis.