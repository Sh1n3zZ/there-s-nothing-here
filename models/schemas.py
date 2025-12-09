from pydantic import BaseModel
from typing import Dict


class ReplaceRequest(BaseModel):
    """Request model for keyword replacement."""
    replacements: Dict[str, str]


class ReplaceResponse(BaseModel):
    """Response model for keyword replacement."""
    success: bool
    message: str
    output_filename: str = None

