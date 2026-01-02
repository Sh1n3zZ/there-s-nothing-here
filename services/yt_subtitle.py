import yt_dlp
import tempfile
import os
from pathlib import Path
from typing import List
import webvtt


def download_youtube_subtitle(urls: List[str], subtitle_lang: str = "en") -> List[str]:
    """
    Download subtitles from YouTube videos using yt-dlp (batch processing).
    
    Args:
        urls: List of YouTube video URLs
        subtitle_lang: Subtitle language code (default: "en")
        
    Returns:
        List of subtitle text content in vtt format (one for each URL)
    """
    results = []
    
    for url in urls:
        # Create a temporary directory to store the subtitle file for each URL
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
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
                        raise Exception(f"No subtitle file found in vtt format for URL: {url}")
                    
                    # Read the first subtitle file found (usually there's only one)
                    subtitle_file = subtitle_files[0]
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_text = f.read()
                    
                    results.append(subtitle_text)
                    
            except yt_dlp.DownloadError as e:
                raise Exception(f"Failed to download subtitle for URL {url}: {str(e)}")
            except Exception as e:
                raise Exception(f"Error downloading subtitle for URL {url}: {str(e)}")
    
    return results

def extract_text_from_vtt(vtt_contents: List[str]) -> List[str]:
    """
    Extract all text content from VTT format subtitles and concatenate into complete texts (batch processing).
    
    Args:
        vtt_contents: List of VTT format subtitle content as strings
        
    Returns:
        List of complete text content extracted from VTT subtitles (one for each input)
    """
    results = []
    
    for vtt_content in vtt_contents:
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
            results.append(complete_text)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from VTT: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    return results
