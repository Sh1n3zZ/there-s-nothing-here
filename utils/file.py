import os
from pathlib import Path
from fastapi import UploadFile


def save_uploaded_file(file: UploadFile, upload_dir: str = "uploads") -> str:
    """
    Save uploaded file to the specified directory.
    
    Args:
        file: Uploaded file object
        upload_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    Path(upload_dir).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    return file_path


def generate_output_filename(input_filename: str, suffix: str = "_replaced") -> str:
    """
    Generate output filename based on input filename.
    
    Args:
        input_filename: Original filename
        suffix: Suffix to add before file extension
        
    Returns:
        Generated output filename
    """
    path = Path(input_filename)
    stem = path.stem
    extension = path.suffix
    return f"{stem}{suffix}{extension}"

