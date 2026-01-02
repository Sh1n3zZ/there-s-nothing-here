from fastapi import APIRouter, HTTPException
from models.schemas import YouTubeSubtitleRequest, YouTubeSubtitleResponse
from services.yt_subtitle import download_youtube_subtitle, extract_text_from_vtt

router = APIRouter()


@router.post("/download", response_model=YouTubeSubtitleResponse)
async def download_youtube_subtitle_endpoint(request: YouTubeSubtitleRequest):
    """
    Download subtitle from YouTube video and return as text content.
    
    Args:
        request: YouTubeSubtitleRequest containing the YouTube URL
        
    Returns:
        YouTubeSubtitleResponse with subtitle text content
    """
    try:
        # Download VTT format subtitle
        vtt_content = download_youtube_subtitle(request.url)
        
        # Extract text content from VTT
        subtitle_text = extract_text_from_vtt(vtt_content)
        
        return YouTubeSubtitleResponse(
            success=True,
            message="Subtitle downloaded and extracted successfully",
            subtitle_text=subtitle_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

