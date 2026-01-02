from pydantic import BaseModel
from typing import Dict, Optional, List

class YouTubeSubtitleRequest(BaseModel):
    """Request model for YouTube subtitle download."""
    urls: List[str]
    output_word: bool = False


class YouTubeSubtitleResponse(BaseModel):
    """Response model for YouTube subtitle download."""
    success: bool
    message: str
    subtitle_texts: Optional[List[str]] = None
