from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from models.schemas import YouTubeSubtitleRequest, YouTubeSubtitleResponse
from services.yt_subtitle import download_youtube_subtitle, extract_text_from_vtt, get_video_title, create_word_document
from urllib.parse import quote
import zipfile
from io import BytesIO
from datetime import datetime

router = APIRouter()


@router.post("/download")
async def download_youtube_subtitle_endpoint(request: YouTubeSubtitleRequest):
    """
    Download subtitles from YouTube videos and return as text contents or Word documents.
    
    Args:
        request: YouTubeSubtitleRequest containing a list of YouTube URLs and output_word flag
        
    Returns:
        YouTubeSubtitleResponse with list of subtitle text contents (if output_word=False)
        or Response with Word document(s) (if output_word=True)
    """
    try:
        # Download VTT format subtitles
        vtt_contents = download_youtube_subtitle(request.urls)
        
        # Extract text content from VTT
        subtitle_texts = extract_text_from_vtt(vtt_contents)
        
        # If output_word is True, return Word document(s)
        if request.output_word:
            if len(request.urls) == 1:
                # Single file: return Word document directly
                word_content = create_word_document(subtitle_texts[0])
                title = get_video_title(request.urls[0])
                filename = f"{title}.docx"
                
                # Use RFC 5987 encoding for filenames with non-ASCII characters
                encoded_filename = quote(filename, safe='')
                content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"
                
                return Response(
                    content=word_content,
                    media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": content_disposition}
                )
            else:
                # Multiple files: create zip archive
                zip_buffer = BytesIO()
                # Track base filenames count to handle duplicates
                filename_counts = {}
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for url, subtitle_text in zip(request.urls, subtitle_texts):
                        title = get_video_title(url)
                        base_filename = f"{title}.docx"
                        
                        # Count occurrences of this base filename
                        if base_filename not in filename_counts:
                            filename_counts[base_filename] = 0
                            filename = base_filename
                        else:
                            filename_counts[base_filename] += 1
                            name, ext = base_filename.rsplit('.', 1)
                            filename = f"{name} ({filename_counts[base_filename]}).{ext}"
                        
                        word_content = create_word_document(subtitle_text)
                        zip_file.writestr(filename, word_content)
                
                zip_buffer.seek(0)
                # Generate timestamp in format YYMMDDHHMMSS
                timestamp = datetime.now().strftime("%y%m%d%H%M%S")
                zip_filename = f"subtitles_{timestamp}.zip"
                encoded_filename = quote(zip_filename, safe='')
                content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"
                
                return Response(
                    content=zip_buffer.getvalue(),
                    media_type="application/zip",
                    headers={"Content-Disposition": content_disposition}
                )
        else:
            # Return JSON response with text contents
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

