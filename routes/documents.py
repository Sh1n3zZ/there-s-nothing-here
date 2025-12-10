from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from services.docx import replace_keywords
from utils.file import generate_output_filename
import json
from urllib.parse import quote

router = APIRouter()


@router.post("/replace")
async def replace_document_keywords(
    file: UploadFile = File(...),
    replacements: str = Form(...)
):
    """
    Upload a docx file and replace keywords.
    Returns the processed file directly without saving to disk.
    """
    try:
        replacements_dict = json.loads(replacements)

        file_content = await file.read()
        
        output_content = replace_keywords(file_content, replacements_dict)
        
        output_filename = generate_output_filename(file.filename)
        
        # Use RFC 5987 encoding for filenames with non-ASCII characters
        # Format: filename*=UTF-8''encoded-name
        encoded_filename = quote(output_filename, safe='')
        content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"
        
        return Response(
            content=output_content,
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": content_disposition}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

