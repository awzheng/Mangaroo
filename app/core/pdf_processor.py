"""
========================================
PDF Processing Module for Mangaroo
========================================

This file handles everything related to reading PDF files.
It extracts the text content so we can analyze it with AI.

KEY CONCEPT: PyMuPDF (fitz)
- PyMuPDF is a library for working with PDF files
- We import it as "fitz" (historical name from the library's origins)
- It can read text, images, and metadata from PDFs

WHAT THIS FILE DOES:
1. Opens PDF files safely
2. Extracts text from each page
3. Cleans up the text (removes extra spaces, etc.)
4. Gets PDF metadata (title, author, page count)
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# fitz is PyMuPDF - the library for reading PDFs
# We install it as "pymupdf" but import it as "fitz"
import fitz

# Type hints make code easier to understand
# List = a collection of items, Dict = key-value pairs, Optional = can be None
from typing import List, Dict, Optional

# Path helps us work with file paths in a cross-platform way
from pathlib import Path


# ----------------------------------------
# PDF PROCESSOR CLASS
# ----------------------------------------
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
        It's like the "constructor" - it sets up the initial state.
        
        Args:
            pdf_path: The file path to the PDF (e.g., "uploads/mybook.pdf")
        """
        # Store the path as a Path object for easier manipulation
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
            # fitz.open() reads the PDF file into memory
            self._doc = fitz.open(self.pdf_path)
            
            # len() on a document gives the page count
            self._total_pages = len(self._doc)
            
            return True
        except Exception as e:
            # If anything goes wrong, print the error and return False
            print(f"Error opening PDF: {e}")
            return False
    
    def close(self):
        """
        Close the PDF document and free up memory.
        
        IMPORTANT: Always close files when done!
        - Open files use memory and system resources
        - Closing releases those resources
        - Prevents memory leaks in long-running applications
        """
        if self._doc:
            self._doc.close()
            self._doc = None
    
    @property  # This decorator makes the method act like a variable
    def total_pages(self) -> int:
        """
        Get total number of pages in the PDF.
        
        WHAT IS @property?
        - It lets you access a method like a variable
        - Instead of: processor.total_pages()
        - You write: processor.total_pages
        
        Returns:
            The number of pages in the PDF
        """
        return self._total_pages
    
    def get_page_text(self, page_number: int) -> str:
        """
        Extract text from a specific page.
        
        This is the core function - it gets the actual text content
        from a page so we can display it and send it to AI.
        
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
        # Pages are 0-indexed: first page = 0, second = 1, etc.
        if page_number < 0 or page_number >= self._total_pages:
            raise ValueError(f"Page {page_number} out of range (0-{self._total_pages - 1})")
        
        # Get the page object from the document
        # self._doc[0] gets the first page, [1] gets second, etc.
        page = self._doc[page_number]
        
        # Extract text using the "text" format
        # Other formats: "dict" (structured), "html", "xml"
        text = page.get_text("text")
        
        # Clean up the text before returning
        text = self._clean_text(text)
        return text
    
    def get_all_pages(self) -> List[Dict[str, any]]:
        """
        Extract text from ALL pages at once.
        
        WHEN TO USE:
        - When you need the entire book's text
        - For preprocessing or indexing
        
        Returns:
            A list of dictionaries, each containing:
            - "page_number": The page index
            - "text": The page content
            
        Example return value:
            [
                {"page_number": 0, "text": "Chapter 1..."},
                {"page_number": 1, "text": "The story begins..."},
            ]
        """
        if not self._doc:
            raise ValueError("PDF not opened. Call open() first.")
        
        pages = []
        # range() creates a sequence: 0, 1, 2, ... up to total_pages-1
        for i in range(self._total_pages):
            pages.append({
                "page_number": i,
                "text": self.get_page_text(i)
            })
        return pages
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing excessive whitespace.
        
        WHY CLEAN TEXT?
        - PDFs often have weird formatting artifacts
        - Extra newlines, multiple spaces, etc.
        - Clean text is easier to read and process
        
        The underscore prefix (_clean_text) indicates this is a
        "private" method - meant for internal use only.
        
        Args:
            text: The raw text extracted from PDF
            
        Returns:
            Cleaned up text
        """
        # Import regex module for pattern matching
        import re
        
        # Replace 3+ newlines with just 2 (paragraph break)
        # \n = newline, {3,} = 3 or more times
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Replace 2+ spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove whitespace from start and end
        text = text.strip()
        
        return text
    
    def get_metadata(self) -> Dict[str, str]:
        """
        Extract PDF metadata (title, author, etc.)
        
        WHAT IS METADATA?
        - Information ABOUT the document (not the content)
        - Title, author, creation date, etc.
        - Set by whoever created the PDF
        
        Returns:
            Dictionary with metadata fields
        """
        if not self._doc:
            raise ValueError("PDF not opened. Call open() first.")
        
        # self._doc.metadata is a dictionary of PDF metadata
        metadata = self._doc.metadata
        
        # Return a cleaned-up version with defaults for missing values
        return {
            "title": metadata.get("title", "Unknown"),
            "author": metadata.get("author", "Unknown"),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "total_pages": self._total_pages
        }


# ----------------------------------------
# CONVENIENCE FUNCTIONS
# ----------------------------------------
# These are standalone functions that use PDFProcessor internally
# They're simpler to use for one-off operations

def extract_page_text(pdf_path: str, page_number: int) -> str:
    """
    Quick function to extract text from a single page.
    
    USE THIS WHEN:
    - You just need one page's text
    - You don't want to manage open/close yourself
    
    Args:
        pdf_path: Path to the PDF file
        page_number: Which page to read (0-indexed)
        
    Returns:
        The text content of that page
        
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


def get_pdf_info(pdf_path: str) -> Dict[str, any]:
    """
    Quick function to get basic PDF information.
    
    USE THIS WHEN:
    - You need to know page count, title, author, etc.
    - Before deciding whether to process a file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with PDF info including total pages
        
    Example:
        info = get_pdf_info("book.pdf")
        print(f"This book has {info['total_pages']} pages")
    """
    processor = PDFProcessor(pdf_path)
    try:
        processor.open()
        return processor.get_metadata()
    finally:
        processor.close()
