"""
========================================
Image Generation Module for Mangaroo
========================================

This file handles creating manga-style images using Google's Imagen 3 AI.
It takes scene descriptions and turns them into actual images.

KEY CONCEPT: Imagen 3
- Google's state-of-the-art image generation model
- Creates high-quality images from text descriptions
- We use it specifically for manga-style artwork

WHAT THIS FILE DOES:
1. Takes scene/character descriptions from Story Bible
2. Constructs detailed image generation prompts
3. Calls Imagen 3 API to create images
4. Returns image data that can be displayed in the browser

FLOW:
    Story Bible → Image Prompt → Imagen 3 → Image Data → Browser Display
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# base64: Encodes binary image data as text for sending to browser
# (Browsers can display images encoded as base64 strings)
import base64

# Type hints
from typing import Optional, Dict

# Google's new GenAI library for Imagen
from google import genai
from google.genai import types

# Our configuration for API keys
from .config import get_settings


# ----------------------------------------
# IMAGE GENERATOR CLASS
# ----------------------------------------
class ImageGenerator:
    """
    Handles manga-style image generation using Imagen 3.
    
    WHAT IT DOES:
    - Takes text descriptions of scenes
    - Generates manga-style images
    - Returns images as base64 data (displayable in HTML)
    
    HOW TO USE:
        generator = ImageGenerator()
        result = await generator.generate_panel(
            scene_description="A samurai drawing his sword in the rain",
            characters=[{"name": "Kenji", "appearance": "tall with scar"}],
            visual_style="dramatic shadows"
        )
        if result["success"]:
            image_data = result["image_data"]  # base64 string
    """
    
    def __init__(self):
        """
        Initialize the image generator.
        
        Sets up the connection to Google's AI services.
        """
        # Configure the AI connection
        self._configure_genai()
        
        # Default art style if none specified
        self.default_style = "manga"
        
    def _configure_genai(self):
        """
        Configure the Google Generative AI client.
        
        This is similar to the Story Manager setup.
        We need the API key to use Google's services.
        """
        settings = get_settings()
        
        if settings.gemini_api_key:
            # Set up the client with our API key
            self.client = genai.Client(api_key=settings.gemini_api_key)
            self.configured = True
        else:
            # No API key - can't generate images
            self.client = None
            self.configured = False
    
    async def generate_panel(
        self,
        scene_description: str,
        characters: list = None,
        visual_style: str = None,
        mood: str = None,
        aspect_ratio: str = "3:4"
    ) -> Dict:
        """
        Generate a manga panel image based on the scene description.
        
        This is the main method - it creates the actual image!
        
        PARAMETERS EXPLAINED:
        - scene_description: What's happening ("A hero facing the villain")
        - characters: List of who's in the scene with their looks
        - visual_style: Art direction ("dramatic", "soft", "action")
        - mood: Emotional tone ("tense", "peaceful", "exciting")
        - aspect_ratio: Image shape (3:4 is typical manga panel ratio)
        
        RETURN VALUE:
        A dictionary with:
        - success: Did it work? (True/False)
        - image_data: The image as base64 text (if successful)
        - prompt_used: What we asked the AI to generate
        - error: What went wrong (if failed)
        
        Args:
            scene_description: Text description of the scene
            characters: List of character descriptions
            visual_style: Art style direction
            mood: Emotional tone
            aspect_ratio: Image dimensions ratio
            
        Returns:
            Dictionary with generation results
        """
        # Check if we're configured properly
        if not self.configured:
            return {
                "success": False,
                "image_data": None,
                "prompt_used": "",
                "error": "API key not configured"
            }
        
        # Build a detailed prompt from all the pieces
        prompt = self._build_prompt(
            scene_description,
            characters,
            visual_style,
            mood
        )
        
        try:
            # Generate the image using the new GenAI client!
            # This is the actual API call to Google
            response = self.client.models.generate_image(
                model="imagen-3.0-generate-001",  # Imagen 3 model
                prompt=prompt,
                config=types.GenerateImageConfig(
                    number_of_images=1,          # Generate 1 image
                    aspect_ratio=aspect_ratio,    # e.g., "3:4"
                    safety_filter_level="block_few",  # Allow most content
                    person_generation="allow_adult"   # Allow adult characters
                )
            )
            
            # Check if we got an image back
            if response.generated_image:
                # Get the generated image
                generated_image = response.generated_image
                
                # The image is already in bytes format
                image_bytes = generated_image.image.image_bytes
                
                # Encode the bytes as base64 text for HTML display
                image_data = base64.b64encode(image_bytes).decode('utf-8')
                
                return {
                    "success": True,
                    "image_data": image_data,
                    "prompt_used": prompt,
                    "error": None
                }
            else:
                # API returned but no images
                return {
                    "success": False,
                    "image_data": None,
                    "prompt_used": prompt,
                    "error": "No images generated"
                }
                
        except Exception as e:
            # Something went wrong - return error info
            return {
                "success": False,
                "image_data": None,
                "prompt_used": prompt,
                "error": str(e)
            }
    
    def _build_prompt(
        self,
        scene_description: str,
        characters: list = None,
        visual_style: str = None,
        mood: str = None
    ) -> str:
        """
        Build a detailed prompt for manga image generation.
        
        PROMPT ENGINEERING FOR IMAGES:
        - Start with style instructions (tells AI the overall look)
        - Add scene description (what's happening)
        - Include character details (who's there)
        - Add mood and style (how it should feel)
        - End with quality boosters (professional, detailed, etc.)
        
        A good prompt = better images!
        
        Args:
            scene_description: What's happening in the scene
            characters: Who's in the scene
            visual_style: Art style direction
            mood: Emotional tone
            
        Returns:
            Complete prompt string
        """
        # Start with base style instructions
        # This tells Imagen we want manga-style art
        base_style = """Professional manga illustration, black and white with screentones, 
detailed linework, dramatic composition, Japanese manga art style, 
clean lines, expressive characters"""
        
        # Start building the prompt with the base style
        prompt_parts = [base_style]
        
        # Add the scene description
        if scene_description:
            prompt_parts.append(f"Scene: {scene_description}")
        
        # Add character descriptions
        if characters:
            char_descriptions = []
            for char in characters:
                # Handle dictionary format (from Story Bible)
                if isinstance(char, dict):
                    desc = char.get('name', '')
                    if char.get('appearance'):
                        desc += f", {char['appearance']}"
                    if char.get('clothing'):
                        desc += f", wearing {char['clothing']}"
                    if char.get('expression'):
                        desc += f", {char['expression']} expression"
                    char_descriptions.append(desc)
                # Handle simple string format
                elif isinstance(char, str):
                    char_descriptions.append(char)
            
            if char_descriptions:
                prompt_parts.append(f"Characters: {'; '.join(char_descriptions)}")
        
        # Add visual style direction
        if visual_style:
            prompt_parts.append(f"Art direction: {visual_style}")
        
        # Add mood/atmosphere
        if mood:
            prompt_parts.append(f"Mood: {mood}")
        
        # Add quality boosters at the end
        prompt_parts.append("High quality, detailed, professional manga panel")
        
        # Join all parts with periods
        return ". ".join(prompt_parts)
    
    async def generate_from_story_bible(self, story_bible_state: Dict) -> Dict:
        """
        Generate an image directly from a Story Bible state.
        
        CONVENIENCE METHOD:
        Instead of manually extracting scene, characters, etc.
        from the Story Bible, this method does it for you.
        
        Args:
            story_bible_state: The current state from StoryBible
            
        Returns:
            Image generation result dictionary
            
        Example:
            bible = StoryBible()
            state = await bible.update_state(page_text)
            result = await generator.generate_from_story_bible(state)
        """
        return await self.generate_panel(
            scene_description=story_bible_state.get("current_scene", ""),
            characters=story_bible_state.get("characters", []),
            visual_style=story_bible_state.get("visual_style", ""),
            mood=story_bible_state.get("mood", "")
        )


# ----------------------------------------
# SINGLETON PATTERN
# ----------------------------------------
# We only need ONE image generator for the whole app
# This pattern ensures we reuse the same instance

# Private variable to store the single instance
_generator: Optional[ImageGenerator] = None


def get_image_generator() -> ImageGenerator:
    """
    Get or create the singleton ImageGenerator instance.
    
    SINGLETON PATTERN:
    - Only one ImageGenerator exists at a time
    - Every call to this function returns the same instance
    - More efficient than creating new instances repeatedly
    
    WHY USE THIS?
    - Saves memory (one instance vs many)
    - Consistent configuration
    - Standard pattern in web applications
    
    Returns:
        The shared ImageGenerator instance
        
    Example:
        generator = get_image_generator()
        result = await generator.generate_panel(...)
    """
    global _generator  # Use the module-level variable
    
    # If no instance exists yet, create one
    if _generator is None:
        _generator = ImageGenerator()
    
    return _generator
