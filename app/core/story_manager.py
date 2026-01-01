"""
========================================
Story Manager Module for Mangaroo
========================================

*** CRITICAL FILE - THE HEART OF THE APP ***

This file contains the "Story Bible" - the brain that keeps track
of characters, settings, and visual details across your entire story.

KEY CONCEPT: Visual Continuity
- When you read a novel, you imagine characters looking the same throughout
- If the hero has blue eyes on page 1, they should have blue eyes on page 100
- The Story Bible ensures AI-generated images maintain this consistency

WHAT THIS FILE DOES:
1. Tracks characters (names, appearances, clothing)
2. Tracks settings (locations, time of day, atmosphere)
3. Uses Gemini AI to analyze new text and update the story context
4. Generates prompts for image creation based on current story state

HOW IT WORKS:
- Each time you move to a new page, we send the text to Gemini
- Gemini extracts: Who's in the scene? What do they look like? Where are they?
- This info is stored and used when generating manga panels
- Previous context is included so Gemini knows what came before
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
# json: For converting Python objects to/from JSON strings
# JSON is a text format for storing structured data
import json

# Type hints for clearer code
from typing import Dict, Optional, List

# Google's Generative AI library for Gemini
import google.generativeai as genai

# Our configuration to get the API key
from .config import get_settings


# ----------------------------------------
# STORY BIBLE CLASS
# ----------------------------------------
class StoryBible:
    """
    The Story Bible maintains narrative and visual context across pages.
    
    ANALOGY: Think of it like a TV show's "series bible"
    - Character sheets: What does each character look like?
    - Setting guides: What does each location look like?
    - Plot summary: What's happened so far?
    
    This ensures visual consistency - like how animated characters
    always look the same episode to episode.
    
    HOW TO USE:
        bible = StoryBible()
        state = await bible.update_state("Chapter 1: John entered...")
        # state now contains character info, scene description, etc.
        prompt = bible.get_image_prompt()
        # prompt is ready to send to image generation
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
        # Get our settings (which includes the API key)
        settings = get_settings()
        
        # If we have an API key, set up the AI
        if settings.gemini_api_key:
            # Configure the library with our API key
            genai.configure(api_key=settings.gemini_api_key)
            
            # Create a Gemini 1.5 Pro model instance
            # This is the model we'll use for text analysis
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            # No API key - AI features won't work
            self.model = None
    
    async def update_state(
        self, 
        new_text: str, 
        previous_state: Optional[Dict] = None
    ) -> Dict:
        """
        Update the Story Bible state based on new text content.
        
        *** THIS IS THE KEY METHOD ***
        
        It takes new page text and asks Gemini to:
        1. Identify characters in the scene
        2. Describe their current appearance/clothing
        3. Describe the setting/location
        4. Suggest a visual style for the manga panel
        
        IMPORTANT: We include previous_state so Gemini knows:
        - What characters looked like before
        - What already happened in the story
        This ensures visual CONTINUITY across pages!
        
        Args:
            new_text: The text from the current page
            previous_state: The story state from before (optional)
            
        Returns:
            Updated state dictionary with:
            - current_scene: What to draw
            - characters: Who's in the scene
            - visual_style: How to draw it
            - mood: The emotional tone
            ... and more
        """
        # Use current state if no previous state provided
        if previous_state is None:
            previous_state = self.state
            
        # If AI isn't configured, return a basic placeholder
        if not self.model:
            return self._generate_placeholder_state(new_text)
        
        # Build the prompt that tells Gemini what to analyze
        prompt = self._build_analysis_prompt(new_text, previous_state)
        
        try:
            # Send the prompt to Gemini and wait for response
            # 'await' is used because this is an async (non-blocking) operation
            response = await self.model.generate_content_async(
                prompt,
                # Tell Gemini to return JSON format
                generation_config=genai.GenerationConfig(
                    temperature=0.7,  # Creativity level (0=focused, 1=creative)
                    response_mime_type="application/json"  # We want JSON back
                )
            )
            
            # Parse the JSON response into a Python dictionary
            result = json.loads(response.text)
            
            # Update our internal state with the new information
            self.state = {
                "current_scene": result.get("current_scene", ""),
                "characters": result.get("characters", []),
                "visual_style": result.get("visual_style", ""),
                "story_summary": result.get("story_summary", self.state.get("story_summary", "")),
                "mood": result.get("mood", ""),
                "time_of_day": result.get("time_of_day", ""),
                "location_details": result.get("location_details", "")
            }
            
            return self.state
            
        except Exception as e:
            # If anything goes wrong, log it and return placeholder
            print(f"Error updating story state: {e}")
            return self._generate_placeholder_state(new_text)
    
    def _build_analysis_prompt(self, new_text: str, previous_state: Dict) -> str:
        """
        Build the prompt that we send to Gemini for analysis.
        
        PROMPT ENGINEERING:
        - We carefully craft what we ask Gemini
        - Include previous context for continuity
        - Request specific JSON format for easy parsing
        - Give clear instructions on what to extract
        
        Args:
            new_text: The new page text to analyze
            previous_state: What we know from previous pages
            
        Returns:
            A carefully crafted prompt string
        """
        # Convert previous state to formatted JSON string
        previous_state_json = json.dumps(previous_state, indent=2)
        
        # The prompt tells Gemini exactly what we need
        # It's like giving detailed instructions to an assistant
        prompt = f"""You are a manga storyboard assistant. Your job is to analyze novel text and extract visual information for creating manga panels.

Here is the previous context from earlier pages:
{previous_state_json}

Here is the new text from the current page:
---
{new_text}
---

Update the story bible with the following information. IMPORTANT: Maintain visual continuity with previous descriptions - if a character was described as wearing a red jacket before, they should still be wearing it unless the text explicitly says otherwise.

Return a JSON object with these exact keys:

1. "current_scene": A vivid, visual description of the most dramatic or important moment on this page. Focus on what would make the best manga panel. Be specific about poses, expressions, and spatial relationships. (2-3 sentences)

2. "characters": An array of character objects. Each character should have:
   - "name": Character name
   - "appearance": Physical description (hair, build, distinguishing features)
   - "clothing": Current outfit description
   - "expression": Current emotional state/facial expression
   - "position": Where they are in the scene

3. "visual_style": Recommended manga art direction for this scene (e.g., "high contrast dramatic shadows", "soft shoujo sparkles", "action lines with motion blur", "peaceful slice-of-life warmth")

4. "mood": The emotional tone of the scene (e.g., "tense", "romantic", "melancholic", "action-packed")

5. "time_of_day": When this scene takes place

6. "location_details": Specific details about the setting/background

7. "story_summary": A brief running summary of the story so far (update the previous summary with new events)

Respond ONLY with the JSON object, no additional text."""

        return prompt
    
    def _generate_placeholder_state(self, text: str) -> Dict:
        """
        Generate a basic placeholder when AI is unavailable.
        
        This is a fallback - if the API key is missing or
        there's an error, we still return something useful.
        
        Args:
            text: The text to create a placeholder from
            
        Returns:
            A basic state dictionary
        """
        # Split text into words
        words = text.split()
        
        # Create a preview (first 50 words)
        preview = ' '.join(words[:50]) + "..." if len(words) > 50 else text
        
        return {
            "current_scene": f"Scene based on: {preview}",
            "characters": [],
            "visual_style": "manga black and white with screentones",
            "mood": "neutral",
            "time_of_day": "unspecified",
            "location_details": "unspecified location",
            "story_summary": preview
        }
    
    def get_image_prompt(self) -> str:
        """
        Generate an image generation prompt from the current state.
        
        This takes all our story knowledge and creates a detailed
        prompt for the image generation AI (Imagen).
        
        The prompt includes:
        - Scene description
        - Character appearances
        - Setting details
        - Mood and style
        
        Returns:
            A detailed prompt string ready for image generation
        """
        # Build character descriptions
        characters_desc = ""
        if self.state["characters"]:
            char_parts = []
            for char in self.state["characters"]:
                # Handle both dict format and string format
                if isinstance(char, dict):
                    char_str = f"{char.get('name', 'Character')}"
                    if char.get('appearance'):
                        char_str += f" ({char['appearance']})"
                    if char.get('clothing'):
                        char_str += f" wearing {char['clothing']}"
                    if char.get('expression'):
                        char_str += f", {char['expression']} expression"
                    char_parts.append(char_str)
                else:
                    char_parts.append(str(char))
            characters_desc = "Characters: " + "; ".join(char_parts)
        
        # Combine all parts into a single prompt
        prompt_parts = [
            "Manga-style illustration,",
            f"Scene: {self.state['current_scene']}",
            characters_desc,
            f"Setting: {self.state.get('location_details', '')}",
            f"Mood: {self.state.get('mood', '')}",
            f"Time: {self.state.get('time_of_day', '')}",
            f"Style: {self.state['visual_style']}",
            "Black and white manga art, detailed linework, professional quality"
        ]
        
        # Join non-empty parts with spaces
        # filter(None, ...) removes empty strings
        return " ".join(filter(None, prompt_parts))
    
    def reset(self):
        """
        Reset the Story Bible to initial empty state.
        
        USE THIS WHEN:
        - Starting a new book
        - User wants to start over
        - Clearing for a new session
        """
        self.state = {
            "current_scene": "",
            "characters": [],
            "visual_style": "",
            "story_summary": "",
            "mood": "",
            "time_of_day": "",
            "location_details": ""
        }
    
    def to_dict(self) -> Dict:
        """
        Export current state as a dictionary.
        
        Useful for:
        - Saving state to a file/database
        - Sending state to the frontend
        - Debugging
        
        Returns:
            A copy of the current state
        """
        # .copy() creates a shallow copy so modifications
        # don't affect the original
        return self.state.copy()
    
    def from_dict(self, state: Dict):
        """
        Import state from a dictionary.
        
        Useful for:
        - Loading saved state
        - Restoring a previous session
        
        Args:
            state: A state dictionary to load
        """
        # .update() merges the provided dict into self.state
        self.state.update(state)
