from pydantic import BaseModel
from typing import Dict, Optional

class ReplaceRequest(BaseModel):
    """Request model for keyword replacement."""
    replacements: Dict[str, str]

class ReplaceResponse(BaseModel):
    """Response model for keyword replacement."""
    success: bool
    message: str
    output_filename: str = None

class YouTubeSubtitleRequest(BaseModel):
    """Request model for YouTube subtitle download."""
    url: str


class YouTubeSubtitleResponse(BaseModel):
    """Response model for YouTube subtitle download."""
    success: bool
    message: str
    subtitle_text: Optional[str] = None
