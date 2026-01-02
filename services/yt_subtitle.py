import yt_dlp
import tempfile
import os
from pathlib import Path
import webvtt


def download_youtube_subtitle(url: str, subtitle_lang: str = "en") -> str:
    """
    Download subtitle from YouTube video using youtube-dl.
    
    Args:
        url: YouTube video URL
        subtitle_lang: Subtitle language code (default: "en")
        
    Returns:
        Subtitle text content in vtt format
    """
    # Create a temporary directory to store the subtitle file
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            # 'verbose': True,
            'skip_download': True,
            'writesubtitles': True,
            'subtitleslangs': [subtitle_lang],
            'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info and download subtitles
                info = ydl.extract_info(url, download=True)
                
                # Find the subtitle file in the temp directory
                # The subtitle file should be in vtt format
                # Filename format is usually: video_title.lang.vtt or video_title.vtt
                subtitle_files = list(Path(temp_dir).glob('*.vtt'))
                
                if not subtitle_files:
                    raise Exception("No subtitle file found in vtt format")
                
                # Read the first subtitle file found (usually there's only one)
                subtitle_file = subtitle_files[0]
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    subtitle_text = f.read()
                
                return subtitle_text
                
        except yt_dlp.DownloadError as e:
            raise Exception(f"Failed to download subtitle: {str(e)}")
        except Exception as e:
            raise Exception(f"Error downloading subtitle: {str(e)}")

def extract_text_from_vtt(vtt_content: str) -> str:
    """
    Extract all text content from VTT format subtitle and concatenate into a complete text.
    
    Args:
        vtt_content: VTT format subtitle content as string
        
    Returns:
        Complete text content extracted from VTT subtitles
    """
    # Create a temporary file to store VTT content
    # webvtt.read() requires a file path, not string content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(vtt_content)
        temp_file_path = temp_file.name
    
    try:
        # Read and parse VTT file
        text_lines = []
        for caption in webvtt.read(temp_file_path):
            # Extract text content from each caption
            text = caption.text.strip()
            if text:  # Skip empty captions
                text_lines.append(text)
        
        # Join all text lines with spaces to form a complete text
        complete_text = ' '.join(text_lines)
        return complete_text
        
    except Exception as e:
        raise Exception(f"Failed to extract text from VTT: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
