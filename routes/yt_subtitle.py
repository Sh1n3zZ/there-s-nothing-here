from fastapi import APIRouter, HTTPException
from models.schemas import YouTubeSubtitleRequest, YouTubeSubtitleResponse
from services.yt_subtitle import download_youtube_subtitle, extract_text_from_vtt

router = APIRouter()


@router.post("/download", response_model=YouTubeSubtitleResponse)
async def download_youtube_subtitle_endpoint(request: YouTubeSubtitleRequest):
    """
    Download subtitles from YouTube videos and return as text contents.
    
    Args:
        request: YouTubeSubtitleRequest containing a list of YouTube URLs
        
    Returns:
        YouTubeSubtitleResponse with list of subtitle text contents
    """
    try:
        # Download VTT format subtitles
        vtt_contents = download_youtube_subtitle(request.urls)
        
        # Extract text content from VTT
        subtitle_texts = extract_text_from_vtt(vtt_contents)
        
        return YouTubeSubtitleResponse(
            success=True,
            message=f"Successfully downloaded and extracted subtitles from {len(subtitle_texts)} video(s)",
            subtitle_texts=subtitle_texts
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

