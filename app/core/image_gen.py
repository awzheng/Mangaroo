"""
========================================
Image Generation Module for Autotoon
========================================

This file handles creating manga-style images using Google's Imagen 3 AI via Vertex AI.
It takes scene descriptions and turns them into actual images.

KEY CONCEPT: Imagen 3 via Vertex AI
- Google's state-of-the-art image generation model
- Accessed through Vertex AI SDK with service account authentication
- Creates high-quality images from text descriptions
- We use it specifically for manga-style artwork

WHAT THIS FILE DOES:
1. Takes scene/character descriptions from Story Bible
2. Constructs detailed image generation prompts
3. Calls Imagen 3 API via Vertex AI to create images
4. Returns image data that can be displayed in the browser

FLOW:
    Story Bible → Image Prompt → Imagen 3 (Vertex AI) → Image Data → Browser Display
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# base64: Encodes binary image data as text for sending to browser
# (Browsers can display images encoded as base64 strings)
import base64
import os

# Type hints
from typing import Optional, Dict

# Google Cloud Vertex AI for Imagen
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel

# Our configuration for API keys and project settings
from .config import get_settings


# ----------------------------------------
# IMAGE GENERATOR CLASS
# ----------------------------------------
class ImageGenerator:
    """
    Handles manga-style image generation using Imagen 3 via Vertex AI.
    
    WHAT IT DOES:
    - Takes text descriptions of scenes
    - Generates manga-style images using Google's Imagen 3
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
        
        Sets up the connection to Google Vertex AI services.
        """
        # Configure the Vertex AI connection
        self._configure_vertex_ai()
        
        # Default art style if none specified
        self.default_style = "manga"
        
    def _configure_vertex_ai(self):
        """
        Configure the Google Vertex AI client.
        
        This initializes Vertex AI with service account credentials
        and project settings from the environment.
        """
        settings = get_settings()
        
        # Set credentials environment variable if specified in settings
        if settings.google_application_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
        
        if settings.google_cloud_project:
            try:
                # Initialize Vertex AI
                # us-central1 is the primary region for Imagen
                aiplatform.init(
                    project=settings.google_cloud_project,
                    location="us-central1"
                )
                
                print(f"✓ Vertex AI initialized for project: {settings.google_cloud_project}")
                
                # Load the Imagen model
                # Try the correct model name for this SDK version
                try:
                    self.model = ImageGenerationModel.from_pretrained("imagegeneration@002")
                    print("✓ Loaded Imagen model: imagegeneration@002")
                except Exception as model_error:
                    print(f"⚠ Could not load imagegeneration@002, trying @006: {model_error}")
                    self.model = ImageGenerationModel.from_pretrained("imagegeneration@006")
                    print("✓ Loaded Imagen model: imagegeneration@006")
                
                self.configured = True
            except Exception as e:
                print(f"✗ Error configuring Vertex AI: {e}")
                self.model = None
                self.configured = False
        else:
            # No project configured - can't generate images
            print("✗ No GOOGLE_CLOUD_PROJECT configured")
            self.model = None
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
        if not self.configured or not self.model:
            return {
                "success": False,
                "image_data": None,
                "prompt_used": "",
                "error": "Vertex AI not configured. Check GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS in .env"
            }
        
        # Build a detailed prompt from all the pieces
        prompt = self._build_prompt(
            scene_description,
            characters,
            visual_style,
            mood
        )
        
        try:
            # Generate the image using Vertex AI!
            # This is the actual API call to Google
            print(f"🎨 Calling Imagen API with prompt: {prompt[:100]}...")
            
            response = self.model.generate_images(
                prompt=prompt,
                number_of_images=1
            )
            
            print(f"📦 Response type: {type(response)}")
            print(f"📦 Response dir: {dir(response)}")
            
            # Check if we got an image back
            if hasattr(response, 'images') and response.images and len(response.images) > 0:
                print(f"✓ Got {len(response.images)} image(s)")
                # Get the generated image
                generated_image = response.images[0]
                
                # The image is in bytes format
                image_bytes = generated_image._image_bytes
                
                # Encode the bytes as base64 text for HTML display
                image_data = base64.b64encode(image_bytes).decode('utf-8')
                
                print(f"✓ Image encoded, {len(image_data)} bytes")
                
                return {
                    "success": True,
                    "image_data": image_data,
                    "prompt_used": prompt,
                    "error": None
                }
            else:
                # API returned but no images
                print(f"✗ No images in response")
                print(f"   Response attributes: {vars(response) if hasattr(response, '__dict__') else 'N/A'}")
                return {
                    "success": False,
                    "image_data": None,
                    "prompt_used": prompt,
                    "error": "No images generated by Vertex AI. The API may have filtered the content."
                }
                
        except Exception as e:
            # Something went wrong - return error info
            error_message = str(e)
            
            # Provide helpful error messages
            if "403" in error_message or "Permission" in error_message:
                error_message = "Permission denied. Check that your service account has 'Vertex AI User' role."
            elif "404" in error_message:
                error_message = "Vertex AI API not found. Make sure Vertex AI API is enabled in Google Cloud Console."
            elif "credentials" in error_message.lower():
                error_message = "Could not load credentials. Check GOOGLE_APPLICATION_CREDENTIALS path in .env"
            
            return {
                "success": False,
                "image_data": None,
                "prompt_used": prompt,
                "error": error_message
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
        # Using neutral language to avoid safety filters
        base_style = """Illustrated story panel in manga/webtoon style, 
detailed line art, greyscale, expressive characters, clear composition, 
professional illustration, sequential art style"""
        
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
            prompt_parts.append(f"Art style: {visual_style}")
        
        # Add mood/atmosphere
        if mood:
            prompt_parts.append(f"Atmosphere: {mood}")
        
        # Add quality boosters at the end
        prompt_parts.append("High quality illustration, detailed artwork, professional comic art")
        
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
